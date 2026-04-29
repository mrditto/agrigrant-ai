import json
import unittest
from pathlib import Path
from uuid import uuid4

from grants import load_grants_data


class LoadGrantsDataTests(unittest.TestCase):
    def write_database(self, payload):
        temp_dir = Path(__file__).with_name(".test_tmp") / str(uuid4())
        temp_dir.mkdir(parents=True, exist_ok=True)
        path = temp_dir / "grants_database.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        self.addCleanup(temp_dir.rmdir)
        self.addCleanup(path.unlink)
        return path

    def test_loads_valid_grants(self):
        path = self.write_database(
            {
                "grants": [
                    {
                        "name": "Test Grant",
                        "agency": "USDA",
                        "description": "Example description",
                        "max_funding": "$100",
                        "url": "https://example.com/grant",
                    }
                ]
            }
        )

        grants = load_grants_data(path)

        self.assertEqual(1, len(grants))
        self.assertEqual("Test Grant", grants[0]["name"])

    def test_rejects_missing_grants_list(self):
        path = self.write_database({"items": []})

        with self.assertRaisesRegex(RuntimeError, "Grant database format is invalid."):
            load_grants_data(path)

    def test_rejects_malformed_grant_record(self):
        path = self.write_database(
            {
                "grants": [
                    {
                        "name": "Broken Grant",
                        "agency": "USDA",
                        "description": "Missing a URL",
                        "max_funding": "$100",
                    }
                ]
            }
        )

        with self.assertRaisesRegex(RuntimeError, "missing required fields: url"):
            load_grants_data(path)


if __name__ == "__main__":
    unittest.main()
