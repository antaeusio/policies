import copy
import json
import unittest
from verify import ROOT, public_url, unique_object, verify


class CatalogVerification(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / "catalog.json").read_text())

    def test_registered_sources_cannot_be_advertised_as_usable(self):
        for change in ({"status": "reviewed"}, {"current_version": "unverified"}):
            catalog = copy.deepcopy(self.catalog)
            catalog["sources"][0].update(change)
            with self.assertRaises(ValueError):
                verify(catalog)

    def test_credentials_signed_queries_and_private_urls_rejected(self):
        for url in ("http://example.org", "https://user:pass@example.org", "https://127.0.0.1/",
                    "https://[::1]/", "https://2130706433/", "https://host.internal/",
                    "https://example.org/?%73ig=private", "https://example.org/?X-Amz-Signature=private",
                    "https://example.org/?token=private", "https://example.org\\@localhost/",
                    "https://example.org/?password=synthetic", "https://example.org/?PaSsWd=synthetic",
                    "https://example.org/?%70wd=synthetic", "https://example.org/?%70assword=synthetic",
                    "https://example.org:8443/", "https://example.org./"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                public_url(url)
        self.assertEqual(public_url("https://example.org/Rules?region=EU"), "https://example.org/Rules?region=EU")

    def test_duplicate_json_keys_and_source_identities_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"sources":[],"sources":[]}', object_pairs_hook=unique_object)
        catalog = copy.deepcopy(self.catalog)
        catalog["sources"].append(catalog["sources"][0])
        with self.assertRaises(ValueError):
            verify(catalog)

    def test_unknown_fields_rejected(self):
        catalog = copy.deepcopy(self.catalog)
        catalog["sources"][0]["visitor_text"] = "Synthetic data that does not belong in the catalog"
        with self.assertRaises(ValueError):
            verify(catalog)


if __name__ == "__main__":
    unittest.main()
