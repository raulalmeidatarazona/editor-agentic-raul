"""Bounded local FFmpeg adapter; no inference, transformations or providers."""

from __future__ import annotations

import hashlib
import os
import re
import selectors
import subprocess
import time
from fractions import Fraction
from pathlib import Path

from content_contract import (ContractError, MAX_INTEGER, MAX_JSON, atomic_json,
                              canonical_bytes, digest, load_json, rational,
                              unknown_fields, validate_inspection, validate_options)

EVIDENCE_LIMIT = 512 * 1024 * 1024
LOG_LIMIT = 2 * 1024 * 1024


def inspector_version():
    h = hashlib.sha256()
    for name in ("content_contract.py", "media_inspection.py", "ingest.py"):
        h.update(name.encode())
        h.update((Path(__file__).parent / name).read_bytes())
    return "f002-v1/" + h.hexdigest()


def tool_versions(ffprobe="ffprobe", ffmpeg="ffmpeg"):
    versions = {}
    for kind, executable in (("ffprobe", ffprobe), ("ffmpeg", ffmpeg)):
        try:
            r = subprocess.run([executable, "-version"], capture_output=True, text=True, timeout=10, check=True)
            versions[kind] = r.stdout.splitlines()[0]
        except (OSError, subprocess.SubprocessError, IndexError) as exc:
            raise ContractError("TOOL_UNAVAILABLE", "Use the approved existing FFmpeg/ffprobe tools; do not auto-install.", kind) from exc
        if not re.search(r"\bversion 9\.0\.1\b", versions[kind]):
            raise ContractError("TOOL_VERSION_MISMATCH", "Recheck compatibility with the approved 9.0.1 tools before changing versions.", kind)
    return versions


class Runner:
    """Drain both pipes concurrently, cap bytes, kill on timeout; retain diagnostics."""

    def __init__(self, directory, timeout=600, limit=EVIDENCE_LIMIT):
        if type(timeout) is not int or not 1 <= timeout <= 3600:
            raise ContractError("INVALID_TIMEOUT", "Timeout must be 1..3600 seconds.", "timeout", "INVALID")
        self.directory, self.timeout, self.limit = Path(directory), timeout, limit
        self.used, self.commands = 0, []
        from datetime import datetime, timezone
        self.started_at_utc = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def reserve(self, byte_count):
        if self.used + byte_count >= self.limit:
            raise ContractError("LIMIT_EXCEEDED", "Aggregate evidence cap reached; retain incomplete diagnostics.", "evidence")
        self.used += byte_count

    def run(self, argv, name, stdout_limit=MAX_JSON, failure_code="PROBE_FAILED", failure_status="BLOCKED"):
        self.used = sum(p.stat().st_size for p in self.directory.iterdir() if p.is_file())
        out, err = self.directory / (name + ".stdout"), self.directory / (name + ".stderr")
        command = {"argv": [str(x) for x in argv], "exit_code": None, "timed_out": False,
                   "output_truncated": False, "stdout_path": out.name, "stderr_path": err.name}
        self.commands.append(command)
        try:
            process = subprocess.Popen(command["argv"], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError as exc:
            err.write_text(str(exc) + "\n")
            out.touch()
            raise ContractError("TOOL_UNAVAILABLE", "Command could not start; inspect local stderr.", name) from exc
        start = time.monotonic()
        counts = {"stdout": 0, "stderr": 0}
        exceeded = False
        with out.open("xb") as of, err.open("xb") as ef, selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ, ("stdout", of, stdout_limit))
            selector.register(process.stderr, selectors.EVENT_READ, ("stderr", ef, LOG_LIMIT))
            try:
                while selector.get_map():
                    if time.monotonic() - start >= self.timeout:
                        command["timed_out"] = True
                        process.kill()
                        break
                    for key, _ in selector.select(timeout=0.1):
                        channel, f, cap = key.data
                        chunk = os.read(key.fd, 65536)
                        if not chunk:
                            selector.unregister(key.fileobj)
                            continue
                        remaining = min(cap - counts[channel], self.limit - self.used)
                        keep = chunk[:max(0, remaining)]
                        f.write(keep)
                        counts[channel] += len(keep)
                        self.used += len(keep)
                        if len(keep) != len(chunk) or counts[channel] >= cap or self.used >= self.limit:
                            command["output_truncated"] = exceeded = True
                            process.kill()
                            break
                    if exceeded:
                        break
                command["exit_code"] = process.wait()
                of.flush(); ef.flush()
                os.fsync(of.fileno()); os.fsync(ef.fileno())
            finally:
                if process.poll() is None:
                    process.kill(); process.wait()
                process.stdout.close(); process.stderr.close()
        if exceeded:
            raise ContractError("LIMIT_EXCEEDED", "Evidence/log cap reached; output is incomplete.", name)
        if command["timed_out"]:
            raise ContractError("TOOL_TIMEOUT", "Command timed out; retain diagnostics and retry explicitly after investigation.", name)
        if command["exit_code"] != 0:
            raise ContractError(failure_code, "Command failed; inspect retained stderr.", name, failure_status)
        return out, err


