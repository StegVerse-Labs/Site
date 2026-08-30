import unittest

from scripts.project_sv_dn1_browser_evidence_intr_target import (
    ProjectionError,
    project_target,
    sha256_hex,
)


def universal():
    return {
        "schema": "stegverse.universal-intr-profiled-ingress/v1",
        "state": "ACTIVE_SOVEREIGN_INTR_INGRESS",
        "protocol": "InTr",
        "profile_path": "/intr/profile",
        "materialization_path": "/intr/materialization",
        "profiles": ["HIL:Ingress", "SV002:PublicObservation", "SV-DN1:BrowserObservation"],
        "supported_origins": [
            "STEGOS_NODE_OUTBOX",
            "TVC_RELAY_EGRESS",
            "STEGOS_WEB_BOOTSTRAP_EGRESS",
        ],
        "event_triggered": True,
        "always_on_application_receiver_required": False,
        "second_user_device_required": False,
        "g18_required": False,
        "tls_enabled": True,
        "credential_authority": "TV/TVC",
        "github_token_runtime_authority": "NONE",
        "execution_authority": "NONE",
        "authority_effect": "NONE_DISCOVERY_EVIDENCE_ONLY",
    }


def hil_compatible():
    profile = universal()
    profile.update(
        {
            "schema": "stegverse.hil-intr-materialization-ingress-profile/v1",
            "always_on_receiver_required": False,
            "direct_node_credential_requirement": "NONE",
            "direct_node_tvc_authorization_required": False,
            "exact_request_validation_required": True,
            "write_once_queue_admission": True,
            "additional_materialization_profiles": [
                "SV002:PublicObservation",
                "SV-DN1:BrowserObservation",
            ],
        }
    )
    profile.pop("profiles")
    profile.pop("always_on_application_receiver_required")
    return profile


def observation(profile):
    return {
        "schema": "stegverse.universal-intr-ingress-observation/v1",
        "observation_state": "OBSERVED_HTTPS_PROFILE",
        "observed_profile_url": "https://stegverse.org/intr/profile",
        "observed_at": "2026-08-30T22:00:00Z",
        "https_observed": True,
        "http_status": 200,
        "credential_used": False,
        "profile": profile,
        "profile_sha256": sha256_hex(profile),
        "evidence_ref": "master-records://runtime-observation/sv-dn1-example",
        "github_token_runtime_authority": "NONE",
        "execution_authority": "NONE",
        "authority_effect": "NONE_OBSERVATION_ONLY",
    }


class ProjectSVDN1TargetTests(unittest.TestCase):
    def test_universal_profile_projects_exact_target(self):
        out = project_target(observation(universal()))
        self.assertEqual(out["state"], "CONFORMING_SOVEREIGN_INTR_INGRESS")
        self.assertEqual(out["ingress_url"], "https://stegverse.org/intr/materialization")
        self.assertEqual(out["transport_origin"], "STEGOS_WEB_BOOTSTRAP_EGRESS")
        self.assertTrue(out["sv_dn1_browser_observation_profile_observed"])
        self.assertFalse(out["sdk_admission_observed"])

    def test_hil_compatible_profile_projects_target(self):
        out = project_target(observation(hil_compatible()))
        self.assertEqual(
            out["source_profile_schema"],
            "stegverse.hil-intr-materialization-ingress-profile/v1",
        )

    def test_missing_sv_dn1_profile_fails_closed(self):
        profile = universal()
        profile["profiles"] = ["HIL:Ingress", "SV002:PublicObservation"]
        obs = observation(profile)
        obs["profile_sha256"] = sha256_hex(profile)
        with self.assertRaises(ProjectionError):
            project_target(obs)

    def test_missing_web_bootstrap_origin_fails_closed(self):
        profile = universal()
        profile["supported_origins"] = ["STEGOS_NODE_OUTBOX", "TVC_RELAY_EGRESS"]
        obs = observation(profile)
        obs["profile_sha256"] = sha256_hex(profile)
        with self.assertRaises(ProjectionError):
            project_target(obs)

    def test_source_assumption_cannot_replace_https_observation(self):
        obs = observation(universal())
        obs["https_observed"] = False
        with self.assertRaises(ProjectionError):
            project_target(obs)

    def test_profile_hash_drift_fails_closed(self):
        obs = observation(universal())
        obs["profile_sha256"] = "0" * 64
        with self.assertRaises(ProjectionError):
            project_target(obs)


if __name__ == "__main__":
    unittest.main()
