#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "stegclaw-release-awareness.json"
TASK = ROOT / "data" / "tasks" / "SITE-STEGCLAW-V1.0.0-RELEASE-AWARENESS-905.json"
HANDOFF = ROOT / "docs" / "STEGCLAW_RELEASE_AWARENESS_MIRROR_HANDOFF.md"

def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")

def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    task = json.loads(TASK.read_text(encoding="utf-8"))
    require(HANDOFF.is_file(), "scoped handoff")
    require(data.get("schema_version") == "1.0.0", "schema_version")
    require(data.get("record_type") == "stegverse.site.stegclaw_release_awareness", "record_type")
    require(data.get("source_repository") == "Data-Continuation/StegClaw", "source_repository")
    src = data.get("source_release", {})
    require(src.get("state") == "RELEASED", "release state")
    require(src.get("version") == "1.0.0", "release version")
    require(src.get("tag_name") == "v1.0.0", "release tag")
    require(src.get("release_id") == 381434394, "release id")
    require(src.get("release_target") == "6b89a4bfb3d4c2fcc61e6cccaa4f292fb4d58cdb", "release target")
    require(src.get("validation_run") == 33650991623, "source validation run")
    require(src.get("validation_artifact_id") == 9854745757, "source validation artifact")
    upstream = data.get("upstream_propagation", {})
    require(upstream.get("state") == "PARTIAL_3_OF_4_SITE_FINAL_TARGET", "upstream propagation state")
    require(upstream.get("stegclaw_reconciliation_merge") == "2a35f0a33c59660ab0806908dd4e2fa1d1942716", "StegClaw reconciliation merge")
    require(upstream.get("stegclaw_reconciliation_validation_run") == 33660228841, "StegClaw reconciliation validation")
    for name in ("publisher","admissibility_wiki","stegguardian_wiki"):
        require(upstream.get(name, {}).get("state") == "COMPLETE_VALIDATED_MERGED", f"{name} state")
    effect = data.get("site_effect", {})
    require(effect.get("state") == "VERIFIED_RELEASE_AWARENESS_ONLY", "Site awareness state")
    for key in (
        "site_activation_authorized","runtime_proven","runtime_activation_claimed",
        "publication_authorized","release_authorized","custody_recorded",
        "provider_authorized","execution_authorized","guardian_authority","admissibility_authority"
    ):
        require(effect.get(key) is False, key)
    orch = data.get("orchestration", {})
    require(orch.get("task_id") == "SITE-STEGCLAW-V1.0.0-RELEASE-AWARENESS-905", "task id")
    require(orch.get("repository_local_task") is True, "repository local task")
    require(orch.get("external_dependencies") == [], "external dependencies")
    require(orch.get("auto_admit") is True, "auto admit")
    require(task.get("repository") == "StegVerse-Labs/Site", "task repository")
    require(task.get("state") in {"READY_FOR_MACHINE_COMPLETION_CHECK","RUNNING","COMPLETE"}, "task state")
    require(task.get("auto_admit") is True, "task auto_admit")
    require(task.get("external_dependencies") == [], "task external dependencies")
    require(data.get("authority_effect") == "NONE", "authority effect")
    require(data.get("activation_effect") is False, "activation effect")
    require(data.get("manual_user_action_required") is False, "manual user action")
    print("SITE_STEGCLAW_RELEASE_AWARENESS=PASS")
    print("SITE_STEGCLAW_RELEASE_AWARENESS_AUTHORITY_EFFECT=NONE")
    print("SITE_STEGCLAW_RELEASE_AWARENESS_ACTIVATION_EFFECT=false")

if __name__ == "__main__":
    main()
