from __future__ import annotations

import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from support_media import ROOT, contract, fixture, read_inspection, rehash_revision
import ingest


class ContractTests(unittest.TestCase):
    def setUp(self):
        parent = ROOT / ".local/validation/F002/tests"; parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.base = Path(self.temp.name)
        out = ingest.ingest(fixture(), "contract-test", self.base)
        self.root = Path(out["project_path"])
        self.doc = read_inspection(self.root)

    def tearDown(self): self.temp.cleanup()

    def test_independent_consumer_wire_input(self):
        # The assertions below use only the wire files and standard library,
        # not ffprobe parsing or the implementation normalizer/validator.
        ingest_output = contract.verify_project(self.root)  # mandatory fresh guard
        project = json.loads((self.root / "project.json").read_text())
        current = json.loads((self.root / "current.json").read_text())
        info = json.loads((self.root / current["inspection_path"]).read_text())
        self.assertEqual(current["status"], "READY")
        raw = self.root / project["source"]["path"]
        self.assertFalse(Path(project["source"]["path"]).is_absolute())
        self.assertEqual(hashlib.sha256(raw.read_bytes()).hexdigest(), project["source"]["sha256"])
        self.assertEqual(hashlib.sha256((self.root / current["inspection_path"]).read_bytes()).hexdigest(), current["inspection_sha256"])
        self.assertEqual(info["timing"]["clock"], "source-presentation-v1")
        self.assertGreater(Fraction(info["timing"]["video_end_s"]), 0)
        self.assertGreater(Fraction(info["timing"]["audio_end_s"]), Fraction(info["timing"]["audio_start_s"]))
        self.assertEqual(info["display"]["geometry"], "PORTRAIT")
        selected = {s["index"]: s for s in info["streams"]}
        self.assertEqual(selected[info["selection"]["audio_index"]]["audio"]["sample_rate_hz"], 32000)
        self.assertNotIn("transcript", info)
        self.assertEqual(ingest_output[2]["source_id"], info["source_id"])

    def test_canonical_roundtrip_and_large_rationals(self):
        bytes_before = contract.canonical_bytes(self.doc)
        self.assertEqual(bytes_before, contract.canonical_bytes(json.loads(bytes_before)))
        self.assertEqual(bytes_before[-1:], b"\n")
        value = Fraction(10**50 + 1, 10**49 + 3)
        self.assertEqual(Fraction(contract.rational(value)), value)
        self.assertIn("ü".encode(), contract.canonical_bytes({"text": "ü"}))

    def test_unknowns_must_track_nulls(self):
        d = copy.deepcopy(self.doc); d["unknowns"].clear()
        with self.assertRaises(contract.ContractError): contract.validate_inspection(d)
        d = copy.deepcopy(self.doc); d["unknowns"]["fake"] = "NOT_REPORTED"
        with self.assertRaises(contract.ContractError): contract.validate_inspection(d)
        d = copy.deepcopy(self.doc); key = next(iter(d["unknowns"])); d["unknowns"][key] = "guessed"
        with self.assertRaises(contract.ContractError): contract.validate_inspection(d)

    def test_unsupported_version_kind_and_core_keys(self):
        for key, value in (("schema_version", 2), ("schema_version", True), ("kind", "transcript"), ("brand", {})):
            with self.subTest(key=key):
                d = copy.deepcopy(self.doc); d[key] = value
                with self.assertRaises(contract.ContractError): contract.validate_inspection(d)
        d = copy.deepcopy(self.doc); del d["timing"]
        with self.assertRaises(contract.ContractError): contract.validate_inspection(d)

    def test_bad_numbers_ratios_selection_and_clock(self):
        for apply in (lambda d: d["streams"][0]["video"].update(width=True),
                      lambda d: d["streams"][0]["video"].update(sar="0/0"),
                      lambda d: d["streams"][0]["video"].update(sar="2/2"),
                      lambda d: d["selection"].update(audio_index=999),
                      lambda d: d["timing"].update(clock_id="0"*64),
                      lambda d: d["timing"].update(video_end_s=2.5),
                      lambda d: d["timing"].update(frame_count=0)):
            d = copy.deepcopy(self.doc); apply(d)
            with self.assertRaises(contract.ContractError): contract.validate_inspection(d)

    def test_paths_traversal_and_escaping_symlink(self):
        for rel in ("../elsewhere", "/absolute", "inspections/../raw/source", "raw\\source", ""):
            with self.subTest(rel=rel), self.assertRaises(contract.ContractError): contract.safe_path(self.root, rel)
        external = self.base / "external"; external.write_text("outside")
        link = self.root / "escape"; link.symlink_to(external)
        with self.assertRaises(contract.ContractError): contract.safe_path(self.root, "escape")
        current = contract.load_json(self.root / "current.json")
        current["inspection_path"] = "../external"
        contract.atomic_json(self.root / "current.json", current)
        with self.assertRaises(contract.ContractError): contract.verify_project(self.root)

    def test_tampered_artifact_blocks_readiness(self):
        current = contract.load_json(self.root / "current.json")
        p = self.root / current["inspection_path"]
        p.write_bytes(p.read_bytes() + b" ")
        with self.assertRaises(contract.ContractError) as e: contract.verify_project(self.root)
        self.assertEqual(e.exception.code, "ARTIFACT_CHANGED")

    def test_structural_guard_even_after_rehash(self):
        current = contract.load_json(self.root / "current.json")
        d = copy.deepcopy(self.doc); d["schema_version"] = 99
        contract.atomic_json(self.root / current["inspection_path"], d); rehash_revision(self.root)
        with self.assertRaises(contract.ContractError) as e: contract.verify_project(self.root)
        self.assertEqual(e.exception.code, "UNSUPPORTED_VERSION")

    def test_incomplete_execution_cannot_be_ready(self):
        current = contract.load_json(self.root / "current.json")
        p = self.root / current["execution_path"]
        d = contract.load_json(p); d["completed"] = False
        contract.atomic_json(p, d); rehash_revision(self.root)
        with self.assertRaises(contract.ContractError) as e: contract.verify_project(self.root)
        self.assertEqual(e.exception.code, "INSPECTION_INCOMPLETE")

    def test_failed_command_or_missing_execution_evidence_cannot_be_ready(self):
        current = contract.load_json(self.root / "current.json")
        p = self.root / current["execution_path"]
        original = contract.load_json(p)
        for mutate in (lambda d: d["commands"][0].update(exit_code=9),
                       lambda d: d["commands"][0].update(timed_out=True),
                       lambda d: d.update(commands=[]),
                       lambda d: d.update(schema_version=True)):
            d = copy.deepcopy(original); mutate(d)
            contract.atomic_json(p, d); rehash_revision(self.root)
            with self.assertRaises(contract.ContractError): contract.verify_project(self.root)

    def test_binding_wrong_source_or_manifest(self):
        for key in ("source_id", "project_manifest_sha256"):
            with self.subTest(key=key):
                current = contract.load_json(self.root / "current.json")
                prior = copy.deepcopy(current)
                current[key] = "sha256:"+"0"*64 if key == "source_id" else "0"*64
                contract.atomic_json(self.root / "current.json", current)
                with self.assertRaises(contract.ContractError): contract.verify_project(self.root)
                contract.atomic_json(self.root / "current.json", prior)

    def test_extensions_are_ignorable_and_not_core(self):
        current = contract.load_json(self.root / "current.json")
        d = copy.deepcopy(self.doc); d["extensions"] = {"org.example.extra": {"new_field": None, "number": 1.25}}
        contract.atomic_json(self.root / current["inspection_path"], d); rehash_revision(self.root)
        self.assertEqual(contract.verify_project(self.root)[1]["status"], "READY")
        d["extensions"] = {"not_namespaced": {}}
        with self.assertRaises(contract.ContractError): contract.validate_inspection(d)

    def test_json_nonfinite_duplicate_and_malformed(self):
        p = self.base / "bad.json"
        for data in ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{malformed'):
            p.write_text(data)
            with self.assertRaises(contract.ContractError): contract.load_json(p)


if __name__ == "__main__": unittest.main()
