from __future__ import annotations

import errno
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import signal
import unittest
from unittest.mock import patch

from support_media import ROOT, contract, fixture, file_snapshot, read_inspection
import ingest


class IngestTests(unittest.TestCase):
    def setUp(self):
        parent = ROOT / ".local" / "validation" / "F002" / "tests"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.base = Path(self.temp.name)
        self.projects = self.base / "projects"
        self.source = self.base / "Grabación móvil ü con espacios.mp4"
        shutil.copyfile(fixture(), self.source)

    def tearDown(self):
        self.temp.cleanup()

    def ingest(self, **kwargs):
        return ingest.ingest(self.source, "test-project", self.projects, profile="MOBILE", **kwargs)

    def test_real_copy_and_noop_and_alias(self):
        before = file_snapshot(self.base)
        first = self.ingest()
        self.assertEqual(first["status"], "READY")
        root = Path(first["project_path"])
        manifest = contract.load_json(root / "project.json")
        self.assertEqual(manifest["source"]["original_name"], self.source.name)
        self.assertEqual(manifest["source"]["sha256"], contract.hash_file(self.source))
        self.assertNotEqual(self.source.stat().st_ino, (root / "raw/source").stat().st_ino)
        snapshot = file_snapshot(root)
        self.assertEqual(self.ingest()["outcome"], "NO_OP")
        self.assertEqual(snapshot, file_snapshot(root))
        alias = self.base / "alias.mp4"; shutil.copyfile(self.source, alias)
        self.assertEqual(ingest.ingest(alias, "test-project", self.projects, profile="MOBILE")["outcome"], "NO_OP")
        self.assertEqual(snapshot, file_snapshot(root))
        self.assertEqual(before[self.source.name], file_snapshot(self.base)[self.source.name])

    def test_source_or_context_conflict(self):
        root = Path(self.ingest()["project_path"]); snapshot = file_snapshot(root)
        for source, profile in ((fixture("landscape"), "MOBILE"), (self.source, "STUDIO")):
            with self.subTest(profile=profile), self.assertRaises(contract.ContractError) as e:
                ingest.ingest(source, "test-project", self.projects, profile=profile)
            self.assertEqual(e.exception.code, "PROJECT_CONFLICT")
            self.assertEqual(snapshot, file_snapshot(root))

    def test_expected_hash_and_invalid_id(self):
        with self.assertRaises(contract.ContractError) as e:
            self.ingest(expected_sha256="0" * 64)
        self.assertEqual(e.exception.code, "EXPECTED_HASH_MISMATCH")
        self.assertFalse((self.projects / "test-project").exists())
        with self.assertRaises(contract.ContractError):
            ingest.ingest(self.source, "UPPERCASE", self.projects)

    def test_invalid_sources(self):
        empty = self.base / "empty"; empty.touch()
        random = self.base / "random"; random.write_bytes(b"not media")
        for src in (self.base / "missing", empty, self.base, "https://example.invalid/source.mp4"):
            with self.subTest(src=str(src)), self.assertRaises(contract.ContractError) as e:
                ingest.ingest(src, "bad", self.projects)
            self.assertEqual(e.exception.status, "INVALID")
        out = ingest.ingest(random, "random", self.projects)
        self.assertNotEqual(out["status"], "READY")
        self.assertIn("PROBE_FAILED", [r["code"] for r in out["reasons"]])

    def test_unreadable_source(self):
        with patch.object(Path, "open", side_effect=PermissionError("test-only unreadable")):
            with self.assertRaises(contract.ContractError) as e:
                ingest.check_source(self.source)
        self.assertEqual(e.exception.code, "INPUT_UNREADABLE")

    def test_regeneration_and_relocation_without_origin(self):
        root = Path(self.ingest()["project_path"])
        prior = contract.load_json(root / "current.json")
        manifest_hash, raw_hash = contract.hash_file(root / "project.json"), contract.hash_file(root / "raw/source")
        first_bytes = (root / prior["inspection_path"]).read_bytes()
        self.source.unlink()
        second = ingest.inspect_project(root)
        self.assertEqual(second["status"], "READY")
        self.assertEqual(first_bytes, (root / second["inspection_path"]).read_bytes())
        self.assertTrue((root / prior["inspection_path"]).exists())
        derived = root / second["inspection_path"]; derived.unlink()
        with self.assertRaises(OSError):
            contract.verify_project(root)
        regenerated = ingest.inspect_project(root)
        self.assertEqual(regenerated["status"], "READY")
        moved = self.base / "moved-project"; root.rename(moved)
        contract.verify_project(moved)
        self.assertEqual(manifest_hash, contract.hash_file(moved / "project.json"))
        self.assertEqual(raw_hash, contract.hash_file(moved / "raw/source"))

    def test_changed_owned_source_and_no_ready_fallback(self):
        root = Path(self.ingest()["project_path"])
        owned = root / "raw/source"; owned.chmod(0o644)
        with owned.open("ab") as f: f.write(b"tampered")
        with self.assertRaises(contract.ContractError) as e: contract.verify_project(root)
        self.assertEqual(e.exception.code, "SOURCE_CHANGED")
        result = ingest.inspect_project(root)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(contract.load_json(root / "current.json")["status"], "BLOCKED")

    def test_source_changes_during_copy(self):
        def hook(point, ctx):
            if point == "after_copy":
                with self.source.open("ab") as f: f.write(b"changed during test")
        with self.assertRaises(contract.ContractError) as e: self.ingest(hook=hook)
        self.assertEqual(e.exception.code, "SOURCE_CHANGED")
        self.assertFalse((self.projects / "test-project").exists())
        self.assertTrue(list((self.projects / ".staging").glob("*/failure.json")))

    def test_changes_during_inspection_and_before_commit(self):
        for point in ("during_inspection", "before_commit"):
            with self.subTest(point=point):
                root = Path(ingest.ingest(self.source, "point-" + point.replace("_", "-"), self.projects)["project_path"])
                def hook(p, ctx):
                    if p == point:
                        ctx["source"].chmod(0o644)
                        with ctx["source"].open("ab") as f: f.write(b"changed")
                out = ingest.inspect_project(root, hook=hook)
                self.assertEqual(out["status"], "BLOCKED")
                self.assertEqual(contract.load_json(root / "current.json")["status"], "BLOCKED")

    def test_writer_lock_and_stale_lock(self):
        self.projects.mkdir()
        with ingest.project_lock(self.projects, "test-project"):
            lock = self.projects / ".locks/test-project.lock"
            lock_snapshot = lock.read_bytes()
            with self.assertRaises(contract.ContractError) as e: self.ingest()
            self.assertEqual(e.exception.code, "BUSY")
            self.assertEqual(lock_snapshot, lock.read_bytes())
        lock.write_text('{"pid":99999999,"created_at_utc":"2000-01-01T00:00:00Z"}')
        with self.assertRaises(contract.ContractError) as e: self.ingest()
        self.assertEqual(e.exception.code, "BUSY")
        self.assertTrue(lock.exists())
        lock.unlink()  # explicit test recovery only, known nonexistent PID
        self.assertEqual(self.ingest()["status"], "READY")

    def test_io_failures_retain_original(self):
        original = contract.hash_file(self.source)
        with patch("ingest.shutil.disk_usage", return_value=shutil._ntuple_diskusage(1, 1, 0)):
            with self.assertRaises(contract.ContractError) as e: self.ingest()
        self.assertEqual(e.exception.code, "IO_NO_SPACE")
        def hook(point, ctx):
            if point == "during_copy": raise OSError(errno.ENOSPC, "test-only disk full")
        with self.assertRaises(contract.ContractError): self.ingest(hook=hook)
        with patch("ingest.os.rename", side_effect=OSError(errno.EIO, "test-only rename failure")):
            with self.assertRaises(contract.ContractError): self.ingest()
        self.assertEqual(original, contract.hash_file(self.source))
        self.assertFalse((self.projects / "test-project").exists())

    def test_invalidation_interruption_and_explicit_recovery(self):
        root = Path(self.ingest()["project_path"])
        def interrupt(point, ctx):
            if point == "after_invalidation": raise KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt): ingest.inspect_project(root, hook=interrupt)
        self.assertEqual(contract.load_json(root / "current.json")["status"], "BLOCKED")
        with self.assertRaises(contract.ContractError): contract.verify_project(root)
        self.assertEqual(ingest.inspect_project(root)["status"], "READY")

    def test_cli_machine_result(self):
        p = subprocess.run([sys.executable, ROOT / "tools/ingest.py", "ingest", "--source", self.source, "--project-id", "cli", "--projects-root", self.projects], capture_output=True)
        self.assertEqual(p.returncode, 0, p.stderr.decode() + p.stdout.decode())
        out = json.loads(p.stdout)
        self.assertEqual(set(out), {"operation", "outcome", "project_id", "status", "reasons", "project_path", "inspection_path"})
        self.assertEqual(out["status"], "READY")

    def test_original_mutation_at_publication_is_blocked(self):
        def hook(point, ctx):
            if point == "before_commit":
                with self.source.open("ab") as f: f.write(b"original changed at boundary")
        out = self.ingest(hook=hook)
        self.assertEqual(out["status"], "BLOCKED")
        self.assertEqual(out["reasons"][0]["code"], "SOURCE_CHANGED")

    def test_real_process_kill_keeps_blocked_pointer_and_stale_lock(self):
        root = Path(self.ingest()["project_path"])
        before = contract.hash_file(root / "raw/source")
        code = "import sys,os,signal; sys.path.insert(0,sys.argv[1]); import ingest; ingest.inspect_project(sys.argv[2],hook=lambda point,ctx: os.kill(os.getpid(),signal.SIGKILL) if point=='after_invalidation' else None)"
        child = subprocess.run([sys.executable, "-c", code, str(ROOT / "tools"), str(root)], capture_output=True)
        self.assertEqual(child.returncode, -signal.SIGKILL)
        self.assertEqual(contract.load_json(root / "current.json")["status"], "BLOCKED")
        lock = self.projects / ".locks/test-project.lock"
        self.assertTrue(lock.exists())
        with self.assertRaises(contract.ContractError) as e: ingest.inspect_project(root)
        self.assertEqual(e.exception.code, "BUSY")
        lock.unlink()  # explicit recovery of this confirmed dead child only
        self.assertEqual(ingest.inspect_project(root)["status"], "READY")
        self.assertEqual(contract.hash_file(root / "raw/source"), before)

    def test_cli_invalid_arguments_are_invalid_exit_four(self):
        p = subprocess.run([sys.executable, ROOT / "tools/ingest.py", "ingest", "--profile", "invalid"], capture_output=True)
        self.assertEqual(p.returncode, 4)
        self.assertEqual(json.loads(p.stdout)["status"], "INVALID")


import sys

if __name__ == "__main__": unittest.main()
