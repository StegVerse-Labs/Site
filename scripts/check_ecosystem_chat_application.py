#!/usr/bin/env python3
"""Run the canonical Site application validation checks.

Live public-route checks are intentionally excluded from this pre-deployment
aggregate. They run after Pages deployment in the existing Site Task Runner,
where the deployment can be observed without creating a circular dependency.
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from typing import Sequence
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'site_application_validation.result.json'
COMMANDS: tuple[tuple[str,...],...]=(
(sys.executable,'scripts/check_ecosystem_chat_navigation.py'),
(sys.executable,'scripts/check_stegwallet_crypto_goals.py'),
(sys.executable,'scripts/check_stegwallet_base_app_surface.py'),
(sys.executable,'scripts/check_stegwallet_base_dev_publication.py'),
(sys.executable,'scripts/check_stegwallet_browser_readiness.py'),
(sys.executable,'scripts/check_stegwallet_siwe_client.py'),
(sys.executable,'scripts/check_stegwallet_siwe_promotion_gate.py'),
(sys.executable,'scripts/check_stegverse_local_node_binding.py'),
(sys.executable,'scripts/check_ecosystem_node_dual_view.py'),
(sys.executable,'scripts/check_ecosystem_node_replay_and_disclosure.py'),
(sys.executable,'scripts/check_stegmusic_playable_slice.py'),
(sys.executable,'scripts/check_stegmusic_adaptive_model.py'),
(sys.executable,'scripts/check_stegmusic_cultural_performance_model.py'),
(sys.executable,'scripts/check_stegmusic_string_component_standard.py'),
(sys.executable,'scripts/check_stegmusic_instrument_component_standard.py'),
(sys.executable,'scripts/check_stegmusic_source_study_algorithm.py'),
(sys.executable,'scripts/check_stegmusic_reference_schemas.py'),
(sys.executable,'scripts/check_stegmusic_source_field_crosswalk.py'),
(sys.executable,'scripts/check_stegmusic_source_evidence_runtime.py'),
(sys.executable,'scripts/check_stegmusic_live_verification_contract.py'),
(sys.executable,'scripts/check_stegmusic_browser_self_test.py'),
(sys.executable,'scripts/check_stegmusic_browser_automation_contract.py'),
(sys.executable,'scripts/check_stegmusic_profile_isolation_accessibility.py'),
(sys.executable,'scripts/check_chat_session_launcher.py'),
(sys.executable,'scripts/check_ecosystem_usage_auth_contract.py'),
(sys.executable,'scripts/check_ecosystem_usage_ledger.py'),
(sys.executable,'scripts/check_llm_adapter_usage_endpoint_handoff.py'),
(sys.executable,'scripts/check_llm_adapter_usage_endpoint_conformance.py'),
(sys.executable,'scripts/check_usage_endpoint_activation_evidence.py'),
(sys.executable,'scripts/check_usage_endpoint_preactivation_checkpoint.py'),
(sys.executable,'scripts/check_ecosystem_chat_activation_receipt_import.py'),
(sys.executable,'scripts/check_site_current_main_validation_evidence.py'),
(sys.executable,'scripts/check_site_current_main_validation_receipt_writer.py'),
(sys.executable,'scripts/check_site_validation_artifact_manifest_writer.py'),
(sys.executable,'scripts/check_site_validation_artifact_bundle_verifier.py'),
(sys.executable,'scripts/check_ecosystem_comparison.py'),
(sys.executable,'scripts/check_governed_transition_observatory.py'),
(sys.executable,'scripts/check_external_chat_compatibility.py'),
(sys.executable,'scripts/check_external_review_console.py'),
(sys.executable,'scripts/check_external_chat_verification_phase.py'),
(sys.executable,'scripts/check_external_chat_activation_evidence.py'),
(sys.executable,'scripts/check_external_chat_activation_request.py'),
(sys.executable,'scripts/check_framework_evaluations.py'),
(sys.executable,'scripts/check_framework_evaluation_replay.py'),
(sys.executable,'scripts/check_stegverse_live_baseline_readiness.py'),
(sys.executable,'scripts/check_stegverse_live_baseline_execution_request.py'),
(sys.executable,'scripts/check_stegverse_live_baseline_handoff.py'),
(sys.executable,'scripts/generate_framework_evaluation_receipts.py'),
(sys.executable,'scripts/check_framework_evaluation_receipts.py'),
(sys.executable,'scripts/check_ecosystem_chat_ai_entry_full.py'),
(sys.executable,'scripts/check_ai_entry_ui_activation_status.py'),
(sys.executable,'scripts/check_ai_entry_application_page.py'),
(sys.executable,'scripts/check_ai_entry_application_completion.py'),
(sys.executable,'scripts/check_ai_entry_backend_activation_boundary.py'),
(sys.executable,'scripts/check_ai_entry_activation_routes.py'),
(sys.executable,'scripts/check_ai_entry_backend_activation_fixtures.py'),
(sys.executable,'scripts/check_ai_entry_ui_activation_routes.py'),
(sys.executable,'scripts/check_ai_entry_backend_activation_progress.py'),
(sys.executable,'scripts/check_ai_entry_ci_visibility.py'),
(sys.executable,'scripts/check_ai_entry_authority_service_boundary.py'),
(sys.executable,'scripts/check_ai_entry_authority_decision_fixtures.py'),
(sys.executable,'scripts/check_ai_entry_operator_recoverability_boundary.py'),
(sys.executable,'scripts/check_ai_entry_recovery_state_fixtures.py'),
(sys.executable,'scripts/check_ai_entry_recovery_completion.py'),
(sys.executable,'scripts/check_ai_entry_cross_repo_handoff.py'),
(sys.executable,'scripts/check_ai_entry_green_run_visibility_consolidation.py'),
(sys.executable,'scripts/check_ai_entry_release_readiness_lockfile.py'),
(sys.executable,'scripts/check_ai_entry_tag_gate.py'),
(sys.executable,'scripts/check_ai_entry_final_handoff_index.py'),
(sys.executable,'scripts/check_ai_entry_next_path_gate.py'),
(sys.executable,'scripts/check_ai_entry_visibility_recheck_index.py'),
(sys.executable,'scripts/check_ai_entry_runtime_design_packet.py'),
(sys.executable,'scripts/check_ai_entry_runtime_design_fixtures.py'),
(sys.executable,'scripts/check_ai_entry_runtime_design_completion.py'),
(sys.executable,'scripts/check_ai_entry_green_data_packet.py'),
(sys.executable,'scripts/check_ai_entry_proposal_completion.py'),
(sys.executable,'scripts/check_ai_entry_no_manual_closure.py'),
(sys.executable,'scripts/check_ai_entry_visible_green_monitor_goal.py'),
(sys.executable,'scripts/check_ai_entry_design_only_refinement.py'),
(sys.executable,'scripts/check_ai_entry_design_only_refinement_completion.py'),
(sys.executable,'scripts/check_ai_entry_stable_archive_checkpoint.py'),
(sys.executable,'scripts/check_ai_entry_post_archive_monitor.py'),
(sys.executable,'scripts/check_ai_entry_post_archive_monitor_completion.py'),
(sys.executable,'scripts/check_ai_entry_loop_checkpoint.py'),
(sys.executable,'scripts/check_ai_entry_loop_checkpoint_completion.py'),
(sys.executable,'scripts/check_ai_entry_loop_cycle_record.py'),
(sys.executable,'scripts/check_ai_entry_supported_validation_commands.py'),
(sys.executable,'scripts/check_ai_entry_rerun_validation_confirmation.py'),
(sys.executable,'scripts/check_ai_entry_infrastructure_stabilization.py'),
(sys.executable,'scripts/check_ai_entry_cross_repo_promotion_record.py'),
(sys.executable,'scripts/check_cross_wiki_metadata_graph_status.py'),
(sys.executable,'scripts/check_site_media_pipeline_mirror.py'),
(sys.executable,'scripts/check_publication_manifest.py'),
(sys.executable,'scripts/check_media_pipeline_downstream_publication.py'),)
def execute(command:Sequence[str])->subprocess.CompletedProcess[str]: return subprocess.run(list(command),cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False)
def write_result(payload:dict)->None: RESULT.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
def main()->int:
    passed=[]
    for command in COMMANDS:
        label=' '.join(command); completed=execute(command)
        if completed.returncode!=0:
            payload={'schema_version':'1.0.0','status_type':'site_application_validation_result','passed':False,'failed_command':label,'returncode':completed.returncode,'output':completed.stdout.rstrip(),'passed_commands':passed,'live_route_verification_phase':'POST_DEPLOYMENT'}; write_result(payload); print(f'SITE_APPLICATION_CHECK_FAIL: {label}'); print(completed.stdout.rstrip()); return completed.returncode
        passed.append(label); print(f'SITE_APPLICATION_CHECK_PASS: {label}')
    write_result({'schema_version':'1.0.0','status_type':'site_application_validation_result','passed':True,'failed_command':None,'returncode':0,'output':'ECOSYSTEM_CHAT_APPLICATION_PASS','passed_commands':passed,'live_route_verification_phase':'POST_DEPLOYMENT'}); print('ECOSYSTEM_CHAT_APPLICATION_PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
