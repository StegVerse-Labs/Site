import copy
import unittest
from scripts.project_sv002_intr_sync_target import project_target, sha256_hex, ProjectionError

def universal():
    return {
        "schema":"stegverse.universal-intr-profiled-ingress/v1",
        "state":"ACTIVE_SOVEREIGN_INTR_INGRESS","protocol":"InTr",
        "profile_path":"/intr/profile","materialization_path":"/intr/materialization",
        "profiles":["HIL:Ingress","SV002:PublicObservation"],
        "heartbeat_derived_carrier":{
            "schema":"stegverse.intr.hb-derived-carrier-profile/v1",
            "state":"SUPPORTED_MIGRATION_OPTIONAL",
            "fundamental_mode":"HB",
            "reference_frequency_hz":100,
            "heartbeat_period_ms":10,
            "progression_dependency":"OSCILLATOR_ONLY",
            "reference_derivation":"HB32_PROTOCOL_ANCHOR_PLUS_ELAPSED_10MS_QUANTA",
            "binding_schema":"stegverse.intr.hb-derived-carrier-binding/v1",
            "channel_family":"H1_PHASE_SLOTS",
            "channel_count":16,
            "channel_selection":"PAYLOAD_SHA256_FIRST64_MOD_16",
            "carrier_binding_required":False,
            "legacy_unbound_packets_temporarily_accepted":True,
            "carrier_presence_grants_admission_authority":False,
            "carrier_presence_grants_execution_authority":False,
            "carrier_presence_grants_credential_authority":False,
            "carrier_presence_grants_routing_authority":False,
            "carrier_presence_grants_transition_authority":False,
            "carrier_presence_grants_receiving_authority":False,
            "credential_authority":"TV/TVC",
            "authority_effect":"NONE_DISCOVERY_EVIDENCE_ONLY"
        },
        "supported_origins":["STEGOS_NODE_OUTBOX","TVC_RELAY_EGRESS"],
        "event_triggered":True,"always_on_application_receiver_required":False,
        "second_user_device_required":False,"g18_required":False,"tls_enabled":True,
        "credential_authority":"TV/TVC","github_token_runtime_authority":"NONE",
        "execution_authority":"NONE","authority_effect":"NONE_DISCOVERY_EVIDENCE_ONLY"
    }

def hil():
    p=universal()
    p.update({
        "schema":"stegverse.hil-intr-materialization-ingress-profile/v1",
        "always_on_receiver_required":False,
        "direct_node_credential_requirement":"NONE",
        "direct_node_tvc_authorization_required":False,
        "exact_request_validation_required":True,
        "write_once_queue_admission":True,
        "additional_materialization_profiles":["SV002:PublicObservation"],
    })
    p.pop("profiles");p.pop("always_on_application_receiver_required")
    return p

def observation(profile):
    return {
        "schema":"stegverse.universal-intr-ingress-observation/v1",
        "observation_state":"OBSERVED_HTTPS_PROFILE",
        "observed_profile_url":"https://stegverse.org/intr/profile",
        "observed_at":"2026-08-30T14:00:00Z",
        "https_observed":True,"http_status":200,"credential_used":False,
        "profile":profile,"profile_sha256":sha256_hex(profile),
        "evidence_ref":"master-records://runtime-observation/example",
        "github_token_runtime_authority":"NONE","execution_authority":"NONE",
        "authority_effect":"NONE_OBSERVATION_ONLY"
    }

class ProjectorTests(unittest.TestCase):
    def test_universal_profile_projects_sv002_target(self):
        out=project_target(observation(universal()))
        self.assertEqual(out["state"],"CONFORMING_SOVEREIGN_INTR_INGRESS")
        self.assertEqual(out["ingress_url"],"https://stegverse.org/intr/materialization")
        self.assertTrue(out["sv002_materialization_profile_observed"])
        self.assertTrue(out["hb_derived_carrier_profile_observed"])
        self.assertEqual(out["hb_derived_carrier_binding_schema"],"stegverse.intr.hb-derived-carrier-binding/v1")
        self.assertFalse(out["hb_derived_carrier_grants_authority"])
        self.assertFalse(out["receiver_readiness_observed"])

    def test_hil_compat_profile_projects_sv002_target(self):
        out=project_target(observation(hil()))
        self.assertEqual(out["source_profile_schema"],"stegverse.hil-intr-materialization-ingress-profile/v1")
        self.assertFalse(out["hb_derived_carrier_profile_observed"])

    def test_universal_profile_missing_or_authorizing_carrier_fails_closed(self):
        p=universal(); del p["heartbeat_derived_carrier"]
        o=observation(p); o["profile_sha256"]=sha256_hex(p)
        with self.assertRaises(ProjectionError): project_target(o)
        p=universal(); p["heartbeat_derived_carrier"]["carrier_presence_grants_routing_authority"]=True
        o=observation(p); o["profile_sha256"]=sha256_hex(p)
        with self.assertRaises(ProjectionError): project_target(o)

    def test_missing_sv002_profile_fails_closed(self):
        p=universal();p["profiles"]=["HIL:Ingress"]
        o=observation(p);o["profile_sha256"]=sha256_hex(p)
        with self.assertRaises(ProjectionError):project_target(o)

    def test_source_assumption_cannot_replace_https_observation(self):
        o=observation(universal());o["https_observed"]=False
        with self.assertRaises(ProjectionError):project_target(o)

    def test_profile_hash_drift_fails_closed(self):
        o=observation(universal());o["profile_sha256"]="0"*64
        with self.assertRaises(ProjectionError):project_target(o)

if __name__=="__main__":
    unittest.main()
