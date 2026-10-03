from __future__ import annotations

import copy
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from support_media import ROOT, contract, fixture, fresh_probe, read_inspection
import ingest
import media_inspection as media


class MediaTests(unittest.TestCase):
    def setUp(self):
        parent = ROOT / ".local/validation/F002/tests"; parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.base = Path(self.temp.name)

    def tearDown(self): self.temp.cleanup()

    def run_fixture(self, kind, **kwargs):
        out = ingest.ingest(fixture(kind), kind.replace("_", "-").replace("-90", "minus90"), self.base, **kwargs)
        return out, read_inspection(out["project_path"])

    def test_missing_and_multiple_streams(self):
        for kind, status, code in (("audio_only", "INVALID", "NO_VIDEO"), ("video_only", "INVALID", "NO_AUDIO"),
                                   ("multi_video", "NEEDS_REVIEW", "SELECT_VIDEO"), ("multi_audio", "NEEDS_REVIEW", "SELECT_AUDIO")):
            with self.subTest(kind=kind):
                out, doc = self.run_fixture(kind)
                self.assertEqual(out["status"], status)
                self.assertIn(code, [x["code"] for x in out["reasons"]])
                self.assertEqual(doc["timing"]["frame_count"], 0)
                if kind.startswith("multi"):
                    options = {"video_index": 1} if kind == "multi_video" else {"audio_index": 2}
                    selected = ingest.inspect_project(out["project_path"], options)
                    self.assertEqual(selected["status"], "READY")
                    self.assertEqual(read_inspection(out["project_path"])["selection"]["basis"]["video" if kind == "multi_video" else "audio"], "USER_SELECTED")
                    wrong = ingest.inspect_project(out["project_path"], {"video_index": 999})
                    self.assertEqual(wrong["status"], "INVALID")

    def test_attached_picture_is_not_main_video(self):
        out, doc = self.run_fixture("attached")
        self.assertEqual(out["status"], "READY")
        self.assertEqual(doc["selection"]["video_index"], 0)
        self.assertEqual(sum(s["type"] == "video" for s in doc["streams"]), 2)
        self.assertTrue(any(s["video"]["attached_picture"] for s in doc["streams"] if s["type"] == "video"))

    def test_unknown_eligibility_does_not_become_false(self):
        p = fresh_probe(fixture()); del p["streams"][0]["disposition"]
        streams = media.normalized_streams(p); f = media.Findings()
        media.select_streams(streams, p, ingest.default_options(), f)
        self.assertIsNone(streams[0]["video"]["attached_picture"])
        self.assertEqual(f.result()["status"], "BLOCKED")

    def test_optional_and_required_missing_metadata(self):
        original = fresh_probe(fixture())
        p = copy.deepcopy(original)
        p["streams"][1].pop("channel_layout", None)
        s = media.normalized_streams(p)
        self.assertIsNone(s[1]["audio"]["channel_layout"])
        for field, typ in (("codec_name", "video"), ("width", "video"), ("time_base", "video"), ("sample_rate", "audio"), ("channels", "audio")):
            with self.subTest(field=field):
                p = copy.deepcopy(original)
                index = 0 if typ == "video" else 1
                p["streams"][index].pop(field, None)
                def fake_probe(path): return p
                with patch("media_inspection.load_json", side_effect=fake_probe):
                    out = ingest.ingest(fixture(), "missing-" + field.replace("_", "-"), self.base)
                self.assertEqual(out["status"], "BLOCKED")

    def test_no_rotation_metadata_portrait_and_landscape(self):
        out, d = self.run_fixture("portrait")
        self.assertEqual(out["status"], "READY")
        self.assertEqual(d["display"]["transform_basis"], "NO_ROTATION_DECLARED")
        self.assertIsNone(d["streams"][0]["video"]["rotation_reported_deg"])
        out, d = self.run_fixture("landscape")
        self.assertEqual(out["status"], "NEEDS_REVIEW")
        self.assertEqual(d["display"]["geometry"], "LANDSCAPE")
        resolved = ingest.inspect_project(out["project_path"], {"display_rotation_override_deg": -90, "override_reason": "Synthetic view test only", "override_reviewer": "test"})
        self.assertEqual(resolved["status"], "READY")
        self.assertEqual(read_inspection(out["project_path"])["display"]["transform_basis"], "USER_OVERRIDE")

    def test_rotation_sign_against_actual_pixels(self):
        base = fixture("landscape")
        original = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(base), "-frames:v", "1", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"])
        w, h = 160, 90
        points = [(20, 20), (130, 20), (20, 65), (130, 65)]
        evidence = []
        for angle in (0, 90, -90, 180):
            out, doc = self.run_fixture("rotation_" + str(angle))
            displayed = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(fixture("rotation_" + str(angle))), "-frames:v", "1", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"])
            dw = h if abs(angle) == 90 else w
            self.assertEqual(doc["display"]["rotation_to_apply_deg"], angle)
            self.assertEqual(doc["display"]["raster_axis_width"], dw)
            self.assertEqual(out["status"], "READY" if abs(angle) == 90 else "NEEDS_REVIEW")
            for x, y in points:
                xx, yy = (y, w - 1 - x) if angle == 90 else (h - 1 - y, x) if angle == -90 else (w - 1 - x, h - 1 - y) if angle == 180 else (x, y)
                a, b = original[(y*w+x)*3:(y*w+x)*3+3], displayed[(yy*dw+xx)*3:(yy*dw+xx)*3+3]
                self.assertTrue(all(abs(i-j) <= 2 for i, j in zip(a, b)), (angle, a, b))
            evidence.append({"angle_ccw": angle, "display": doc["display"], "status": out["status"], "pixel_points_matched": points})
        (fixture("landscape").parent / "rotation-pixel-proof.json").write_bytes(contract.canonical_bytes(evidence))

    def test_non_square_sar(self):
        out, doc = self.run_fixture("sar")
        self.assertEqual(out["status"], "NEEDS_REVIEW")
        self.assertEqual(doc["display"]["square_pixel_width"], "180/1")
        self.assertEqual(doc["display"]["square_pixel_height"], "160/1")
        self.assertEqual(doc["display"]["aspect"], "9/8")

    def test_conflicts_and_unsupported_matrices(self):
        raw = media.normalized_streams(fresh_probe(fixture()))[0]
        examples = ["\n0: -65536 0 0\n1: 0 65536 0\n2: 0 0 1073741824\n",
                    "\n0: 131072 0 0\n1: 0 131072 0\n2: 0 0 1073741824\n",
                    "\n0: 65536 0 1\n1: 0 65536 0\n2: 0 0 1073741824\n"]
        for matrix in examples:
            with self.subTest(matrix=matrix):
                s = copy.deepcopy(raw); s["video"]["display_matrix"] = matrix
                f = media.Findings(); media.display_properties(s, ingest.default_options(), f)
                self.assertEqual(f.result()["status"], "NEEDS_REVIEW")
        s = copy.deepcopy(raw)
        s["video"].update(display_matrix="\n0: 0 65536 0\n1: -65536 0 0\n2: 0 0 1073741824\n", rotation_reported_deg="-90", rotation_tag_deg="-90")
        f = media.Findings(); media.display_properties(s, ingest.default_options(), f)
        self.assertEqual(f.result()["status"], "NEEDS_REVIEW")
        s["video"].update(display_matrix=None, rotation_reported_deg=None, rotation_tag_deg="90")
        f = media.Findings(); d = media.display_properties(s, ingest.default_options(), f)
        self.assertEqual(d["rotation_to_apply_deg"], -90)
        s["video"]["rotation_tag_deg"] = "45"
        f = media.Findings(); media.display_properties(s, ingest.default_options(), f)
        self.assertEqual(f.result()["status"], "NEEDS_REVIEW")

    def test_vfr_and_offset_independent_timing(self):
        evidence = []
        for kind in ("vfr", "offset", "bframes"):
            out, doc = self.run_fixture(kind)
            raw = fresh_probe(fixture(kind))
            starts, ends, deltas = {}, {}, []
            for typ in ("video", "audio"):
                s = next(s for s in raw["streams"] if s["codec_type"] == typ)
                frames = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", str(s["index"]), "-show_frames", "-show_entries", "frame=pts,duration", "-of", "json", str(fixture(kind))]))["frames"]
                base = Fraction(s["time_base"])
                starts[typ] = min(int(f["pts"]) for f in frames) * base
                ends[typ] = max((int(f["pts"]) + int(f["duration"])) * base for f in frames)
                if typ == "video":
                    deltas = [int(b["pts"])-int(a["pts"]) for a,b in zip(frames, frames[1:])]
            self.assertEqual(Fraction(doc["timing"]["origin_media_s"]), starts["video"])
            self.assertEqual(Fraction(doc["timing"]["audio_start_s"]), starts["audio"]-starts["video"])
            for typ in ("video", "audio"):
                self.assertEqual(Fraction(doc["timing"][typ + "_end_s"]), ends[typ]-starts["video"])
            if kind == "vfr":
                self.assertGreater(len(set(deltas)), 1)
                self.assertEqual(doc["timing"]["cadence"], "VARYING")
            if kind == "offset":
                self.assertGreater(starts["video"], 0)
                self.assertLess(Fraction(doc["timing"]["audio_start_s"]), 0)
            if kind == "bframes":
                packets = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_packets", "-show_entries", "packet=pts,dts", "-of", "json", str(fixture(kind))]))["packets"]
                self.assertTrue(any(p["pts"] != p["dts"] for p in packets if "dts" in p))
                self.assertEqual(doc["timing"]["cadence"], "UNIFORM")
            evidence.append({"fixture": kind, "status": out["status"], "timing": doc["timing"], "independent_starts": {k: str(v) for k,v in starts.items()}, "independent_ends": {k: str(v) for k,v in ends.items()}})
        (fixture().parent / "independent-time-proof.json").write_bytes(contract.canonical_bytes(evidence))

    def test_missing_pts_and_duration_fallback(self):
        s = media.normalized_streams(fresh_probe(fixture()))[0]
        for rows, expected in (("stream_index=0|duration=100\n", "MISSING_PTS"), ("stream_index=0|pts=1|duration=1\nstream_index=0|pts=1|duration=1\n", "NONMONOTONIC_PTS"), ("stream_index=0|pts=2|duration=1\nstream_index=0|pts=1|duration=1\n", "NONMONOTONIC_PTS")):
            p = self.base / "controlled.compact"; p.write_text(rows)
            with (self.base / "controlled.tsv").open("w") as tsv:
                summary = media.scan_frames(p, s, tsv)
            self.assertIn(expected, summary["errors"])
        streams = media.normalized_streams(fresh_probe(fixture()))
        video, audio = streams
        summary = {"count": 2, "first_pts": "-10", "last_pts": "0", "max_end_pts": None, "max_delta_pts": "10", "max_duration_ticks": "0", "cadence": "UNIFORM", "errors": []}
        video.update(start_pts="-10", duration_ticks="20", time_base_s="1/10", reported_duration_s="2/1")
        audio.update(start_pts="-10", duration_ticks="20", time_base_s="1/10", reported_duration_s="2/1")
        f = media.Findings()
        t = media.timing_properties(video, audio, {0: summary, 1: summary}, "sha256:" + "0"*64, {"reported_duration_s": None}, f)
        self.assertEqual(t["origin_media_s"], "-1/1")
        self.assertEqual(t["video_end_s"], "2/1")
        self.assertEqual(t["extent_basis"]["video"], "STREAM_DURATION")
        video["duration_ticks"] = None
        f = media.Findings(); t = media.timing_properties(video, audio, {0:summary,1:summary}, "sha256:"+"0"*64, {"reported_duration_s":None}, f)
        self.assertEqual(f.result()["status"], "BLOCKED")
        self.assertIsNone(t["video_end_s"])

    def test_tool_failure_and_evidence_limits(self):
        directory = self.base / "run"; directory.mkdir()
        r = media.Runner(directory)
        with self.assertRaises(contract.ContractError) as e: r.run(["/nonexistent/tool"], "missing")
        self.assertEqual(e.exception.code, "TOOL_UNAVAILABLE")
        r = media.Runner(directory)
        with self.assertRaises(contract.ContractError) as e: r.run([sys.executable, "-c", "raise SystemExit(7)"], "nonzero")
        self.assertEqual(e.exception.code, "PROBE_FAILED")
        r = media.Runner(directory, timeout=1)
        with self.assertRaises(contract.ContractError) as e: r.run([sys.executable, "-c", "import time; time.sleep(5)"], "timeout")
        self.assertEqual(e.exception.code, "TOOL_TIMEOUT")
        r = media.Runner(directory, limit=32)
        with self.assertRaises(contract.ContractError) as e: r.run([sys.executable, "-c", "print('x'*1024)"], "cap")
        self.assertEqual(e.exception.code, "LIMIT_EXCEEDED")
        self.assertTrue(r.commands[-1]["output_truncated"])

    def test_probe_and_decode_failure_during_reinspection(self):
        root = Path(ingest.ingest(fixture(), "failure-guard", self.base)["project_path"])
        original = media.Runner.run
        for mode, expected in (("missing_tool", "TOOL_UNAVAILABLE"), ("bad_json", "INVALID_JSON"), ("bad_shape", "PROBE_INVALID"), ("decode", "DECODE_FAILED")):
            def controlled(runner, argv, name, **kwargs):
                if mode == "missing_tool": raise contract.ContractError("TOOL_UNAVAILABLE", "Test double: missing tool")
                if mode in {"bad_json", "bad_shape"} and name == "probe":
                    p = runner.directory / "controlled.stdout"; p.write_text("{bad" if mode == "bad_json" else '{"streams":null}')
                    e = runner.directory / "controlled.stderr"; e.touch()
                    return p, e
                if mode == "decode" and name == "decode":
                    raise contract.ContractError("DECODE_FAILED", "Test double: decoder exit failure", "decode", "INVALID")
                return original(runner, argv, name, **kwargs)
            with self.subTest(mode=mode), patch.object(media.Runner, "run", controlled):
                out = ingest.inspect_project(root)
            self.assertNotEqual(out["status"], "READY")
            self.assertEqual(out["reasons"][0]["code"], expected)
            self.assertNotEqual(contract.load_json(root / "current.json")["status"], "READY")
        truncated = self.base / "truncated.mp4"; truncated.write_bytes(fixture().read_bytes()[:100])
        out = ingest.ingest(truncated, "truncated", self.base)
        self.assertNotEqual(out["status"], "READY")

    def test_malformed_metadata_reasons_and_multiple_matrices(self):
        p = fresh_probe(fixture())
        p["streams"][0]["width"] = "not-a-number"
        with patch("media_inspection.load_json", return_value=p):
            out = ingest.ingest(fixture(), "bad-width", self.base)
        d = read_inspection(out["project_path"])
        self.assertEqual(d["unknowns"]["streams.0.video.width"], "INVALID_METADATA")
        p = fresh_probe(fixture())
        p["streams"][0]["side_data_list"] = [
            {"side_data_type": "Display Matrix", "rotation": 0, "displaymatrix": "\n0: 65536 0 0\n1: 0 65536 0\n2: 0 0 1073741824\n"},
            {"side_data_type": "Display Matrix", "rotation": 90, "displaymatrix": "\n0: 0 -65536 0\n1: 65536 0 0\n2: 0 0 1073741824\n"}]
        with patch("media_inspection.load_json", return_value=p):
            out = ingest.ingest(fixture(), "multiple-matrices", self.base)
        self.assertEqual(out["status"], "NEEDS_REVIEW")
        self.assertEqual(read_inspection(out["project_path"])["unknowns"]["streams.0.video.display_matrix"], "AMBIGUOUS")


if __name__ == "__main__": unittest.main()
