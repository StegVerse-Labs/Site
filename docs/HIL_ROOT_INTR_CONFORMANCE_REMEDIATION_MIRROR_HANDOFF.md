# HIL Root InTr Conformance Remediation Mirror Handoff

Updated: 2026-09-20
Repository: `StegVerse-Labs/Site`
Parent owner: `StegVerse-Labs/Site#640` (OPEN)
Remediation child: `HIL-ROOT-INTR-CONFORMANCE-FAILURE-REMEDIATION-20260920-001`
StegHealth owner: `StegVerse-Labs/StegHealth#102`
PR: `#1429`

## Exact failure

Site PR #1425 exact head `96f591535a60dbe5db87563a90966a0c63ca7913` passed HIL-specific source checks but StegOS Node Public Observation run `35517253905`, job `106095163713`, failed because `scripts/check_hil_intr_node_sync_impl.py` required the obsolete exact literal:

```text
profiles:["KV:KnowledgeVaultInterlock","HIL:Ingress","MasterRecords:SV001Custody"]
```

Current root `intr-service-worker.js` is a larger multi-profile wrapper and still carries both required capability markers `HIL:Ingress` and `MasterRecords:SV001Custody`.

## Bounded repair

The validator now requires those two capabilities individually instead of asserting an obsolete exact list representation. Root InTr runtime source is unchanged.

## Nonclaims

This repair does not add/remove profiles, change runtime behavior, establish HIL custody/readiness, alter WorkerCoordinator, Interlock/InTr, Master Records, TV/TVC, HB, or device authority, or satisfy Site #640's authentic sovereign ingress evidence gate.

## Completion

Close this child only after exact-head Site validation passes and PR #1429 merges. Return the exact validation/merge evidence to Site #640 and StegHealth #102.

## Composed-source resolution — 2026-09-22

Successor child: `HIL-ROOT-INTR-CONFORMANCE-COMPOSED-SOURCE-RESOLUTION-20260922-001`
Claim: `SITE-HIL-ROOT-INTR-BASE-RESOLUTION-20260922`

### The remediation above was incomplete, and the claim correctly stayed open

PR #1429 merged on 2026-09-20, but its own release condition — *"the directly relevant StegOS Node Public Observation conformance path is validated"* — was never met. The `observe` job kept failing, one marker further down:

```text
HILInTrNodeSyncError:
  root_intr_contract_missing:HIL_INGRESS_SCHEMA="stegverse.hil-intr-materialization-ingress/v1"
```

Reproduced on `main` at `cc940c96` with no pull request in the picture, so it was never any one branch's failure. It has been failing every pull request that touches `stegos-node/**`.

### Same cause, one level deeper

`check_hil_intr_node_sync_impl.py` read a single file:

```python
root_intr = (root / "intr-service-worker.js").read_text(encoding="utf-8")
```

That file is a 2,327-byte wrapper. Its own header states the prior runtime is retained byte-for-byte in `intr-service-worker-base-v1.js` — 44,310 bytes — and it composes the runtime through five `importScripts` calls. Of the eleven literals `required_root_intr` asserts, nine are absent from the wrapper and all nine are present in the base. The two that pass are exactly the two #1429 added to the wrapper's compatibility block.

So #1429 repaired the first symptom of the split by copying two markers up into the wrapper. The remaining nine were never copied, and copying them would have duplicated runtime contract text into a file that does not implement it.

### The repair

`_root_intr_composed_source()` reads the wrapper and follows its own `importScripts` to the sources it composes, resolving only inside the repository root and skipping anything absent. The contract is then evaluated against the worker the browser actually runs.

Nothing is relaxed. All eleven markers are still required. Fixed-file reading is replaced by graph-following, so a further split does not reintroduce this.

### Negative controls

| control | result |
|---|---|
| marker removed from the base | fails closed, names that marker |
| wrapper stops importing the base | fails closed, names the first missing marker |
| marker removed from the wrapper only, still present in the base | passes |

The third is a deliberate and stated consequence: the contract is now over the composed worker, so a marker satisfied anywhere in that graph satisfies it. The second control is what keeps that honest — if the wrapper stops composing the base, the check fails immediately.

### Nonclaims

Validator-only. Root Universal InTr runtime source, the wrapper, and every imported extension are unchanged. No profile added or removed, no runtime, scheduler, custody store, credential path, or device dependency created. This does not establish HIL custody or readiness, and does not satisfy Site #640's authentic sovereign ingress evidence gate.

### Predecessor claim

`SITE-HIL-ROOT-INTR-CONFORMANCE-CHILD-102-20260920` is released in this change under repository owner authorization, its release condition met by this repair rather than by #1429 alone. Its `claimed_paths` and `dependency_surface_keys` transfer to the successor claim above.

The wrapper/base split has further witnesses outside this claim's surface — among them a Site test asserting `MY_KV_INSTALLATION_STATUS` against the same wrapper. They are catalogued in `Randolph_Geneaology_Hub` PR #11 and are not repaired here.