class Findings:
    def __init__(self):
        self.items = {}

    def add(self, code, field, action, status="BLOCKED"):
        self.items[code, field] = (status, {"code": code, "field": field, "action": action})

    def result(self):
        ranks = {"READY": 0, "NEEDS_REVIEW": 1, "BLOCKED": 2, "INVALID": 3}
        status = max((v[0] for v in self.items.values()), key=ranks.get, default="READY")
        return {"status": status, "reasons": [self.items[k][1] for k in sorted(self.items)]}


def number(value, positive=False):
    try:
        f = Fraction(str(value).replace(":", "/"))
        return rational(f) if not positive or f > 0 else None
    except (ValueError, ZeroDivisionError):
        return None


def integer(value, positive=False):
    if isinstance(value, bool) or not re.fullmatch(r"[0-9]+", str(value)):
        return None
    v = int(value)
    return v if int(positive) <= v <= MAX_INTEGER else None


def ticks(value):
    return str(value) if re.fullmatch(r"0|-?[1-9][0-9]*", str(value)) else None


def text(value):
    return value if isinstance(value, str) and value and value not in {"unknown", "N/A", "und"} else None


def normalized_streams(probe):
    result = []
    for s in probe.get("streams", []):
        index = integer(s.get("index"))
        if index is None:
            raise ContractError("PROBE_INVALID", "Stream indexes must be known nonnegative integers.")
        typ = s.get("codec_type")
        typ = typ if typ in {"video", "audio", "data", "subtitle", "attachment"} else "unknown"
        row = {"index": index, "type": typ, "codec": text(s.get("codec_name")),
               "time_base_s": number(s.get("time_base"), True), "start_pts": ticks(s.get("start_pts")),
               "reported_start_s": number(s.get("start_time")), "reported_duration_s": number(s.get("duration"), True),
               "duration_ticks": ticks(s.get("duration_ts")), "video": None, "audio": None}
        if typ == "video":
            matrices = [x for x in s.get("side_data_list", []) if x.get("side_data_type") == "Display Matrix"]
            m = matrices[0] if len(matrices) == 1 else {}
            attached = s.get("disposition", {}).get("attached_pic")
            row["video"] = {"width": integer(s.get("width"), True), "height": integer(s.get("height"), True),
                "pixel_format": text(s.get("pix_fmt")), "sar": number(s.get("sample_aspect_ratio"), True),
                "dar_reported": number(s.get("display_aspect_ratio"), True), "r_frame_rate": number(s.get("r_frame_rate"), True),
                "avg_frame_rate": number(s.get("avg_frame_rate"), True),
                "attached_picture": bool(attached) if type(attached) is int and attached in {0, 1} else None,
                "rotation_reported_deg": str(m["rotation"]) if number(m.get("rotation")) is not None else None,
                "rotation_tag_deg": str(s["tags"]["rotate"]) if number(s.get("tags", {}).get("rotate")) is not None else None,
                "display_matrix": text(m.get("displaymatrix"))}
        elif typ == "audio":
            row["audio"] = {"sample_rate_hz": integer(s.get("sample_rate"), True), "channels": integer(s.get("channels"), True),
                "channel_layout": text(s.get("channel_layout")), "sample_format": text(s.get("sample_fmt")),
                "bits_per_sample": integer(s.get("bits_per_sample"), True)}
        result.append(row)
    result.sort(key=lambda x: x["index"])
    return result


