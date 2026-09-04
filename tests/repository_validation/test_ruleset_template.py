"""Test the proposed import configuration, not GitHub's live state."""

import json
import unittest
from pathlib import Path


class MainRulesetTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[2] / "config" / "main-ruleset.json"
        cls.config = json.loads(path.read_text(encoding="utf-8"))
        cls.rules = {rule["type"]: rule for rule in cls.config["rules"]}

    def test_targets_only_main(self):
        self.assertEqual(self.config["target"], "branch")
        self.assertEqual(self.config["conditions"], {
            "ref_name": {"include": ["refs/heads/main"], "exclude": []}
        })

    def test_active_without_bypass(self):
        self.assertEqual(self.config["enforcement"], "active")
        self.assertEqual(self.config["bypass_actors"], [])

    def test_pull_request_does_not_require_a_second_operator(self):
        params = self.rules["pull_request"]["parameters"]
        self.assertEqual(params["required_approving_review_count"], 0)
        self.assertFalse(params["require_code_owner_review"])
        self.assertFalse(params["require_last_push_approval"])
        self.assertTrue(params["required_review_thread_resolution"])

    def test_requires_exact_governance_check_on_current_base(self):
        params = self.rules["required_status_checks"]["parameters"]
        self.assertEqual(params["required_status_checks"], [
            {"context": "repository-governance"}
        ])
        self.assertTrue(params["strict_required_status_checks_policy"])
        self.assertFalse(params["do_not_enforce_on_create"])

    def test_blocks_deletion_and_force_push(self):
        self.assertIn("deletion", self.rules)
        self.assertIn("non_fast_forward", self.rules)

    def test_does_not_add_update_lock_or_duplicate_rules(self):
        self.assertEqual(len(self.rules), len(self.config["rules"]))
        self.assertEqual(set(self.rules), {
            "deletion", "non_fast_forward", "pull_request", "required_status_checks"
        })


if __name__ == "__main__":
    unittest.main()
