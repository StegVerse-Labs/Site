#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))
from check_session_work_claims import active_claims, load_registry

INDEX=ROOT/"data/cosv/task-vector-index.json"
ORDER="LRUIVGOCMTBEAP"
LIFECYCLE={"UNKNOWN":0,"UNCLAIMED":1,"CLAIMED_IMPLEMENTATION":2,"CLAIMED_VALIDATION":3,"CLAIMED_INTEGRATION":4,"MACHINE_OWNED":5,"BLOCKED":6,"COMPLETE":7,"SUPERSEDED":8,"MERGED_INTO_CANONICAL_WORKSTREAM":9}

def enc(m):
    vals=[
        LIFECYCLE[m["lifecycle"]],
        1 if m["archive_ready"] else 0,
        m["unassigned_work"],m["chat_owned_implementation"],m["chat_owned_validation"],
        m["chat_owned_integration"],m["chat_owned_observation"],m["chat_owned_credentials"],
        1 if m["canonical_owner_installed"] else 0,
        1 if m["thread_required"] else 0,
        min(9,m["blocker_count"]),
        1 if m["evidence_complete"] else 0,
        1 if m["activated"] else 0,
        1 if m["propagated"] else 0,
    ]
    return "".join(str(x) for x in vals)

def main():
    idx=json.loads(INDEX.read_text())
    assert idx["profile"]=="task.v1" and idx["notation"]=="L R U I V G O C M T B E A P" and idx["width"]==14
    assert idx["authority_effect"]=="NONE"
    ids=[]
    source_bound=0
    deferred=0
    machine_owned_external=0
    terminal_external=0
    for row in idx["tasks"]:
        ids.append(row["task_id"])
        task=json.loads((ROOT/row["task_ref"]).read_text())
        rec=json.loads((ROOT/row["vector_ref"]).read_text())
        assert task["task_id"]==row["task_id"]
        assert rec["identity"]==f"StegVerse-Labs/Site:task:{row['task_id']}"
        assert rec["exact_metrics"]["symbol_order"]==ORDER
        assert rec["vector"]==row["vector"]==enc(rec["exact_metrics"])
        if row["binding_mode"]=="SOURCE_BOUND":
            source_bound += 1
            assert task["source_state_vector_ref"]==row["vector_ref"]
            assert task["machine_readable_state"]["cosv"]["vector"]==row["vector"]
            assert task["machine_readable_state"]["cosv"]["authority_effect"]=="NONE"
        elif row["binding_mode"]=="EXTERNAL_PROJECTION_SOURCE_BINDING_DEFERRED_ACTIVE_OWNER":
            deferred += 1
        elif row["binding_mode"]=="EXTERNAL_PROJECTION_MACHINE_OWNED_SOURCE":
            machine_owned_external += 1
            assert rec["exact_metrics"]["lifecycle"]=="MACHINE_OWNED"
            assert rec["exact_metrics"]["archive_ready"] is False
            assert rec["exact_metrics"]["blocker_count"] >= 1
            assert rec["exact_metrics"]["evidence_complete"] is False
            assert rec["exact_metrics"]["activated"] is False
            assert rec["exact_metrics"]["propagated"] is False
            assert task.get("archive_eligible") is False
            assert task.get("remaining")
        elif row["binding_mode"]=="EXTERNAL_PROJECTION_TERMINAL_SOURCE":
            terminal_external += 1
            assert rec["exact_metrics"]["lifecycle"]=="COMPLETE"
            assert rec["exact_metrics"]["archive_ready"] is True
            assert rec["exact_metrics"]["thread_required"] is False
            assert rec["exact_metrics"]["blocker_count"]==0
            assert rec["exact_metrics"]["evidence_complete"] is True
            assert rec["exact_metrics"]["activated"] is False
            assert rec["exact_metrics"]["propagated"] is False
            if "archive_eligible" in task:
                assert task["archive_eligible"] is True
                if "remaining" in task:
                    assert task["remaining"] == []
            elif "publication_verified" in task:
                assert task["publication_verified"] is True
                assert task.get("state")=="PUBLICATION_VERIFIED_COMPLETE"
            else:
                raise AssertionError(f"terminal external task lacks native terminal predicate: {row['task_id']}")
        else:
            raise AssertionError(f"unsupported binding mode: {row['binding_mode']}")
        assert rec["authority_effect"]=="NONE"
    assert len(ids)==len(set(ids))
    cov=idx["coverage"]
    assert cov["explicit_cosv_task_surfaces_discovered"]==5
    assert cov["task_vectors_emitted"]==len(ids)
    assert cov["source_bound_task_vectors"]==source_bound
    assert cov["repository_claim_task_vectors"]==1
    successor_rows=[row for row in idx["tasks"] if row["task_id"]=="SITE-COSV-REPOSITORY-WIDE-ADOPTION-001"]
    assert len(successor_rows)==1
    assert successor_rows[0]["binding_mode"]=="SOURCE_BOUND"
    assert successor_rows[0]["vector"]=="20010000101000"
    assert cov["external_machine_owned_source_bindings"]==machine_owned_external==1
    assert cov["active_owner_deferred_source_bindings"]==deferred
    assert cov["terminal_external_source_bindings"]==terminal_external
    assert cov["repository_active_owner_projection_vectors"]==deferred
    assert cov["legacy_claim_deferred_tasks"]==0
    assert cov["explicit_cosv_surface_gap"]==0

    registry=load_registry()
    effective_active=active_claims(registry)
    indexed_ids=set(ids)
    active_task_ids={str(claim["task_id"]) for claim in effective_active}
    unindexed_active=sorted(active_task_ids-indexed_ids)
    assert effective_active
    assert unindexed_active
    print(f"SITE_COSV_COMPUTED_COUNTS active_claims={len(effective_active)} active_task_ids={len(active_task_ids)} unindexed_active_task_ids={len(unindexed_active)}")
    assert cov["repository_effective_active_claims_observed"]==len(effective_active)
    assert cov["repository_effective_active_task_ids_observed"]==len(active_task_ids)
    assert cov["repository_unindexed_active_task_ids_observed"]==len(unindexed_active)
    assert cov["repository_active_claim_denominator_nonzero"] is True
    assert cov["repository_unindexed_active_claim_tasks_present"] is True
    assert cov["repository_vector_present_blocker"]=="UNINDEXED_ACTIVE_CLAIM_TASKS_REMAIN"
    assert cov["repository_active_task_surface_audit_complete"] is False
    assert cov["repository_vector_present_claimed"] is False
    print(f"SITE_COSV_ACTIVE_DENOMINATOR active_claims={len(effective_active)} active_task_ids={len(active_task_ids)} unindexed_active_task_ids={len(unindexed_active)}")
    print("SITE_COSV_UNINDEXED_ACTIVE_TASK_SAMPLE=" + ",".join(unindexed_active[:10]))
    print(f"SITE_COSV_TASK_PROJECTION_PASS emitted={len(ids)} source_bound={source_bound} machine_owned_external={machine_owned_external} active_owner_deferred={deferred} terminal_external={terminal_external} legacy_deferred={cov['legacy_claim_deferred_tasks']} repository_vector_present=false")

if __name__=="__main__":
    main()