def select_streams(streams, probe, options, findings):
    selection = {"video_index": None, "audio_index": None, "basis": {"video": "UNRESOLVED", "audio": "UNRESOLVED"}}
    raw = {s["index"]: s for s in probe.get("streams", [])}
    for typ in ("video", "audio"):
        candidates = []
        unknown_eligibility = False
        for s in streams:
            if s["type"] != typ:
                continue
            if typ == "video":
                disposition = raw[s["index"]].get("disposition", {})
                if s["video"]["attached_picture"] is None:
                    unknown_eligibility = True
                    continue
                if s["video"]["attached_picture"] or any(disposition.get(k) == 1 for k in ("timed_thumbnails", "still_image")):
                    continue
            candidates.append(s["index"])
        chosen = options[typ + "_index"]
        if chosen is not None:
            if chosen not in candidates:
                findings.add("INVALID_STREAM_SELECTION", typ, "Select an eligible stream index of the correct type.", "INVALID")
            else:
                selection[typ + "_index"] = chosen
                selection["basis"][typ] = "USER_SELECTED"
        elif unknown_eligibility:
            findings.add("CANDIDACY_UNKNOWN", typ, "Video eligibility is not established; inspect dispositions.")
        elif not candidates:
            findings.add("NO_" + typ.upper(), typ, "Provide a source containing usable video and integrated audio.", "INVALID")
        elif len(candidates) > 1:
            findings.add("SELECT_" + typ.upper(), typ, "Choose an explicit stream index; defaults do not identify voice/content.", "NEEDS_REVIEW")
        else:
            selection[typ + "_index"] = candidates[0]
            selection["basis"][typ] = "UNIQUE_CANDIDATE"
    return selection


def matrix_angle(matrix):
    try:
        rows = [list(map(int, line.split(":", 1)[1].split())) for line in matrix.splitlines() if ":" in line]
        if len(rows) != 3 or any(len(r) != 3 for r in rows):
            return None
        a, b, u, c, d, v, x, y, w = sum(rows, [])
        if (u, v, w) != (0, 0, 1 << 30):
            return None
        unit = 1 << 16
        return {(unit, 0, 0, unit): 0, (0, unit, -unit, 0): -90,
                (-unit, 0, 0, -unit): 180, (0, -unit, unit, 0): 90}.get((a, b, c, d))
    except (ValueError, AttributeError):
        return None


def quarter_angle(value):
    n = number(value)
    if n is None or Fraction(n) % 90:
        return None
    v = int(Fraction(n)) % 360
    return -90 if v == 270 else v


def display_properties(video, options, findings):
    d = {"transform_basis": "UNRESOLVED", "rotation_to_apply_deg": None, "raster_axis_width": None,
         "raster_axis_height": None, "square_pixel_width": None, "square_pixel_height": None,
         "aspect": None, "geometry": "UNKNOWN"}
    if video is None:
        return d
    v = video["video"]
    angle, basis, conflict = 0, "NO_ROTATION_DECLARED", False
    if v["display_matrix"] is not None:
        angle, basis = matrix_angle(v["display_matrix"]), "MATRIX"
        reported = quarter_angle(v["rotation_reported_deg"])
        conflict = angle is None or (v["rotation_reported_deg"] is not None and angle != reported)
    elif v["rotation_reported_deg"] is not None:
        angle, basis = quarter_angle(v["rotation_reported_deg"]), "MATRIX"
        conflict = True  # angle alone cannot exclude reflection/scale in a missing matrix
    if v["rotation_tag_deg"] is not None:
        # Legacy rotate tag is clockwise; display-matrix angle is counterclockwise.
        tag_angle = quarter_angle(-Fraction(v["rotation_tag_deg"]))
        if basis == "NO_ROTATION_DECLARED":
            angle, basis = tag_angle, "TAG"
            conflict = tag_angle is None
        elif tag_angle != angle:
            conflict = True
    override = options["display_rotation_override_deg"]
    if override is not None:
        angle, basis, conflict = override, "USER_OVERRIDE", False
    if conflict:
        findings.add("DISPLAY_TRANSFORM_UNRESOLVED", "display", "Review conflicting/unsupported display transform; record an explicit view override.", "NEEDS_REVIEW")
        return d
    if any(v[k] is None for k in ("width", "height", "sar")) or angle is None:
        findings.add("DISPLAY_GEOMETRY_UNKNOWN", "display", "Raster/SAR/view transform must be established without guessing.", "NEEDS_REVIEW")
        return d
    width, height = Fraction(v["width"]) * Fraction(v["sar"]), Fraction(v["height"])
    if v["dar_reported"] is not None and Fraction(v["dar_reported"]) != width / height:
        findings.add("DISPLAY_ASPECT_CONFLICT", "display.aspect", "Reported DAR disagrees with raster/SAR; investigate.", "NEEDS_REVIEW")
    rw, rh = v["width"], v["height"]
    if angle in {-90, 90}:
        width, height, rw, rh = height, width, rh, rw
    geometry = "PORTRAIT" if width < height else "LANDSCAPE" if width > height else "SQUARE"
    d.update(transform_basis=basis, rotation_to_apply_deg=angle, raster_axis_width=rw, raster_axis_height=rh,
             square_pixel_width=rational(width), square_pixel_height=rational(height), aspect=rational(width / height), geometry=geometry)
    if geometry != "PORTRAIT":
        findings.add("DISPLAY_NOT_VERTICAL", "display.geometry", "Review view orientation; no crop or normalization is performed.", "NEEDS_REVIEW")
    return d


