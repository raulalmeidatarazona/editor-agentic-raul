"""F002 local ingest/inspect/verify CLI. No dependencies outside the stdlib/tools."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys
import uuid

from content_contract import (ContractError, HASH, PROJECT_ID, atomic_json, canonical_bytes,
    hash_file, load_json, safe_path, stat_identity, sync_directory, unknown_fields,
    validate_current, validate_options, validate_project, verify_project)
from media_inspection import EVIDENCE_LIMIT, Runner, inspect_media, inspector_version, tool_versions

DEFAULT_ROOT = Path(__file__).resolve().parent.parent / ".local" / "projects"
EXIT_CODES = {"READY": 0, "NEEDS_REVIEW": 2, "BLOCKED": 3, "INVALID": 4}


def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def default_options():
    return {"video_index": None, "audio_index": None, "display_rotation_override_deg": None,
            "override_reason": None, "override_reviewer": None}


def call_hook(hook, point, **context):
    # Injection is a Python test seam only, never an environment flag or CLI option.
    if hook is not None:
        hook(point, context)


def require_runtime():
    if sys.version_info[:3] != (3, 14, 7):
        raise ContractError("RUNTIME_VERSION_MISMATCH", "F002 was approved for existing Python 3.14.7; recheck compatibility without auto-installing.")


def check_source(path):
    if "://" in str(path):
        raise ContractError("INPUT_NOT_LOCAL", "Use a local regular file, not a URL.", "source", "INVALID")
    p = Path(path).absolute()
    if not p.exists():
        raise ContractError("INPUT_MISSING", "Locate the source file before ingesting.", str(p), "INVALID")
    if not p.is_file() or not p.stat().st_size:
        raise ContractError("INPUT_NOT_REGULAR_OR_EMPTY", "Provide a nonempty regular media file.", str(p), "INVALID")
    try:
        with p.open("rb") as f:
            f.read(1)
    except OSError as exc:
        raise ContractError("INPUT_UNREADABLE", "Cannot read source; check local permissions/access.", str(p), "INVALID") from exc
    return p


@contextmanager
def project_lock(parent, project_id):
    directory = Path(parent) / ".locks"
    directory.mkdir(parents=True, exist_ok=True)
    lock = safe_path(parent, ".locks/" + project_id + ".lock")
    try:
        f = lock.open("xb")
    except FileExistsError as exc:
        raise ContractError("BUSY", "A writer/stale lock exists. Diagnose its PID/run and recover explicitly; never expire by age.", str(lock)) from exc
    with f:
        f.write(canonical_bytes({"pid": os.getpid(), "run_id": str(uuid.uuid4()), "created_at_utc": utc_now(), "project_id": project_id}))
        f.flush(); os.fsync(f.fileno())
    sync_directory(directory)
    try:
        yield
    finally:
        lock.unlink()
        sync_directory(directory)


def source_manifest(source, project_id, sha, profile, limitations, references):
    doc = {"schema_version": 1, "kind": "content-project-source", "project_id": project_id,
           "source": {"id": "sha256:" + sha, "path": "raw/source", "bytes": source.stat().st_size, "sha256": sha,
                      "original_name": source.name, "original_path": str(source), "resolved_original_path": str(source.resolve()), "ingested_at_utc": utc_now()},
           "capture_context": {"profile": profile, "limitations": limitations}, "references": references,
           "unknowns": {}, "extensions": {}}
    doc["unknowns"] = unknown_fields(doc, "NOT_PROVIDED")
    validate_project(doc)
    return doc


def current_document(project, manifest_hash, status="BLOCKED", reasons=None, inspection=None, execution=None, hashes=None):
    doc = {"schema_version": 1, "kind": "current-media-inspection", "project_id": project["project_id"],
           "source_id": project["source"]["id"], "status": status,
           "reasons": reasons or [{"code": "INSPECTION_IN_PROGRESS", "field": "current.json", "action": "Wait for complete inspection or recover interrupted work explicitly."}],
           "inspection_path": inspection, "inspection_sha256": (hashes or {}).get(inspection),
           "execution_path": execution, "execution_sha256": (hashes or {}).get(execution),
           "project_manifest_sha256": manifest_hash, "artifact_hashes": hashes or {}, "unknowns": {}, "extensions": {}}
    if status == "READY":
        doc["reasons"] = []
    doc["unknowns"] = unknown_fields(doc, "NOT_PROVIDED")
    validate_current(doc)
    return doc


def render_report(project, inspection, failure=None):
    s = project["source"]
    lines = ["# F002 — Local media inspection", "", f"Project: {project['project_id']}",
             f"Source: {s['original_name']} → {s['path']}", f"Bytes: {s['bytes']}", f"SHA-256: {s['sha256']}",
             "", "Source bytes/hash: MEASURED. Capture context: USER-REPORTED; no voice/equipment inference.",
             f"Profile: {project['capture_context']['profile']}", "", "Recovery reference: " + str(project["references"]["recovery_location"]),
             "Recovery was referenced, not reverified by F002. Owned copy is independent of original path, not a separate-disk backup.", ""]
    if inspection:
        d, t = inspection["display"], inspection["timing"]
        video = next((s for s in inspection["streams"] if s["index"] == inspection["selection"]["video_index"]), None)
        lines += ["Status: " + inspection["readiness"]["status"], "Selection: " + str(inspection["selection"]),
                  "Stored raster (MEASURED): " + str(video["video"] if video else "UNKNOWN"),
                  "Display (DERIVED; override USER-REPORTED if used): " + str(d), "Clock/offsets (DERIVED): " + str(t), ""]
        for reason in inspection["readiness"]["reasons"]:
            lines.append(f"- {reason['code']} / {reason['field']}: {reason['action']}")
        lines += ["", "UNKNOWN fields:"] + [f"- {p}: {r}" for p, r in inspection["unknowns"].items()]
    if failure:
        lines += ["", f"Failure: {failure.code}: {failure.action}"]
    lines += ["", "Declared limitations:"] + ["- " + x for x in project["capture_context"]["limitations"]]
    lines += ["", "READY concerns deterministic input only. No transcription, editorial, crop, audio enhancement, render or production approval.", ""]
    return "\n".join(lines)


def result(operation, outcome, project_id, project_path, current=None, error=None):
    return {"operation": operation, "outcome": outcome, "project_id": project_id,
            "status": error.status if error else current["status"], "reasons": [error.reason()] if error else current["reasons"],
            "project_path": str(project_path) if project_path else None,
            "inspection_path": current["inspection_path"] if current else None}


def inspect_owned(root, project, options, timeout, hook=None, original=None, original_before=None,
                  ffprobe="ffprobe", ffmpeg="ffmpeg"):
    root = Path(root)
    validate_project(project); validate_options(options)
    manifest_hash = hash_file(root / "project.json")
    source = safe_path(root, project["source"]["path"])
    # Invalidate old readiness before any tool call, including tool/version failure.
    atomic_json(root / "current.json", current_document(project, manifest_hash))
    call_hook(hook, "after_invalidation", root=root, source=source)
    run_id = str(uuid.uuid4())
    directory = safe_path(root, "inspections/" + run_id)
    directory.mkdir(parents=True)
    runner = Runner(directory, timeout)
    before, after, inspection, failure, versions = None, None, None, None, {}
    try:
        before = {"stat": stat_identity(source), "sha256": hash_file(source)}
        if before["sha256"] != project["source"]["sha256"] or before["stat"]["bytes"] != project["source"]["bytes"] or source.is_symlink():
            raise ContractError("SOURCE_CHANGED", "Owned RAW differs from the immutable source manifest; recover explicitly.", "raw/source")
        versions = tool_versions(ffprobe, ffmpeg)
        call_hook(hook, "during_inspection", root=root, source=source)
        inspection = inspect_media(source, project, manifest_hash, directory, options, runner, versions, ffprobe, ffmpeg)
        after = {"stat": stat_identity(source), "sha256": hash_file(source)}
        if before != after or hash_file(root / "project.json") != manifest_hash:
            raise ContractError("SOURCE_CHANGED", "Source/manifest changed during inspection; no READY publication.", "source")
        if original is not None:
            original_after = {"stat": stat_identity(original), "sha256": hash_file(original)}
            if original_after != original_before:
                raise ContractError("SOURCE_CHANGED", "Original changed during ingest/inspection; preserve copies and investigate.", "original")
        else:
            original_after = None
        call_hook(hook, "before_commit", root=root, source=source)
        # Hooks/IO can change bytes at the last boundary; check again before commit.
        if stat_identity(source) != after["stat"] or hash_file(source) != after["sha256"] or hash_file(root / "project.json") != manifest_hash:
            raise ContractError("SOURCE_CHANGED", "Source changed before publication.", "source")
        if original is not None:
            original_after = {"stat": stat_identity(original), "sha256": hash_file(original)}
            if original_after != original_before:
                raise ContractError("SOURCE_CHANGED", "Original changed at publication boundary; no READY result.", "original")
    except (ContractError, OSError, ValueError, TypeError) as exc:
        failure = exc if isinstance(exc, ContractError) else ContractError("IO_OR_INSPECTION_FAILED", "Inspect retained diagnostics: " + str(exc))
        original_after = None
    if failure:
        status, reasons = failure.status, [failure.reason()]
        # A failed attempt never retains a normalized READY artifact as its active revision.
        inspection = None
    else:
        status, reasons = inspection["readiness"]["status"], inspection["readiness"]["reasons"]
        runner.reserve(len(canonical_bytes(inspection)))
        atomic_json(directory / "inspection.json", inspection)
    report = render_report(project, inspection, failure)
    runner.reserve(len(report.encode()))
    with (directory / "report.md").open("x") as f:
        f.write(report); f.flush(); os.fsync(f.fileno())
    if (directory / "decode.stderr").exists():
        runner.reserve((directory / "decode.stderr").stat().st_size)
        shutil.copyfile(directory / "decode.stderr", directory / "decode.log")
    prefix = "inspections/" + run_id + "/"
    hashes = {prefix + p.name: hash_file(p) for p in directory.iterdir() if p.is_file()}
    if sum(p.stat().st_size for p in directory.iterdir() if p.is_file()) >= EVIDENCE_LIMIT:
        status, reasons, inspection = "BLOCKED", [{"code": "LIMIT_EXCEEDED", "field": "evidence", "action": "Aggregate evidence cap reached."}], None
    execution = {"schema_version": 1, "kind": "media-inspection-execution", "project_id": project["project_id"], "run_id": run_id,
        "source_id": project["source"]["id"], "project_manifest_sha256": manifest_hash,
        "started_at_utc": getattr(runner, "started_at_utc", utc_now()), "finished_at_utc": utc_now(), "completed": True,
        "status": status, "reasons": reasons, "options": {**options, "command_timeout_seconds": timeout},
        "versions": {**versions, "python": sys.version.split()[0], "inspector": inspector_version()},
        "commands": [{**c, "stdout_path": prefix + c["stdout_path"], "stderr_path": prefix + c["stderr_path"]} for c in runner.commands],
        "integrity": {"owned_before": before, "owned_after": after, "original_before": original_before, "original_after": original_after},
        "artifact_hashes": hashes}
    runner.reserve(len(canonical_bytes(execution)))
    atomic_json(directory / "execution.json", execution)
    hashes = {**hashes, prefix + "execution.json": hash_file(directory / "execution.json")}
    current = current_document(project, manifest_hash, status, reasons,
        prefix + "inspection.json" if inspection else None, prefix + "execution.json", hashes)
    atomic_json(root / "current.json", current)
    return current


def ingest(source, project_id, projects_root=DEFAULT_ROOT, profile="UNKNOWN", limitations=None,
           references=None, expected_sha256=None, options=None, timeout=600, hook=None):
    require_runtime()
    if not isinstance(project_id, str) or not PROJECT_ID.fullmatch(project_id):
        raise ContractError("INVALID_PROJECT_ID", "Use a lowercase ID matching [a-z0-9][a-z0-9-]{0,63}.", "project_id", "INVALID")
    source = check_source(source)
    options = options or default_options(); validate_options(options)
    if expected_sha256 is not None and not HASH.fullmatch(expected_sha256):
        raise ContractError("INVALID_EXPECTED_HASH", "Expected SHA-256 must be 64 lowercase hexadecimal characters.", "expected_sha256", "INVALID")
    limitations = list(limitations or [])
    references = references or {k: None for k in ("fixture_id", "feature_revision", "recovery_location", "evidence_manifest_sha256")}
    projects_root = Path(projects_root).resolve(); projects_root.mkdir(parents=True, exist_ok=True)
    root = safe_path(projects_root, project_id)
    if root.is_symlink():
        raise ContractError("PROJECT_CONFLICT", "Do not reuse a symlink project root.", project_id)
    with project_lock(projects_root, project_id):
        initial = {"stat": stat_identity(source), "sha256": hash_file(source)}
        if expected_sha256 is not None and initial["sha256"] != expected_sha256:
            raise ContractError("EXPECTED_HASH_MISMATCH", "Source does not match the approved expected SHA-256.", "source")
        call_hook(hook, "after_hash", source=source, root=root)
        if root.exists():
            existing = load_json(safe_path(root, "project.json")); validate_project(existing)
            if existing["source"]["sha256"] != initial["sha256"] or existing["source"]["bytes"] != initial["stat"]["bytes"] or existing["capture_context"] != {"profile": profile, "limitations": limitations} or existing["references"] != references:
                raise ContractError("PROJECT_CONFLICT", "This ID already owns another source/context. Use a new project ID.", project_id)
            _, current, inspection = verify_project(root)
            if inspection["options"] != options or inspection["tool_versions"] != tool_versions() or inspection["inspector_version"] != inspector_version():
                raise ContractError("INSPECTION_OPTIONS_CHANGED", "Use explicit inspect for changed selection/options/tool or inspector version.", project_id)
            if initial != {"stat": stat_identity(source), "sha256": hash_file(source)}:
                raise ContractError("SOURCE_CHANGED", "Original changed during repeated ingest.", "source")
            return result("ingest", "NO_OP", project_id, root, current)
        if shutil.disk_usage(projects_root).free < initial["stat"]["bytes"] + EVIDENCE_LIMIT:
            raise ContractError("IO_NO_SPACE", "Need source bytes plus 512 MiB free for this ingest.", str(projects_root))
        stage = safe_path(projects_root, ".staging/" + project_id + "-" + str(uuid.uuid4()))
        (stage / "raw").mkdir(parents=True)
        owned = stage / "raw/source"
        try:
            with source.open("rb") as src, owned.open("xb") as dst:
                while chunk := src.read(4 * 1024 * 1024):
                    dst.write(chunk)
                    call_hook(hook, "during_copy", source=source, root=stage, owned=owned)
                dst.flush(); os.fsync(dst.fileno())
            call_hook(hook, "after_copy", source=source, root=stage, owned=owned)
            final = {"stat": stat_identity(source), "sha256": hash_file(source)}
            if initial != final or owned.stat().st_size != initial["stat"]["bytes"] or hash_file(owned) != initial["sha256"]:
                raise ContractError("SOURCE_CHANGED", "Original/copy identity is unstable; partial work retained.", "source")
            owned.chmod(0o444)
            project = source_manifest(source, project_id, initial["sha256"], profile, limitations, references)
            atomic_json(stage / "project.json", project)
            current = inspect_owned(stage, project, options, timeout, hook, source, initial)
            sync_directory(stage / "raw"); sync_directory(stage)
            if root.exists():
                raise ContractError("PROJECT_CONFLICT", "Project appeared during staging; refuse replacement.", str(root))
            os.rename(stage, root)
            sync_directory(projects_root)
            return result("ingest", "CREATED", project_id, root, current)
        except (OSError, ContractError, ValueError) as exc:
            error = exc if isinstance(exc, ContractError) else ContractError("IO_FAILED", "Copy/publication failed; staging retained: " + str(exc))
            try:
                atomic_json(stage / "failure.json", {"recorded_at_utc": utc_now(), "status": error.status, "reason": error.reason(), "stage": str(stage)})
            except OSError:
                pass
            raise error


def inspect_project(root, options=None, timeout=600, hook=None):
    require_runtime()
    root = Path(root).resolve()
    project = load_json(safe_path(root, "project.json")); validate_project(project)
    with project_lock(root.parent, project["project_id"]):
        old_options = default_options()
        current_path = safe_path(root, "current.json")
        if current_path.exists():
            old = load_json(current_path); validate_current(old)
            if old["inspection_path"] is not None:
                p = safe_path(root, old["inspection_path"])
                if p.exists() and hash_file(p) == old["inspection_sha256"]:
                    old_options = load_json(p)["options"]
            elif old["execution_path"] is not None:
                p = safe_path(root, old["execution_path"])
                if p.exists() and hash_file(p) == old["execution_sha256"]:
                    opts = load_json(p)["options"]
                    old_options = {k: opts[k] for k in default_options()}
        new_options = {**old_options, **(options or {})}
        validate_options(new_options)
        current = inspect_owned(root, project, new_options, timeout, hook)
        return result("inspect", "REINSPECTED", project["project_id"], root, current)


class CLIParser(argparse.ArgumentParser):
    def error(self, message):
        error = ContractError("INVALID_ARGUMENT", message, "arguments", "INVALID")
        sys.stdout.buffer.write(canonical_bytes(result("arguments", "REJECTED", None, None, error=error)))
        raise SystemExit(4)


def main(argv=None):
    parser = CLIParser(description="F002 local media ingestion/inspection; no editing or transcription.")
    sub = parser.add_subparsers(dest="operation", required=True)
    p = sub.add_parser("ingest")
    p.add_argument("--source", required=True); p.add_argument("--project-id", required=True)
    p.add_argument("--projects-root", type=Path, default=DEFAULT_ROOT)
    p.add_argument("--profile", choices=("STUDIO", "MOBILE", "UNKNOWN"), default="UNKNOWN")
    p.add_argument("--expected-sha256"); p.add_argument("--limitation", action="append", default=[])
    for name in ("fixture-id", "feature-revision", "recovery-location", "evidence-manifest-sha256"):
        p.add_argument("--" + name)
    q = sub.add_parser("inspect"); q.add_argument("--project", required=True, type=Path)
    q.add_argument("--display-rotation", type=int, choices=(0, -90, 90, 180))
    q.add_argument("--override-reason"); q.add_argument("--override-reviewer")
    for child in (p, q):
        child.add_argument("--video-stream", type=int); child.add_argument("--audio-stream", type=int)
        child.add_argument("--command-timeout-seconds", type=int, default=600)
    v = sub.add_parser("verify"); v.add_argument("--project", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.operation == "ingest":
            options = {**default_options(), "video_index": args.video_stream, "audio_index": args.audio_stream}
            refs = {k: getattr(args, k) for k in ("fixture_id", "feature_revision", "recovery_location", "evidence_manifest_sha256")}
            out = ingest(args.source, args.project_id, args.projects_root, args.profile, args.limitation,
                         refs, args.expected_sha256, options, args.command_timeout_seconds)
        elif args.operation == "inspect":
            options = {}
            for key, arg in (("video_index", args.video_stream), ("audio_index", args.audio_stream), ("display_rotation_override_deg", args.display_rotation), ("override_reason", args.override_reason), ("override_reviewer", args.override_reviewer)):
                if arg is not None:
                    options[key] = arg
            out = inspect_project(args.project, options, args.command_timeout_seconds)
        else:
            project, current, _ = verify_project(args.project)
            out = result("verify", "VERIFIED", project["project_id"], args.project, current)
    except (ContractError, OSError, ValueError, TypeError, KeyError) as exc:
        error = exc if isinstance(exc, ContractError) else ContractError("IO_OR_CONTRACT_FAILED", "Inspect local access/contract: " + str(exc))
        out = result(args.operation, "REJECTED", getattr(args, "project_id", None), getattr(args, "project", None), error=error)
    sys.stdout.buffer.write(canonical_bytes(out))
    return EXIT_CODES[out["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
