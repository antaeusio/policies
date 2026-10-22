import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from verify import ROOT, verify_repository


class CandidateIntegrity(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copy(ROOT / "catalog.json", self.root / "catalog.json")
        shutil.copytree(ROOT / "policies", self.root / "policies")
        self.catalog = json.loads((self.root / "catalog.json").read_text())
        self.entry = self.catalog["versions"][0]
        self.folder = self.root / "policies" / self.entry["source_id"] / "versions" / self.entry["version_id"]

    def save(self):
        (self.root / "catalog.json").write_text(json.dumps(self.catalog))

    def rewrite(self, name, change):
        path = self.folder / name
        value = json.loads(path.read_text())
        change(value)
        path.write_text(json.dumps(value))
        self.entry["files"][name] = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        self.save()

    def test_candidate_is_consistent(self):
        self.assertEqual(verify_repository(self.root), (25, 1))

    def browser_provenance(self):
        # Synthetic metadata only: never a real source observation or new artifact.
        value = json.loads((self.folder / "provenance.json").read_text())
        value["schema_version"] = "2"
        for key in ["response_sha256", "extracted_text_sha256", "extractor"]:
            del value[key]
        value["observation"] = {
            "method": "browser-dom", "selector": ".synthetic-article", "element_index": 0,
            "matched_elements": 2, "text_property": "innerText", "normalization": "none",
            "text_sha256": hashlib.sha256(b"Synthetic observation.").hexdigest(), "text_bytes": 22,
            "http_response_sha256": None, "response_linkage": "not-established",
            "authentication": "public-no-sign-in",
        }
        return value

    def test_browser_observation_candidate_is_offline_only_and_consistent(self):
        value = self.browser_provenance()
        self.rewrite("provenance.json", lambda p: (p.clear(), p.update(value)))
        self.assertEqual(verify_repository(self.root), (25, 1))
        self.assertEqual(self.entry["state"], "candidate")
        self.assertEqual(self.entry["semantic_evaluation"], "not_evaluated")

    def test_browser_observation_cannot_assert_a_response_chain_or_private_session(self):
        original = self.browser_provenance()
        for key, value in [("http_response_sha256", "a" * 64), ("response_linkage", "verified"),
                           ("method", "https-response"), ("text_property", "innerHTML"),
                           ("normalization", "trim"), ("authentication", "signed-in"),
                           ("selector", " "), ("selector", "x" * 1001),
                           ("cookie", "synthetic-value"), ("text", "Third-party snapshot")]:
            with self.subTest(field=key):
                replacement = copy.deepcopy(original)
                replacement["observation"][key] = value
                self.rewrite("provenance.json", lambda p: (p.clear(), p.update(replacement)))
                with self.assertRaises(ValueError):
                    verify_repository(self.root)

    def test_browser_observation_requires_bounded_exact_identity(self):
        original = self.browser_provenance()
        for key, value in [("matched_elements", True), ("matched_elements", 0), ("matched_elements", 257),
                           ("element_index", False), ("element_index", -1), ("element_index", 2),
                           ("text_bytes", True), ("text_bytes", 0), ("text_bytes", 1048577),
                           ("text_sha256", "sha256:" + "a" * 64), ("text_sha256", "A" * 64)]:
            with self.subTest(field=key, value=value):
                replacement = copy.deepcopy(original)
                replacement["observation"][key] = value
                self.rewrite("provenance.json", lambda p: (p.clear(), p.update(replacement)))
                with self.assertRaisesRegex(ValueError, "browser observation identity"):
                    verify_repository(self.root)

    def test_browser_and_response_provenance_formats_cannot_be_mixed(self):
        original = self.browser_provenance()
        for change in [{"response_sha256": "a" * 64}, {"extracted_text_sha256": "a" * 64},
                       {"extractor": "fake-http-chain"}, {"schema_version": "1"}, {"schema_version": "3"}]:
            with self.subTest(change=change):
                replacement = copy.deepcopy(original)
                replacement.update(change)
                self.rewrite("provenance.json", lambda p: (p.clear(), p.update(replacement)))
                with self.assertRaises(ValueError):
                    verify_repository(self.root)

    def test_browser_format_does_not_bypass_common_candidate_assertions(self):
        original = self.browser_provenance()
        for change in [{"source_url": "https://example.org/other"}, {"semantic_evaluation": "passed"},
                       {"source_snapshot_retained": True}, {"cli_version": "0.6.0"},
                       {"authoring": {"method": "generated", "tool": "synthetic", "model": "synthetic", "revision": "synthetic"}},
                       {"schema_version": []}]:
            with self.subTest(change=change):
                replacement = copy.deepcopy(original)
                replacement.update(change)
                self.rewrite("provenance.json", lambda p: (p.clear(), p.update(replacement)))
                with self.assertRaises(ValueError):
                    verify_repository(self.root)

    def test_browser_provenance_cannot_replace_published_format_one_history(self):
        previous = copy.deepcopy(self.catalog)
        value = self.browser_provenance()
        self.rewrite("provenance.json", lambda p: (p.clear(), p.update(value)))
        with patch("verify.subprocess.check_output", return_value=json.dumps(previous).encode()):
            with self.assertRaisesRegex(ValueError, "published version altered"):
                verify_repository(self.root, base_ref="trusted-base")

    def test_changed_bytes_are_detected(self):
        with (self.folder / "README.md").open("a") as stream:
            stream.write("altered")
        with self.assertRaisesRegex(ValueError, "immutable file"):
            verify_repository(self.root)

    def test_repinning_old_bytes_cannot_rewrite_published_history(self):
        previous = copy.deepcopy(self.catalog)
        path = self.folder / "README.md"
        path.write_text(path.read_text() + "altered")
        self.entry["files"]["README.md"] = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        self.save()
        with patch("verify.subprocess.check_output", return_value=json.dumps(previous).encode()):
            with self.assertRaisesRegex(ValueError, "published version altered"):
                verify_repository(self.root, base_ref="trusted-base")

    def test_unqualified_promotion_is_rejected(self):
        for field, value in [("state", "maintainer_reviewed"), ("semantic_evaluation", "passed")]:
            with self.subTest(field=field):
                original = self.entry[field]
                self.entry[field] = value
                self.save()
                with self.assertRaisesRegex(ValueError, "publication/review assertion"):
                    verify_repository(self.root)
                self.entry[field] = original

    def test_directory_traversal_is_rejected(self):
        self.entry["version_id"] = "../../other"
        self.save()
        with self.assertRaisesRegex(ValueError, "version identity"):
            verify_repository(self.root)

    def test_symlink_cannot_substitute_version_file(self):
        path = self.folder / "README.md"
        other = self.root / "other.md"
        path.rename(other)
        path.symlink_to(other)
        with self.assertRaisesRegex(ValueError, "immutable file"):
            verify_repository(self.root)

    def test_unindexed_version_is_rejected(self):
        (self.folder.parent / "2026-10-22.2").mkdir()
        with self.assertRaisesRegex(ValueError, "unindexed"):
            verify_repository(self.root)

    def test_fixture_input_digest_mismatch_survives_repinning(self):
        self.rewrite("cases.json", lambda suite: suite["cases"][0]["input"].update(text="Different synthetic input"))
        with self.assertRaisesRegex(ValueError, "fixture binding"):
            verify_repository(self.root)

    def test_missing_rule_mapping_survives_repinning(self):
        def remove(coverage):
            for clause in coverage["clauses"]:
                clause["rule_ids"] = [rid for rid in clause["rule_ids"] if rid != "chance-entry"]
                if clause["status"] == "converted" and not clause["rule_ids"]:
                    clause["status"] = "out_of_scope"
        self.rewrite("coverage.json", remove)
        with self.assertRaisesRegex(ValueError, "unmapped rule"):
            verify_repository(self.root)

    def test_missing_rule_evidence_survives_repinning(self):
        self.rewrite("fixtures.json", lambda fixtures: fixtures["cases"][0]["ruleResults"].pop())
        with self.assertRaisesRegex(ValueError, "fixture binding"):
            verify_repository(self.root)

    def test_source_identity_cannot_drift(self):
        self.rewrite("provenance.json", lambda provenance: provenance.update(source_url="https://example.org/other"))
        with self.assertRaisesRegex(ValueError, "provenance assertion"):
            verify_repository(self.root)

    def test_provenance_requires_nonempty_observation_and_authoring_text(self):
        original = json.loads((self.folder / "provenance.json").read_text())
        for field in ["language", "region", "extractor", "scope", "tool", "model", "revision"]:
            for value in [None, "", " \t"]:
                with self.subTest(field=field, value=value):
                    replacement = copy.deepcopy(original)
                    target = replacement["authoring"] if field in {"tool", "model", "revision"} else replacement
                    target[field] = value
                    self.rewrite("provenance.json", lambda p: p.update(replacement))
                    with self.assertRaisesRegex(ValueError, "text identity"):
                        verify_repository(self.root)

    def test_retrieval_timestamp_requires_a_real_date_and_timezone(self):
        original = json.loads((self.folder / "provenance.json").read_text())
        for value in [None, "", "2026-10-22", "2026-10-22T14:36:47", "2026-99-22T14:36:47Z"]:
            with self.subTest(value=value):
                replacement = copy.deepcopy(original)
                replacement["retrieved_at"] = value
                self.rewrite("provenance.json", lambda p: p.update(replacement))
                with self.assertRaisesRegex(ValueError, "observation/effective date"):
                    verify_repository(self.root)

    def test_effective_date_is_null_or_valid_iso_date(self):
        original = json.loads((self.folder / "provenance.json").read_text())
        for value in ["", "2026-02-30", "2026-10-22T14:36:47Z", 20261022]:
            with self.subTest(value=value):
                replacement = copy.deepcopy(original)
                replacement["source_effective_date"] = value
                self.rewrite("provenance.json", lambda p: p.update(replacement))
                with self.assertRaisesRegex(ValueError, "observation/effective date"):
                    verify_repository(self.root)


if __name__ == "__main__":
    unittest.main()