def scan_frames(path, stream, tsv, budget=None):
    """Read compact rows incrementally; retain real PTS, never best-effort/FPS substitutes."""
    count, first, last, max_end, first_delta, max_delta = 0, None, None, None, None, None
    known, varying, errors, max_duration = True, False, set(), 0
    with Path(path).open() as source:
        for line in source:
            fields = dict(part.split("=", 1) for part in line.strip().split("|") if "=" in part)
            if "stream_index" not in fields:
                continue
            if integer(fields["stream_index"]) != stream["index"]:
                errors.add("STREAM_INDEX_MISMATCH")
                continue
            pts, duration = ticks(fields.get("pts")), ticks(fields.get("duration"))
            row = f"{stream['index']}\t{pts or 'UNKNOWN'}\t{duration or 'UNKNOWN'}\t{stream['time_base_s'] or 'UNKNOWN'}\n"
            if budget is not None:
                budget.reserve(len(row.encode()))
            tsv.write(row)
            count += 1
            if pts is None:
                errors.add("MISSING_PTS")
                continue
            p = int(pts)
            if first is None:
                first = p
            if last is not None:
                delta = p - last
                if delta <= 0:
                    errors.add("NONMONOTONIC_PTS")
                elif first_delta is None:
                    first_delta = delta
                elif delta != first_delta:
                    varying = True
                max_delta = max(max_delta or 0, delta)
            last = p
            if duration is None or int(duration) <= 0:
                known = False
            else:
                max_duration = max(max_duration, int(duration))
                max_end = max(max_end if max_end is not None else p, p + int(duration))
    return {"count": count, "first_pts": str(first) if first is not None else None,
            "last_pts": str(last) if last is not None else None, "max_end_pts": str(max_end) if known and max_end is not None else None,
            "max_delta_pts": str(max_delta) if max_delta is not None else None, "max_duration_ticks": str(max_duration),
            "time_base_s": stream["time_base_s"], "cadence": "UNKNOWN" if count < 2 else "VARYING" if varying else "UNIFORM",
            "errors": sorted(errors)}


