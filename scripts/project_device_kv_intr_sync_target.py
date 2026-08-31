#!/usr/bin/env python3
"""Project DEVICE_KV Node InTr sync target from authentic HTTPS ingress evidence."""
from __future__ import annotations

import argparse, hashlib, json
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlsplit, urlunsplit

OBSERVATION_SCHEMA="stegverse.universal-intr-ingress-observation/v1"
UNIVERSAL_PROFILE_SCHEMA="stegverse.universal-intr-profiled-ingress/v1"
TARGET_SCHEMA="stegos.site.device_kv_intr_sync_target.v1"
PROFILE_PATH="/intr/profile"
MATERIALIZATION_PATH="/intr/materialization"
RESULT_PATH="/intr/device-kv/result"
DEVICE_KV_PROFILE="KV:KnowledgeVaultInterlock"
HB_CARRIER_PROFILE_SCHEMA="stegverse.intr.hb-derived-carrier-profile/v1"
HB_CARRIER_BINDING_SCHEMA="stegverse.intr.hb-derived-carrier-binding/v1"

class ProjectionError(ValueError): pass

def require(ok:bool,reason:str)->None:
    if not ok: raise ProjectionError(reason)

def canonical_bytes(value:Any)->bytes:
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()

def sha256_hex(value:Any)->str:
    raw=value if isinstance(value,bytes) else canonical_bytes(value)
    return hashlib.sha256(raw).hexdigest()

def profile_urls(value:Any)->tuple[str,str,str]:
    require(isinstance(value,str) and bool(value),"observed_profile_url_required")
    p=urlsplit(value)
    require(p.scheme=="https","observed_profile_url_requires_https")
    require(bool(p.hostname),"observed_profile_hostname_required")
    require(not p.username and not p.password,"observed_profile_credentials_forbidden")
    require(not p.query and not p.fragment,"observed_profile_query_or_fragment_forbidden")
    require(p.path==PROFILE_PATH,"observed_profile_path_mismatch")
    origin=urlunsplit((p.scheme,p.netloc,"","",""))
    return value,origin+MATERIALIZATION_PATH,origin+RESULT_PATH

def validate_profile(profile:Mapping[str,Any])->None:
    require(profile.get("schema")==UNIVERSAL_PROFILE_SCHEMA,"profile_schema_invalid")
    expected={
      "state":"ACTIVE_SOVEREIGN_INTR_INGRESS",
      "protocol":"InTr",
      "profile_path":PROFILE_PATH,
      "materialization_path":MATERIALIZATION_PATH,
      "device_kv_result_path":RESULT_PATH,
      "event_triggered":True,
      "always_on_application_receiver_required":False,
      "second_user_device_required":False,
      "g18_required":False,
      "tls_enabled":True,
      "credential_authority":"TV/TVC",
      "github_token_runtime_authority":"NONE",
      "execution_authority":"NONE",
      "authority_effect":"NONE_DISCOVERY_EVIDENCE_ONLY",
    }
    for k,v in expected.items(): require(profile.get(k)==v,f"profile_{k}_mismatch")
    origins=profile.get("supported_origins")
    require(isinstance(origins,list) and "STEGOS_NODE_OUTBOX" in origins,"profile_direct_node_origin_missing")
    profiles=profile.get("profiles")
    require(isinstance(profiles,list) and DEVICE_KV_PROFILE in profiles,"profile_device_kv_support_missing")
    carrier=profile.get("heartbeat_derived_carrier")
    require(isinstance(carrier,Mapping),"profile_hb_carrier_missing")
    carrier_expected={
      "schema":HB_CARRIER_PROFILE_SCHEMA,
      "state":"SUPPORTED_MIGRATION_OPTIONAL",
      "fundamental_mode":"HB",
      "reference_frequency_hz":100,
      "heartbeat_period_ms":10,
      "progression_dependency":"OSCILLATOR_ONLY",
      "reference_derivation":"HB32_PROTOCOL_ANCHOR_PLUS_ELAPSED_10MS_QUANTA",
      "binding_schema":HB_CARRIER_BINDING_SCHEMA,
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
      "authority_effect":"NONE_DISCOVERY_EVIDENCE_ONLY",
    }
    for k,v in carrier_expected.items(): require(carrier.get(k)==v,f"profile_hb_carrier_{k}_mismatch")

def project_target(observation:Mapping[str,Any])->dict[str,Any]:
    require(observation.get("schema")==OBSERVATION_SCHEMA,"observation_schema_invalid")
    require(observation.get("observation_state")=="OBSERVED_HTTPS_PROFILE","observation_state_invalid")
    require(observation.get("https_observed") is True,"https_observation_required")
    require(observation.get("http_status")==200,"profile_http_status_mismatch")
    require(observation.get("credential_used") is False,"profile_observation_credential_forbidden")
    require(observation.get("github_token_runtime_authority")=="NONE","observation_github_runtime_authority_forbidden")
    require(observation.get("execution_authority")=="NONE","observation_execution_authority_forbidden")
    require(observation.get("authority_effect")=="NONE_OBSERVATION_ONLY","observation_authority_effect_invalid")
    require(isinstance(observation.get("observed_at"),str) and observation["observed_at"],"observed_at_required")
    require(isinstance(observation.get("evidence_ref"),str) and observation["evidence_ref"],"evidence_ref_required")
    profile_url,ingress_url,result_url=profile_urls(observation.get("observed_profile_url"))
    profile=observation.get("profile")
    require(isinstance(profile,Mapping),"profile_object_required")
    validate_profile(profile)
    actual=sha256_hex(profile)
    require(observation.get("profile_sha256")==actual,"profile_sha256_mismatch")
    return {
      "schema":TARGET_SCHEMA,
      "state":"CONFORMING_SOVEREIGN_INTR_INGRESS",
      "ingress_url":ingress_url,
      "result_url":result_url,
      "transport_origin":"STEGOS_NODE_OUTBOX",
      "runtime_ingress_observed":True,
      "configuration_authority":"StegVerse sovereign profiled InTr runtime evidence projection",
      "credential_authority":"TV/TVC",
      "credential_requirement":"NONE",
      "github_token_runtime_authority":"NONE",
      "execution_authority":"NONE",
      "authority_effect":"NONE_DISCOVERY_ONLY",
      "source_profile_url":profile_url,
      "source_profile_schema":profile["schema"],
      "source_profile_sha256":actual,
      "runtime_profile_observed_at":observation["observed_at"],
      "runtime_profile_evidence_ref":observation["evidence_ref"],
      "device_kv_materialization_profile_observed":True,
      "hb_derived_carrier_profile_observed":True,
      "hb_derived_carrier_profile_schema":profile["heartbeat_derived_carrier"]["schema"],
      "hb_derived_carrier_binding_schema":profile["heartbeat_derived_carrier"]["binding_schema"],
      "hb_derived_carrier_channel_count":profile["heartbeat_derived_carrier"]["channel_count"],
      "hb_derived_carrier_grants_authority":False,
      "runtime_materialization_observed":False,
      "canonical_kv_staging_observed":False,
      "trusted_semantic_admission_observed":False,
      "provider_session_observed":False,
      "g18_completion_required":False,
    }

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument("observation",type=Path)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    value=json.loads(a.observation.read_text())
    require(isinstance(value,dict),"observation_object_required")
    target=project_target(value)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(target,indent=2,sort_keys=True)+"\n")
    print(json.dumps(target,sort_keys=True))
    return 0

if __name__=="__main__": raise SystemExit(main())
