"""F002 v1 wire contracts and read-only integrity guard. Standard library only."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import uuid
from fractions import Fraction
from pathlib import Path

MAX_JSON = 16 * 1024 * 1024
MAX_INTEGER = 2**53 - 1
PROJECT_ID = re.compile(r"[a-z0-9][a-z0-9-]{0,63}\Z")
HASH = re.compile(r"[0-9a-f]{64}\Z")
STATES = {"READY", "NEEDS_REVIEW", "BLOCKED", "INVALID"}
UNKNOWN_REASONS = {"NOT_REPORTED", "NOT_PROVIDED", "INVALID_METADATA", "AMBIGUOUS", "UNSUPPORTED"}


class ContractError(Exception):
    def __init__(self, code, action, field="", status="BLOCKED"):
        super().__init__(action)
        self.code, self.action, self.field, self.status = code, action, field, status

    def reason(self):
        return {"code": self.code, "field": self.field, "action": self.action}


def canonical_bytes(value):
    return (json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def rational(value):
    f = Fraction(value)
    return f"{f.numerator}/{f.denominator}"


def stat_identity(path):
    s = Path(path).stat()
    return {"bytes": s.st_size, "mtime_ns": str(s.st_mtime_ns), "inode": str(s.st_ino), "device": str(s.st_dev)}


def hash_file(path):
    path = Path(path)
    before = stat_identity(path)
    if not path.is_file():
        raise ContractError("INPUT_NOT_REGULAR", "Use a regular local file.", str(path), "INVALID")
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(4 * 1024 * 1024):
            h.update(chunk)
    if before != stat_identity(path):
        raise ContractError("SOURCE_CHANGED", "File changed during hashing; investigate and recover the expected identity.", str(path))
    return h.hexdigest()


def _unique(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError(f"Duplicate JSON key: {k}")
        d[k] = v
    return d


def load_json(path):
    p = Path(path)
    if p.stat().st_size > MAX_JSON:
        raise ContractError("LIMIT_EXCEEDED", "JSON exceeds the 16 MiB limit.", str(p))
    try:
        return json.loads(p.read_text(encoding="utf-8"), object_pairs_hook=_unique,
                          parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    except (ValueError, UnicodeError) as exc:
        raise ContractError("INVALID_JSON", "JSON is malformed, duplicated or non-finite.", str(p)) from exc


def atomic_json(path, value):
    """Flush a sibling temporary file, replace atomically, flush the directory."""
    p = Path(path)
    if p.is_symlink():
        raise ContractError("UNSAFE_PATH", "Refuse to replace a symlink.", str(p))
    tmp = p.with_name(f".{p.name}.{uuid.uuid4().hex}.tmp")
    with tmp.open("xb") as f:
        f.write(canonical_bytes(value))
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, p)
    sync_directory(p.parent)


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def safe_path(root, relative):
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ContractError("UNSAFE_PATH", "Expected a nonempty project-relative path.")
    rel = Path(relative)
    if rel.is_absolute() or any(x in {"..", "."} for x in relative.split("/")):
        raise ContractError("UNSAFE_PATH", "Absolute paths and traversal are forbidden.", relative)
    root = Path(root).resolve()
    path = root / rel
    if not path.resolve().is_relative_to(root):
        raise ContractError("UNSAFE_PATH", "A symlink escapes the project.", relative)
    return path


def _bad(field, action="Invalid v1 contract value."):
    raise ContractError("CONTRACT_INVALID", action, field, "INVALID")


def _keys(obj, keys, field):
    if not isinstance(obj, dict) or set(obj) != set(keys.split()):
        _bad(field, "Missing or unexpected v1 core keys.")


def _string(v, field, nullable=False):
    if v is None and nullable:
        return
    if not isinstance(v, str) or not v:
        _bad(field)


def _int(v, field, nullable=False, positive=False):
    if v is None and nullable:
        return
    if type(v) is not int or not (int(positive) <= v <= MAX_INTEGER):
        _bad(field)


def _r(v, field, nullable=True, positive=False):
    if v is None and nullable:
        return
    try:
        if not isinstance(v, str) or rational(v) != v or (positive and Fraction(v) <= 0):
            _bad(field)
    except (ValueError, ZeroDivisionError, TypeError):
        _bad(field)


def _ticks(v, field):
    if v is not None and (not isinstance(v, str) or not re.fullmatch(r"0|-?[1-9][0-9]*", v)):
        _bad(field)


def _hash(v, field, nullable=False):
    if v is None and nullable:
        return
    if not isinstance(v, str) or not HASH.fullmatch(v):
        _bad(field)


def _walk(value, path=""):
    if isinstance(value, dict):
        for k, v in value.items():
            yield from _walk(v, f"{path}.{k}" if path else k)
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from _walk(v, f"{path}.{i}")
    else:
        yield path, value


def unknown_fields(doc, reason="NOT_REPORTED"):
    return {p: reason for p, v in _walk(doc) if v is None and not p.startswith(("unknowns.", "extensions."))}


def _common(doc, kind):
    if type(doc.get("schema_version")) is not int or doc["schema_version"] != 1 or doc.get("kind") != kind:
        raise ContractError("UNSUPPORTED_VERSION", "Use a supported kind/schema_version; do not assume compatibility.", "schema_version", "INVALID")
    if not isinstance(doc.get("project_id"), str) or not PROJECT_ID.fullmatch(doc["project_id"]):
        _bad("project_id")
    for path, v in _walk(doc):
        if isinstance(v, float) and (not math.isfinite(v) or not path.startswith("extensions.")):
            _bad(path, "Core values cannot be floating point.")
    if not isinstance(doc.get("unknowns"), dict) or any(v not in UNKNOWN_REASONS for v in doc["unknowns"].values()):
        _bad("unknowns")
    if not isinstance(doc.get("extensions"), dict) or any(not re.fullmatch(r"[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)+", k) for k in doc["extensions"]):
        _bad("extensions")
    nulls = unknown_fields(doc)
    if set(doc["unknowns"]) != set(nulls):
        _bad("unknowns", "Every core null needs a reason, without stale unknown entries.")


def _reasons(status, reasons):
    if status not in STATES or not isinstance(reasons, list) or (status == "READY") != (not reasons):
        _bad("readiness")
    for reason in reasons:
        _keys(reason, "code field action", "reasons")
        _string(reason["code"], "reasons.code")
        _string(reason["action"], "reasons.action")
        if not isinstance(reason["field"], str):
            _bad("reasons.field")
    if reasons != sorted(reasons, key=lambda x: (x["code"], x["field"])):
        _bad("reasons", "Reasons must be sorted by code/field.")


def validate_project(doc):
    _keys(doc, "schema_version kind project_id source capture_context references unknowns extensions", "project")
    _common(doc, "content-project-source")
    s = doc["source"]
    _keys(s, "id path bytes sha256 original_name original_path resolved_original_path ingested_at_utc", "source")
    _hash(s["sha256"], "source.sha256")
    _int(s["bytes"], "source.bytes", positive=True)
    if s["id"] != "sha256:" + s["sha256"] or s["path"] != "raw/source":
        _bad("source")
    for key in ("original_name", "original_path", "resolved_original_path", "ingested_at_utc"):
        _string(s[key], "source." + key)
    if Path(s["original_name"]).name != s["original_name"] or not all(Path(s[x]).is_absolute() for x in ("original_path", "resolved_original_path")):
        _bad("source.original_path")
    if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z", s["ingested_at_utc"]):
        _bad("source.ingested_at_utc")
    _keys(doc["capture_context"], "profile limitations", "capture_context")
    if doc["capture_context"]["profile"] not in {"STUDIO", "MOBILE", "UNKNOWN"}:
        _bad("capture_context.profile")
    if not isinstance(doc["capture_context"]["limitations"], list):
        _bad("capture_context.limitations")
    for x in doc["capture_context"]["limitations"]:
        _string(x, "capture_context.limitations")
    _keys(doc["references"], "fixture_id feature_revision recovery_location evidence_manifest_sha256", "references")
    for k, v in doc["references"].items():
        (_hash if k.endswith("sha256") else _string)(v, "references." + k, nullable=True)


def validate_options(options):
    _keys(options, "video_index audio_index display_rotation_override_deg override_reason override_reviewer", "options")
    for key in ("video_index", "audio_index"):
        _int(options[key], "options." + key, nullable=True)
    angle = options["display_rotation_override_deg"]
    if angle is not None and (type(angle) is not int or angle not in {0, 90, -90, 180}):
        _bad("options.display_rotation_override_deg")
    for key in ("override_reason", "override_reviewer"):
        _string(options[key], "options." + key, nullable=angle is None)
    if angle is None and any(options[x] is not None for x in ("override_reason", "override_reviewer")):
        _bad("options", "An override needs angle, reviewer and reason together.")


def validate_inspection(doc):
    _keys(doc, "schema_version kind project_id source_id source_sha256 project_manifest_sha256 inspector_version tool_versions container streams selection display timing options readiness unknowns extensions", "inspection")
    _common(doc, "media-inspection")
    for key in ("source_sha256", "project_manifest_sha256"):
        _hash(doc[key], key)
    if doc["source_id"] != "sha256:" + doc["source_sha256"]:
        _bad("source_id")
    _string(doc["inspector_version"], "inspector_version")
    _keys(doc["tool_versions"], "ffprobe ffmpeg", "tool_versions")
    for k, v in doc["tool_versions"].items():
        _string(v, "tool_versions." + k)
    _keys(doc["container"], "format_names reported_start_s reported_duration_s", "container")
    if not isinstance(doc["container"]["format_names"], list):
        _bad("container.format_names")
    for name in doc["container"]["format_names"]:
        _string(name, "container.format_names")
    _r(doc["container"]["reported_start_s"], "container.reported_start_s")
    _r(doc["container"]["reported_duration_s"], "container.reported_duration_s", positive=True)
    if not isinstance(doc["streams"], list):
        _bad("streams")
    indexes = []
    for s in doc["streams"]:
        _keys(s, "index type codec time_base_s start_pts reported_start_s reported_duration_s duration_ticks video audio", "stream")
        _int(s["index"], "streams.index")
        indexes.append(s["index"])
        if s["type"] not in {"video", "audio", "data", "subtitle", "attachment", "unknown"}:
            _bad("streams.type")
        _string(s["codec"], "streams.codec", True)
        _r(s["time_base_s"], "streams.time_base_s", positive=True)
        for key in ("start_pts", "duration_ticks"):
            _ticks(s[key], "streams." + key)
        _r(s["reported_start_s"], "streams.reported_start_s")
        _r(s["reported_duration_s"], "streams.reported_duration_s", positive=True)
        v, a = s["video"], s["audio"]
        if s["type"] == "video":
            _keys(v, "width height pixel_format sar dar_reported r_frame_rate avg_frame_rate attached_picture rotation_reported_deg rotation_tag_deg display_matrix", "video")
            for key in ("width", "height"):
                _int(v[key], "video." + key, True, True)
            for key in ("sar", "dar_reported", "r_frame_rate", "avg_frame_rate"):
                _r(v[key], "video." + key, positive=True)
            for key in ("pixel_format", "display_matrix", "rotation_reported_deg", "rotation_tag_deg"):
                _string(v[key], "video." + key, True)
            if v["attached_picture"] is not None and type(v["attached_picture"]) is not bool:
                _bad("video.attached_picture")
            if a is not None:
                _bad("streams.audio")
        elif s["type"] == "audio":
            _keys(a, "sample_rate_hz channels channel_layout sample_format bits_per_sample", "audio")
            for key in ("sample_rate_hz", "channels", "bits_per_sample"):
                _int(a[key], "audio." + key, True, True)
            for key in ("channel_layout", "sample_format"):
                _string(a[key], "audio." + key, True)
            if v is not None:
                _bad("streams.video")
        elif a is not None or v is not None:
            _bad("streams")
    if indexes != sorted(set(indexes)):
        _bad("streams.index", "Stream indexes must be unique and ordered.")
    _keys(doc["selection"], "video_index audio_index basis", "selection")
    _keys(doc["selection"]["basis"], "video audio", "selection.basis")
    for typ in ("video", "audio"):
        i = doc["selection"][typ + "_index"]
        _int(i, "selection." + typ, True)
        if doc["selection"]["basis"][typ] not in {"UNIQUE_CANDIDATE", "USER_SELECTED", "UNRESOLVED"}:
            _bad("selection.basis")
        if i is not None and not any(s["index"] == i and s["type"] == typ for s in doc["streams"]):
            _bad("selection")
    d = doc["display"]
    _keys(d, "transform_basis rotation_to_apply_deg raster_axis_width raster_axis_height square_pixel_width square_pixel_height aspect geometry", "display")
    if d["transform_basis"] not in {"MATRIX", "TAG", "NO_ROTATION_DECLARED", "USER_OVERRIDE", "UNRESOLVED"} or d["geometry"] not in {"PORTRAIT", "LANDSCAPE", "SQUARE", "UNKNOWN"}:
        _bad("display")
    if d["rotation_to_apply_deg"] is not None and (type(d["rotation_to_apply_deg"]) is not int or d["rotation_to_apply_deg"] not in {0, -90, 90, 180}):
        _bad("display.rotation_to_apply_deg")
    for key in ("raster_axis_width", "raster_axis_height"):
        _int(d[key], "display." + key, True, True)
    for key in ("square_pixel_width", "square_pixel_height", "aspect"):
        _r(d[key], "display." + key, positive=True)
    t = doc["timing"]
    _keys(t, "clock origin_video_pts origin_time_base_s origin_media_s clock_id video_start_s video_end_s audio_start_s audio_end_s extent_basis cadence frame_count audio_frame_count", "timing")
    if t["clock"] != "source-presentation-v1" or t["cadence"] not in {"UNIFORM", "VARYING", "UNKNOWN"}:
        _bad("timing")
    _ticks(t["origin_video_pts"], "timing.origin_video_pts")
    _hash(t["clock_id"], "timing.clock_id", True)
    for key in ("origin_time_base_s", "origin_media_s", "video_start_s", "video_end_s", "audio_start_s", "audio_end_s"):
        _r(t[key], "timing." + key)
    _keys(t["extent_basis"], "video audio", "timing.extent_basis")
    if any(x not in {"FRAME_EXTENTS", "STREAM_DURATION", "UNKNOWN"} for x in t["extent_basis"].values()):
        _bad("timing.extent_basis")
    for key in ("frame_count", "audio_frame_count"):
        _int(t[key], "timing." + key)
    validate_options(doc["options"])
    _keys(doc["readiness"], "status reasons", "readiness")
    _reasons(**doc["readiness"])
    if doc["readiness"]["status"] == "READY":
        if d["geometry"] != "PORTRAIT" or any(x is None for x in d.values()) or any(t[x] is None for x in ("origin_video_pts", "origin_time_base_s", "origin_media_s", "clock_id", "video_start_s", "video_end_s", "audio_start_s", "audio_end_s")):
            _bad("readiness", "READY requires resolved display and exact clock.")
        if t["video_start_s"] != "0/1" or Fraction(t["video_end_s"]) <= 0 or Fraction(t["audio_end_s"]) <= Fraction(t["audio_start_s"]) or min(t["frame_count"], t["audio_frame_count"]) < 1:
            _bad("timing", "READY requires populated positive stream extents.")
        for typ in ("video", "audio"):
            index = doc["selection"][typ + "_index"]
            s = next((s for s in doc["streams"] if s["index"] == index), None)
            if s is None or s["codec"] is None or s["time_base_s"] is None:
                _bad("selection", "READY needs selected usable AV streams.")
            keys = ("width", "height", "sar") if typ == "video" else ("sample_rate_hz", "channels")
            if any(s[typ][k] is None for k in keys):
                _bad(typ)
        clock = {"source_id": doc["source_id"], "video_index": doc["selection"]["video_index"], "origin_video_pts": t["origin_video_pts"], "origin_time_base_s": t["origin_time_base_s"], "clock": t["clock"]}
        if digest(clock) != t["clock_id"] or Fraction(t["origin_video_pts"]) * Fraction(t["origin_time_base_s"]) != Fraction(t["origin_media_s"]):
            _bad("timing.clock_id")


def validate_current(doc):
    _keys(doc, "schema_version kind project_id source_id status reasons inspection_path inspection_sha256 execution_path execution_sha256 project_manifest_sha256 artifact_hashes unknowns extensions", "current")
    _common(doc, "current-media-inspection")
    _reasons(doc["status"], doc["reasons"])
    _string(doc["source_id"], "source_id")
    _hash(doc["project_manifest_sha256"], "project_manifest_sha256")
    for key in ("inspection_sha256", "execution_sha256"):
        _hash(doc[key], key, True)
    for key in ("inspection_path", "execution_path"):
        _string(doc[key], key, True)
    if not isinstance(doc["artifact_hashes"], dict):
        _bad("artifact_hashes")
    for key, h in doc["artifact_hashes"].items():
        _hash(h, key)
    if doc["status"] == "READY" and any(doc[k] is None for k in ("inspection_path", "inspection_sha256", "execution_path", "execution_sha256")):
        _bad("current", "READY cannot point to incomplete work.")


def verify_project(root):
    """Return domain input only after fresh content/revision checks, without mutation."""
    root = Path(root).resolve()
    project = load_json(safe_path(root, "project.json"))
    validate_project(project)
    manifest_hash = hash_file(root / "project.json")
    source = safe_path(root, project["source"]["path"])
    if source.is_symlink() or source.stat().st_size != project["source"]["bytes"] or hash_file(source) != project["source"]["sha256"]:
        raise ContractError("SOURCE_CHANGED", "Restore expected source bytes after explicit recovery review.", "source")
    current = load_json(safe_path(root, "current.json"))
    validate_current(current)
    for key in ("project_id", "source_id"):
        expected = project["project_id"] if key == "project_id" else project["source"]["id"]
        if current[key] != expected:
            raise ContractError("BINDING_MISMATCH", "Current revision belongs to another source/project.", key)
    if current["project_manifest_sha256"] != manifest_hash:
        raise ContractError("MANIFEST_CHANGED", "Source manifest identity changed; do not reuse old approval.", "project.json")
    if current["inspection_path"] is None or current["execution_path"] is None:
        raise ContractError("INSPECTION_INCOMPLETE", "Run explicit inspect after resolving the recorded failure.", "current.json")
    cached = {"raw/source": project["source"]["sha256"], "project.json": manifest_hash}
    for rel, expected in current["artifact_hashes"].items():
        actual = cached.get(rel) or hash_file(safe_path(root, rel))
        if actual != expected:
            raise ContractError("ARTIFACT_CHANGED", "Regenerate derived metadata with explicit inspect.", rel)
    for typ in ("inspection", "execution"):
        rel = current[typ + "_path"]
        if hash_file(safe_path(root, rel)) != current[typ + "_sha256"]:
            raise ContractError("ARTIFACT_CHANGED", "Regenerate derived metadata with explicit inspect.", rel)
    inspection = load_json(safe_path(root, current["inspection_path"]))
    validate_inspection(inspection)
    execution = load_json(safe_path(root, current["execution_path"]))
    required = "schema_version kind project_id run_id source_id project_manifest_sha256 started_at_utc finished_at_utc completed status reasons options versions commands integrity artifact_hashes"
    _keys(execution, required, "execution")
    if type(execution["schema_version"]) is not int or execution["schema_version"] != 1 or execution["kind"] != "media-inspection-execution" or execution["completed"] is not True or not execution["finished_at_utc"]:
        raise ContractError("INSPECTION_INCOMPLETE", "Execution is not complete.", "execution")
    _reasons(execution["status"], execution["reasons"])
    if not isinstance(execution["commands"], list):
        _bad("execution.commands")
    for command in execution["commands"]:
        _keys(command, "argv exit_code timed_out output_truncated stdout_path stderr_path", "command")
        if not isinstance(command["argv"], list) or not command["argv"] or any(not isinstance(x, str) for x in command["argv"]):
            _bad("command.argv")
        if type(command["timed_out"]) is not bool or type(command["output_truncated"]) is not bool:
            _bad("command")
        if execution["status"] == "READY" and (type(command["exit_code"]) is not int or command["exit_code"] != 0 or command["timed_out"] or command["output_truncated"]):
            raise ContractError("INSPECTION_INCOMPLETE", "READY cannot include failed/timed-out/truncated commands.", "commands")
        for key in ("stdout_path", "stderr_path"):
            safe_path(root, command[key])
            if command[key] not in execution["artifact_hashes"]:
                raise ContractError("INSPECTION_INCOMPLETE", "Command evidence is missing from the manifest.", key)
    if execution["status"] == "READY":
        prefix = str(Path(current["inspection_path"]).parent) + "/"
        required_artifacts = {prefix+x for x in ("inspection.json", "ffprobe.json", "timing-summary.json", "frames.tsv", "decode.log", "report.md")}
        if len(execution["commands"]) < 4 or not required_artifacts.issubset(execution["artifact_hashes"]):
            raise ContractError("INSPECTION_INCOMPLETE", "Full probe/decode/timing evidence is required.", "artifact_hashes")
    for doc in (inspection, execution):
        if doc["project_id"] != project["project_id"] or doc["source_id"] != project["source"]["id"] or doc["project_manifest_sha256"] != manifest_hash:
            raise ContractError("BINDING_MISMATCH", "Artifacts must bind to this source and manifest.")
    if inspection["source_sha256"] != project["source"]["sha256"] or inspection["readiness"]["status"] != current["status"] or execution["status"] != current["status"]:
        raise ContractError("BINDING_MISMATCH", "Readiness or source hashes disagree.")
    for rel, expected in execution["artifact_hashes"].items():
        if current["artifact_hashes"].get(rel) != expected:
            raise ContractError("BINDING_MISMATCH", "Current and execution artifact manifests disagree.", rel)
    if current["status"] != "READY":
        raise ContractError("INPUT_NOT_READY", "Resolve recorded inspection reasons before consumption.", "readiness", current["status"])
    return project, current, inspection