def timing_properties(video, audio, summaries, source_id, container, findings):
    t = {"clock": "source-presentation-v1", "origin_video_pts": None, "origin_time_base_s": None,
         "origin_media_s": None, "clock_id": None, "video_start_s": None, "video_end_s": None,
         "audio_start_s": None, "audio_end_s": None, "extent_basis": {"video": "UNKNOWN", "audio": "UNKNOWN"},
         "cadence": "UNKNOWN", "frame_count": 0, "audio_frame_count": 0}
    if video is None or audio is None:
        return t
    for stream in (video, audio):
        summary = summaries.get(stream["index"])
        if summary is None:
            return t
        t["frame_count" if stream["type"] == "video" else "audio_frame_count"] = summary["count"]
        if not summary["count"]:
            findings.add("EMPTY_STREAM", stream["type"], "No presented frames were decoded.", "INVALID")
        if summary["errors"] or summary["first_pts"] is None or stream["time_base_s"] is None:
            findings.add("TIMING_UNKNOWN", stream["type"], "PTS/time base is missing or nonmonotonic; no inferred timing allowed.")
    vs, aus = summaries[video["index"]], summaries[audio["index"]]
    if any(x["errors"] or x["first_pts"] is None for x in (vs, aus)) or any(s["time_base_s"] is None for s in (video, audio)):
        return t
    origin = int(vs["first_pts"]) * Fraction(video["time_base_s"])
    t.update(origin_video_pts=vs["first_pts"], origin_time_base_s=video["time_base_s"], origin_media_s=rational(origin),
             video_start_s="0/1", cadence=vs["cadence"])
    t["clock_id"] = digest({"source_id": source_id, "video_index": video["index"], "origin_video_pts": t["origin_video_pts"],
                            "origin_time_base_s": t["origin_time_base_s"], "clock": t["clock"]})
    tolerance = max(int(vs["max_delta_pts"] or 0), int(vs["max_duration_ticks"])) * Fraction(video["time_base_s"])
    sr = audio["audio"]["sample_rate_hz"]
    if sr:
        tolerance = max(tolerance, Fraction(1, sr))
    for s, summary in ((video, vs), (audio, aus)):
        typ = s["type"]
        start = int(summary["first_pts"]) * Fraction(s["time_base_s"])
        t[typ + "_start_s"] = rational(start - origin)
        end_pts, basis = summary["max_end_pts"], "FRAME_EXTENTS"
        if end_pts is None and s["start_pts"] == summary["first_pts"] and s["duration_ticks"] is not None and int(s["duration_ticks"]) > 0:
            end_pts, basis = str(int(s["start_pts"]) + int(s["duration_ticks"])), "STREAM_DURATION"
        if end_pts is None or int(end_pts) <= int(summary["first_pts"]):
            findings.add("TIMING_UNKNOWN", typ + ".end", "No reliable frame extent or matching stream duration is available.")
            continue
        end = int(end_pts) * Fraction(s["time_base_s"])
        t[typ + "_end_s"], t["extent_basis"][typ] = rational(end - origin), basis
        if s["reported_duration_s"] is not None and abs(Fraction(s["reported_duration_s"]) - (end - start)) > tolerance:
            findings.add("DURATION_DISCREPANCY", typ, "Reported and presented stream duration disagree beyond the approved bound.", "NEEDS_REVIEW")
    if container["reported_duration_s"] is not None and t["video_end_s"] is not None and t["audio_end_s"] is not None:
        extent = max(Fraction(t["video_end_s"]), Fraction(t["audio_end_s"])) - min(Fraction(0), Fraction(t["audio_start_s"]))
        if abs(Fraction(container["reported_duration_s"]) - extent) > tolerance:
            findings.add("DURATION_DISCREPANCY", "container", "Container extent differs from selected AV; inspect extra streams/metadata.", "NEEDS_REVIEW")
    return t


