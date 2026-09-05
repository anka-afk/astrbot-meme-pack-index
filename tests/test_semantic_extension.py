"""Validate optional semantic metadata without requiring the plugin runtime."""

import copy
import hashlib
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "examples/semantic/optional-semantic-demo"
MANIFEST = json.loads((PACK / "manifest.json").read_text())
METADATA = json.loads((PACK / "semantic_metadata.json").read_text())
MANIFEST_SCHEMA = json.loads(
    (ROOT / "schemas/meme-pack-manifest.schema.json").read_text()
)
SEMANTIC_SCHEMA = json.loads(
    (ROOT / "schemas/meme-pack-semantic.schema.json").read_text()
)


class SemanticExtensionTests(unittest.TestCase):
    def test_schemas_are_valid(self):
        for path in (ROOT / "schemas").glob("*.json"):
            Draft202012Validator.check_schema(json.loads(path.read_text()))

    def test_base_pack_does_not_require_extension(self):
        manifest = copy.deepcopy(MANIFEST)
        del manifest["extensions"]
        Draft202012Validator(MANIFEST_SCHEMA).validate(manifest)

    def test_declared_extension(self):
        Draft202012Validator(MANIFEST_SCHEMA).validate(MANIFEST)
        Draft202012Validator(SEMANTIC_SCHEMA).validate(METADATA)

    def test_empty_and_partial_description_coverage(self):
        metadata = copy.deepcopy(METADATA)
        metadata["images"] = {}
        Draft202012Validator(SEMANTIC_SCHEMA).validate(metadata)
        metadata["images"] = copy.deepcopy(METADATA["images"])
        Draft202012Validator(SEMANTIC_SCHEMA).validate(metadata)

    def test_bad_extension_declarations(self):
        for declaration in (
            {},
            {"version": 1},
            {"version": 2, "file": "semantic_metadata.json"},
            {"version": 1, "file": "../semantic_metadata.json"},
            {"version": 1, "file": "https://example.com/data.json"},
        ):
            with self.subTest(declaration=declaration):
                manifest = copy.deepcopy(MANIFEST)
                manifest["extensions"]["semantic"] = declaration
                self.assertFalse(
                    Draft202012Validator(MANIFEST_SCHEMA).is_valid(manifest)
                )

    def test_invalid_record_fields(self):
        for field, value in (
            ("relative_path", "../image.png"),
            ("relative_path", "memes/../image.png"),
            ("relative_path", "C:/image.png"),
            ("relative_path", "memes/happy/../../image.png"),
            ("content_sha256", "short"),
            ("caption", "  "),
            ("caption_status", "ready"),
            ("tags", "happy"),
        ):
            with self.subTest(field=field, value=value):
                metadata = copy.deepcopy(METADATA)
                next(iter(metadata["images"].values()))[field] = value
                self.assertFalse(
                    Draft202012Validator(SEMANTIC_SCHEMA).is_valid(metadata)
                )

    def test_unknown_metadata_version_is_invalid(self):
        metadata = copy.deepcopy(METADATA)
        metadata["schema_version"] = "999.0"
        self.assertFalse(Draft202012Validator(SEMANTIC_SCHEMA).is_valid(metadata))

    def test_fixture_file_identity(self):
        self.assertEqual(METADATA["pack_id"], MANIFEST["id"])
        for key, record in METADATA["images"].items():
            path = (PACK / record["relative_path"]).resolve()
            self.assertTrue(path.is_relative_to((PACK / "memes").resolve()))
            self.assertEqual(path.parent.name, record["category"])
            self.assertIn(record["category"], MANIFEST["categories"])
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(record["content_sha256"], digest)
            entry_id = hashlib.sha256(
                f"{digest}\0{record['category']}\0{record['relative_path']}".encode()
            ).hexdigest()
            self.assertEqual(record["entry_id"], entry_id)
            self.assertEqual(key, entry_id)


if __name__ == "__main__":
    unittest.main()
