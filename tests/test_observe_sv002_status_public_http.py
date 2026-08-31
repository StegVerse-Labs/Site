from __future__ import annotations

import unittest

from scripts.observe_sv002_status_public_http import validate


class SV002StatusPublicHttpObserverTests(unittest.TestCase):
    def valid_status(self):
        return {
            "authority_effect": "NONE_STATUS_ONLY",
            "principal_transition_semantics": {
                "authority_transfer_assumed": False,
                "authority_effect_resolution": "DERIVED_FROM_APPLICABLE_TRANSITION_ELEMENTS",
                "capability_realization_is_transition_evidence": True,
                "capability_realization_observed": False,
                "transition_effect_state": "NOT_YET_EVALUATED",
                "lifecycle_self_promotion": False,
            },
            "adjacent_lifecycle_goal": {"system_ai_active": False},
        }

    def test_valid_projection_passes(self):
        page = (
            "EXPERIMENT EFFECTS: TRANSITION-ELEMENT DERIVED\n"
            "Completing self-characterization does not self-promote StegVerse-002"
        )
        checks = validate(page, self.valid_status())
        self.assertTrue(all(checks.values()))

    def test_preclaimed_capability_fails(self):
        status = self.valid_status()
        status["principal_transition_semantics"]["capability_realization_observed"] = True
        checks = validate(
            "EXPERIMENT EFFECTS: TRANSITION-ELEMENT DERIVED "
            "Completing self-characterization does not self-promote StegVerse-002",
            status,
        )
        self.assertFalse(checks["capability_realization_not_preclaimed"])

    def test_blanket_none_effect_fails(self):
        status = self.valid_status()
        status["principal_transition_semantics"]["authority_effect_resolution"] = "NONE"
        checks = validate(
            "EXPERIMENT EFFECTS: TRANSITION-ELEMENT DERIVED "
            "Completing self-characterization does not self-promote StegVerse-002",
            status,
        )
        self.assertFalse(checks["transition_effect_resolution"])


if __name__ == "__main__":
    unittest.main()