def inspect_media(source, project, manifest_hash, directory, options, runner, versions,
                  ffprobe="ffprobe", ffmpeg="ffmpeg"):
    validate_options(options)
    findings = Findings()
    path, _ = runner.run([ffprobe, "-v", "error", "-protocol_whitelist", "file,pipe", "-show_format", "-show_streams", "-of", "json=string_validation=fail", str(source)], "probe")
    probe = load_json(path)
    if not isinstance(probe, dict) or not isinstance(probe.get("streams", []), list) or not isinstance(probe.get("format", {}), dict):
        raise ContractError("PROBE_INVALID", "Expected ffprobe object/streams/container structure.")
    for stream in probe.get("streams", []):
        if not isinstance(stream, dict) or any(not isinstance(stream.get(key, {}), dict) for key in ("tags", "disposition")) or not isinstance(stream.get("side_data_list", []), list) or any(not isinstance(s, dict) for s in stream.get("side_data_list", [])):
            raise ContractError("PROBE_INVALID", "Malformed stream metadata structure.")
    runner.reserve(len(canonical_bytes(probe)))
    atomic_json(Path(directory) / "ffprobe.json", probe)
    streams = normalized_streams(probe)
    selection = select_streams(streams, probe, options, findings)
    chosen = {typ: next((s for s in streams if s["index"] == selection[typ + "_index"]), None) for typ in ("video", "audio")}
    if chosen["video"] is not None and options["display_rotation_override_deg"] is None:
        raw_video = next(s for s in probe["streams"] if s["index"] == chosen["video"]["index"])
        if sum(s.get("side_data_type") == "Display Matrix" for s in raw_video.get("side_data_list", [])) > 1:
            findings.add("DISPLAY_TRANSFORM_UNRESOLVED", "display", "Multiple display matrices require explicit review.", "NEEDS_REVIEW")
    for typ, s in chosen.items():
        if s is None:
            continue
        keys = ("width", "height", "sar") if typ == "video" else ("sample_rate_hz", "channels")
        if s["codec"] is None or s["time_base_s"] is None or any(s[typ][k] is None for k in keys):
            findings.add("REQUIRED_PROPERTY_UNKNOWN", typ, "Selected codec, time base and required media properties must be known.")
    c = probe.get("format", {})
    container = {"format_names": str(c["format_name"]).split(",") if c.get("format_name") else [],
                 "reported_start_s": number(c.get("start_time")), "reported_duration_s": number(c.get("duration"), True)}
    display = display_properties(chosen["video"], options, findings)
    summaries = {}
    if all(chosen.values()) and not any(status in {"INVALID", "BLOCKED"} for status, _ in findings.items.values()):
        _, error_log = runner.run([ffmpeg, "-nostdin", "-hide_banner", "-v", "error", "-xerror", "-err_detect", "explode", "-protocol_whitelist", "file,pipe", "-noautorotate", "-i", str(source),
            "-map", "0:" + str(selection["video_index"]), "-map", "0:" + str(selection["audio_index"]), "-f", "null", "-"], "decode", failure_code="DECODE_FAILED", failure_status="INVALID")
        if error_log.stat().st_size:
            findings.add("DECODE_FAILED", "decode", "Decoder reported errors despite a successful exit; inspect log.", "INVALID")
        with (Path(directory) / "frames.tsv").open("x") as tsv:
            header = "stream_index\tpts\tduration_ticks\ttime_base_s\n"
            runner.reserve(len(header.encode())); tsv.write(header)
            for typ in ("video", "audio"):
                s = chosen[typ]
                frame_path, _ = runner.run([ffprobe, "-v", "error", "-protocol_whitelist", "file,pipe", "-select_streams", str(s["index"]), "-show_frames", "-show_entries", "frame=stream_index,pts,duration", "-of", "compact=p=0:nk=0", str(source)], "frames-" + str(s["index"]), stdout_limit=EVIDENCE_LIMIT)
                summaries[s["index"]] = scan_frames(frame_path, s, tsv, runner)
            tsv.flush(); os.fsync(tsv.fileno())
    timing = timing_properties(chosen["video"], chosen["audio"], summaries, project["source"]["id"], container, findings)
    summary_document = {"schema_version": 1, "kind": "media-timing-summary", "streams": {str(k): v for k, v in summaries.items()}, "timing": timing}
    runner.reserve(len(canonical_bytes(summary_document)))
    atomic_json(Path(directory) / "timing-summary.json", summary_document)
    doc = {"schema_version": 1, "kind": "media-inspection", "project_id": project["project_id"], "source_id": project["source"]["id"],
           "source_sha256": project["source"]["sha256"], "project_manifest_sha256": manifest_hash,
           "inspector_version": inspector_version(), "tool_versions": versions, "container": container, "streams": streams,
           "selection": selection, "display": display, "timing": timing, "options": options, "readiness": findings.result(), "unknowns": {}, "extensions": {}}
    doc["unknowns"] = unknown_fields(doc)
    # Distinguish malformed reported values from fields the tool did not report.
    raw_by_index = {s["index"]: s for s in probe.get("streams", [])}
    for n, s in enumerate(streams):
        raw = raw_by_index[s["index"]]
        mappings = {"codec": "codec_name", "time_base_s": "time_base", "start_pts": "start_pts", "reported_duration_s": "duration", "duration_ticks": "duration_ts"}
        if s["type"] == "video":
            mappings.update({"video."+k: v for k,v in {"width":"width", "height":"height", "sar":"sample_aspect_ratio", "dar_reported":"display_aspect_ratio", "r_frame_rate":"r_frame_rate", "avg_frame_rate":"avg_frame_rate"}.items()})
        if s["type"] == "audio":
            mappings.update({"audio."+k: v for k,v in {"sample_rate_hz":"sample_rate", "channels":"channels"}.items()})
        for field, raw_key in mappings.items():
            path = f"streams.{n}.{field}"
            value = raw.get(raw_key)
            if path in doc["unknowns"] and value is not None and str(value) not in {"N/A", "unknown", "und", "0/0", "0:0", ""}:
                doc["unknowns"][path] = "INVALID_METADATA"
        if s["type"] == "video" and sum(x.get("side_data_type") == "Display Matrix" for x in raw.get("side_data_list", [])) > 1:
            for field in ("display_matrix", "rotation_reported_deg"):
                doc["unknowns"][f"streams.{n}.video.{field}"] = "AMBIGUOUS"
    validate_inspection(doc)
    return doc
