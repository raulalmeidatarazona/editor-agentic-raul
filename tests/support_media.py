"""Small technical AV fixtures, retained locally with reproducible provenance."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import content_contract as contract

FIXTURES = ROOT / ".local" / "fixtures" / ("F002-synthetic-" + str(uuid.uuid4()))
FIXTURES.mkdir(parents=True)
COMMANDS = []
CACHE = {}


def generate(name, arguments):
    path = FIXTURES / name
    argv = ["ffmpeg", "-nostdin", "-hide_banner", "-v", "error", *map(str, arguments), str(path)]
    run = subprocess.run(argv, capture_output=True, timeout=30)
    COMMANDS.append({"argv": argv, "exit_code": run.returncode, "stderr": run.stderr.decode(errors="replace"),
                     "path": str(path), "sha256": contract.hash_file(path) if path.exists() else None})
    (FIXTURES / "generation.json").write_bytes(contract.canonical_bytes({"kind": "F002-synthetic-provenance", "commands": COMMANDS}))
    if run.returncode:
        raise RuntimeError(run.stderr.decode())
    if path.stat().st_size > 2 * 1024 * 1024 or sum(p.stat().st_size for p in FIXTURES.iterdir() if p.is_file()) > 20 * 1024 * 1024:
        raise RuntimeError("Approved synthetic fixture size budget exceeded")
    return path


def fixture(kind="portrait"):
    if kind in CACHE:
        return CACHE[kind]
    if kind in {"portrait", "landscape", "vfr", "bframes", "offset", "audio_lag"}:
        size = "160x90" if kind == "landscape" else "90x160"
        args = ["-f", "lavfi", "-i", f"testsrc2=size={size}:rate=10:duration=2", "-f", "lavfi", "-i", "sine=frequency=660:sample_rate=32000:duration=2"]
        codec, extra, suffix = "mpeg4", [], ".mp4"
        if kind == "vfr":
            extra = ["-vf", "setpts=if(lt(N\\,5)\\,N/(10*TB)\\,(N+2)/(10*TB))", "-fps_mode", "passthrough"]
        elif kind == "bframes":
            codec, extra = "libx264", ["-bf", "2", "-g", "10", "-pix_fmt", "yuv420p"]
        elif kind == "offset":
            codec, suffix, extra = "ffv1", ".mkv", ["-vf", "setpts=PTS+1/TB", "-af", "asetpts=PTS+0.5/TB", "-copyts", "-avoid_negative_ts", "disabled", "-fps_mode", "passthrough"]
        elif kind == "audio_lag":
            codec, suffix, extra = "ffv1", ".mkv", ["-af", "asetpts=PTS+1/TB", "-copyts", "-avoid_negative_ts", "disabled", "-fps_mode", "passthrough"]
        args += extra + ["-c:v", codec, "-c:a", "pcm_s16le" if kind in {"offset", "audio_lag"} else "aac"]
        path = generate(kind + suffix, args)
    elif kind == "audio_only":
        path = generate("audio-only.m4a", ["-f", "lavfi", "-i", "sine=sample_rate=32000:duration=2", "-c:a", "aac"])
    elif kind == "video_only":
        path = generate("video-only.mp4", ["-i", fixture(), "-map", "0:v:0", "-c", "copy", "-an"])
    elif kind in {"multi_video", "multi_audio"}:
        maps = ["-map", "0:v:0", "-map", "0:v:0", "-map", "0:a:0"] if kind == "multi_video" else ["-map", "0:v:0", "-map", "0:a:0", "-map", "0:a:0"]
        path = generate(kind + ".mp4", ["-i", fixture(), *maps, "-c", "copy"])
    elif kind == "attached":
        cover = generate("cover.jpg", ["-f", "lavfi", "-i", "color=red:size=160x90:duration=1", "-frames:v", "1"])
        path = generate("attached.mp4", ["-i", fixture(), "-i", cover, "-map", "0:v", "-map", "0:a", "-map", "1:v", "-c", "copy", "-disposition:v:1", "attached_pic"])
    elif kind.startswith("rotation_"):
        angle = int(kind.split("_")[1])
        path = generate(kind + ".mp4", ["-display_rotation", str(angle), "-i", fixture("landscape"), "-c", "copy"])
    elif kind == "sar":
        path = generate("sar.mp4", ["-i", fixture(), "-vf", "setsar=2/1", "-c:v", "mpeg4", "-c:a", "copy"])
    else:
        raise ValueError(kind)
    CACHE[kind] = path
    return path


def fresh_probe(path):
    return json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)]))


def file_snapshot(root):
    return {str(p.relative_to(root)): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
            for p in Path(root).rglob("*") if p.is_file()}


def read_inspection(root):
    current = contract.load_json(Path(root) / "current.json")
    return contract.load_json(Path(root) / current["inspection_path"])


def rehash_revision(root):
    """Test-only tampering seam: update hash manifests so structural checks are tested."""
    root = Path(root)
    current = contract.load_json(root / "current.json")
    execution_path = root / current["execution_path"]
    execution = contract.load_json(execution_path)
    for rel in list(execution["artifact_hashes"]):
        execution["artifact_hashes"][rel] = contract.hash_file(root / rel)
    contract.atomic_json(execution_path, execution)
    for rel in list(current["artifact_hashes"]):
        current["artifact_hashes"][rel] = contract.hash_file(root / rel)
    current["inspection_sha256"] = contract.hash_file(root / current["inspection_path"])
    current["execution_sha256"] = contract.hash_file(execution_path)
    contract.atomic_json(root / "current.json", current)
