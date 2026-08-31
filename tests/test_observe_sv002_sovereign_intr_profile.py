from __future__ import annotations

import unittest

from scripts.observe_sv002_sovereign_intr_profile import (
    HB_BINDING_SCHEMA,
    HB_PROFILE_SCHEMA,
    UNIVERSAL_SCHEMA,
    validate_profile,
)


class SV002SovereignInTrProfileObserverTests(unittest.TestCase):
    def profile(self):
        return {
            "schema": UNIVERSAL_SCHEMA,
            "state": "ACTIVE_SOVEREIGN_INTR_INGRESS",
            "protocol": "InTr",
            "profile_path": "/intr/profile",
            "materialization_path": "/intr/materialization",
            "event_triggered": True,
            "second_user_device_required": False,
            "g18_required": False,
            "tls_enabled": True,
            "credential_authority": "TV/TVC",
            "github_token_runtime_authority": "NONE",
            "execution_authority": "NONE",
            "authority_effect": "NONE_DISCOVERY_EVIDENCE_ONLY",
            "supported_origins": ["STEGOS_NODE_OUTBOX"],
            "always_on_application_receiver_required": False,
            "profiles": ["SV002:PublicObservation"],
            "heartbeat_derived_carrier": {
                "schema": HB_PROFILE_SCHEMA,
                "binding_schema": HB_BINDING_SCHEMA,
                "reference_frequency_hz": 100,
                "heartbeat_period_ms": 10,
                "progression_dependency": "OSCILLATOR_ONLY",
                "channel_family": "H1_PHASE_SLOTS",
                "channel_count": 16,
                "channel_selection": "PAYLOAD_SHA256_FIRST64_MOD_16",
                "carrier_presence_grants_admission_authority": False,
                "carrier_presence_grants_execution_authority": False,
                "carrier_presence_grants_credential_authority": False,
                "carrier_presence_grants_routing_authority": False,
                "carrier_presence_grants_transition_authority": False,
                "carrier_presence_grants_receiving_authority": False,
            },
        }

    def test_canonical_profile_passes(self):
        self.assertTrue(all(validate_profile(self.profile()).values()))

    def test_missing_sv002_support_fails(self):
        profile = self.profile()
        profile["profiles"] = []
        self.assertFalse(validate_profile(profile)["sv002_profile_advertised"])

    def test_wrong_carrier_channel_rule_fails(self):
        profile = self.profile()
        profile["heartbeat_derived_carrier"]["channel_selection"] = "SHA256_PACKET_ID"
        self.assertFalse(validate_profile(profile)["hb_channel_selection"])

    def test_carrier_authority_fails(self):
        profile = self.profile()
        profile["heartbeat_derived_carrier"][
            "carrier_presence_grants_routing_authority"
        ] = True
        self.assertFalse(validate_profile(profile)["hb_carrier_non_authorizing"])


if __name__ == "__main__":
    unittest.main()
