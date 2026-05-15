"""
StegVerse Genealogy Hub v1.0
Sovereign identity ledger with public sharing and viral fork.
Integrates with Knowledge Vault for private-state storage.
Serves as template for 'Create your own Genealogy Hub!' flow.
"""

import json
import hashlib
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# CID format: <NS>-<BirthYear>-<Sequence>-<BirthState>
# e.g.  RND-1796-001-TN

EVIDENCE_GRADES = {
    "A": "Primary Record (Original document)",
    "B": "Transcribed Primary",
    "C": "Secondary Published Source",
    "D": "Family Narrative / Unsourced",
}

SCHEMA = "stegverse_genealogy_hub.v1"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


# ── CID utilities ─────────────────────────────────────────────────────────────

def make_cid(namespace: str, birth_year: int, sequence: int, birth_state: str) -> str:
    return f"{namespace.upper()}-{birth_year}-{str(sequence).zfill(3)}-{birth_state.upper()}"

def validate_cid(cid: str) -> bool:
    parts = cid.split("-")
    return len(parts) == 4 and parts[1].isdigit() and parts[2].isdigit()


# ── Identity record ───────────────────────────────────────────────────────────

def make_identity_record(
    cid: str,
    name: str,
    birth_year: Optional[int],
    birth_state: Optional[str],
    death_year: Optional[int],
    parent_cids: list,
    spouse_cids: list,
    child_cids: list,
    source_ids: list,
    evidence_grade: str,
    notes: str,
    dna_attestation_hash: Optional[str],   # hash of DNA attestation — never raw sequence
    biomarker_refs: list,                   # list of {"type": "...", "attestation_hash": "..."}
    privacy: str,                           # private | shared | public
    created_by: str,
    prev_hash: Optional[str] = None,
) -> dict:
    assert evidence_grade in EVIDENCE_GRADES, f"Invalid grade: {evidence_grade}"
    assert validate_cid(cid), f"Invalid CID: {cid}"
    assert privacy in ("private", "shared", "public")

    record = {
        "schema": SCHEMA,
        "record_id": str(uuid.uuid4()),
        "generated_at": now(),
        "cid": cid,
        "name": name,
        "birth_year": birth_year,
        "birth_state": birth_state,
        "death_year": death_year,
        "parent_cids": parent_cids,
        "spouse_cids": spouse_cids,
        "child_cids": child_cids,
        "source_ids": source_ids,
        "evidence_grade": evidence_grade,
        "evidence_grade_label": EVIDENCE_GRADES[evidence_grade],
        "notes": notes,
        "dna_attestation_hash": dna_attestation_hash,
        "biomarker_refs": biomarker_refs,
        "privacy": privacy,
        "created_by": created_by,
        "prev_hash": prev_hash,
        "superseded": False,
    }
    record["record_hash"] = sha256(json.dumps(
        {k: v for k, v in record.items() if k != "record_hash"},
        sort_keys=True
    ))
    return record


# ── Genealogy Hub ─────────────────────────────────────────────────────────────

class GenealogyHub:
    """
    Per-user genealogy hub.
    Storage: JSONL append-only ledger.
    Privacy gate: private records never exposed in public/shared views.
    Fork flow: creates a new hub instance with template structure.
    """

    def __init__(self, hub_root: str, owner_id: str, namespace: str):
        self.root      = Path(hub_root)
        self.owner_id  = owner_id
        self.namespace = namespace.upper()
        self.root.mkdir(parents=True, exist_ok=True)
        self.ledger_path   = self.root / "identities.jsonl"
        self.sources_path  = self.root / "sources.jsonl"
        self.receipts_path = self.root / "hub_receipts.jsonl"
        self.meta_path     = self.root / "hub_meta.json"
        self._init_meta()

    def _init_meta(self):
        if not self.meta_path.exists():
            meta = {
                "schema": "stegverse_genealogy_hub_meta.v1",
                "hub_id": str(uuid.uuid4()),
                "owner_id": self.owner_id,
                "namespace": self.namespace,
                "created_at": now(),
                "forked_from": None,
                "version": "1.0",
            }
            with open(self.meta_path, "w") as f:
                json.dump(meta, f, indent=2)

    def _append(self, path: Path, record: dict):
        with open(path, "a") as f:
            f.write(json.dumps(record) + "\n")

    def _load(self, path: Path) -> list:
        if not path.exists():
            return []
        records = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records

    def _latest_hash(self) -> Optional[str]:
        records = self._load(self.ledger_path)
        return records[-1]["record_hash"] if records else None

    def _emit_receipt(self, decision: str, reason: str, ref: str):
        receipt = {
            "schema": "stegverse_genealogy_hub_receipt.v1",
            "generated_at": now(),
            "engine": "genealogy-hub",
            "input_ref": ref,
            "actor_or_source": self.owner_id,
            "decision": decision,
            "reason": reason,
            "hashes": {"ref_hash": sha256(ref)},
            "unknowns": [],
            "next_route": "knowledge-vault",
        }
        self._append(self.receipts_path, receipt)
        return receipt

    # ── Write ─────────────────────────────────────────────────────────────

    def add_identity(
        self,
        cid: str,
        name: str,
        birth_year: int = None,
        birth_state: str = None,
        death_year: int = None,
        parent_cids: list = None,
        spouse_cids: list = None,
        child_cids: list = None,
        source_ids: list = None,
        evidence_grade: str = "D",
        notes: str = "",
        dna_attestation_hash: str = None,
        biomarker_refs: list = None,
        privacy: str = "private",
    ) -> dict:
        # Grade D alone cannot establish a parent-child link
        if evidence_grade == "D" and parent_cids:
            return {
                "decision": "FAIL_CLOSED",
                "reason": "Grade D evidence alone cannot establish parent-child lineage. Upgrade evidence first.",
                "cid": cid,
            }

        prev = self._latest_hash()
        record = make_identity_record(
            cid=cid, name=name, birth_year=birth_year, birth_state=birth_state,
            death_year=death_year, parent_cids=parent_cids or [],
            spouse_cids=spouse_cids or [], child_cids=child_cids or [],
            source_ids=source_ids or [], evidence_grade=evidence_grade,
            notes=notes, dna_attestation_hash=dna_attestation_hash,
            biomarker_refs=biomarker_refs or [], privacy=privacy,
            created_by=self.owner_id, prev_hash=prev,
        )
        self._append(self.ledger_path, record)
        receipt = self._emit_receipt("ALLOW", f"Identity {cid} ({name}) added.", cid)
        return {"record_id": record["record_id"], "cid": cid, "receipt": receipt}

    def add_source(self, source_id: str, title: str, source_type: str,
                   url: str = None, notes: str = "") -> dict:
        source = {
            "source_id": source_id, "title": title, "source_type": source_type,
            "url": url, "notes": notes, "added_at": now(),
            "source_hash": sha256(f"{source_id}:{title}"),
        }
        self._append(self.sources_path, source)
        return source

    def attach_dna_attestation(self, cid: str, dna_hash: str) -> dict:
        """
        Attach a DNA attestation hash to an existing identity.
        NEVER stores raw DNA — only the hash of the governed attestation.
        """
        record = self.get_identity(cid)
        if not record:
            return {"decision": "FAIL_CLOSED", "reason": f"CID {cid} not found."}

        upgraded = dict(record)
        upgraded["record_id"]             = str(uuid.uuid4())
        upgraded["generated_at"]          = now()
        upgraded["dna_attestation_hash"]  = dna_hash
        upgraded["prev_hash"]             = record["record_hash"]
        upgraded["evidence_grade"]        = max(record["evidence_grade"], "B")
        upgraded["record_hash"]           = sha256(json.dumps(
            {k: v for k, v in upgraded.items() if k != "record_hash"}, sort_keys=True
        ))
        self._append(self.ledger_path, upgraded)
        return self._emit_receipt("ALLOW", f"DNA attestation attached to {cid}.", cid)

    # ── Read ──────────────────────────────────────────────────────────────

    def get_identity(self, cid: str, requester_id: str = None) -> Optional[dict]:
        records = self._load(self.ledger_path)
        matches = [r for r in records if r.get("cid") == cid and not r.get("superseded")]
        if not matches:
            return None
        record = matches[-1]
        # Privacy gate
        if record.get("privacy") == "private" and requester_id != self.owner_id:
            return None
        return record

    def get_lineage(self, root_cid: str, requester_id: str = None) -> list:
        """Return full descendant lineage from root CID."""
        visited, queue, result = set(), [root_cid], []
        while queue:
            cid = queue.pop(0)
            if cid in visited:
                continue
            visited.add(cid)
            record = self.get_identity(cid, requester_id)
            if record:
                result.append(record)
                queue.extend(record.get("child_cids", []))
        return result

    def list_identities(self, requester_id: str = None, privacy_filter: str = None) -> list:
        records = self._load(self.ledger_path)
        seen_cids, result = set(), []
        for r in reversed(records):
            cid = r.get("cid")
            if cid in seen_cids or r.get("superseded"):
                continue
            seen_cids.add(cid)
            if r.get("privacy") == "private" and requester_id != self.owner_id:
                continue
            if privacy_filter and r.get("privacy") != privacy_filter:
                continue
            result.append(r)
        return list(reversed(result))

    def public_summary(self) -> dict:
        """Safe public-facing summary. Private records are excluded."""
        all_ids  = self.list_identities()
        public   = [r for r in all_ids if r.get("privacy") in ("public", "shared")]
        meta     = json.loads(self.meta_path.read_text())
        sources  = self._load(self.sources_path)
        return {
            "hub_id":      meta["hub_id"],
            "namespace":   self.namespace,
            "total_known": len(all_ids),
            "public_count": len(public),
            "identities":  public,
            "sources":     sources,
            "generated_at": now(),
        }

    # ── Fork ──────────────────────────────────────────────────────────────

    def generate_fork_manifest(self, new_owner_id: str, new_namespace: str) -> dict:
        """
        Generate a fork manifest for 'Create your own Genealogy Hub!'
        Returns everything a new user needs to bootstrap their own hub.
        Shared/public identities are included as starting evidence.
        Private identities are excluded.
        """
        meta = json.loads(self.meta_path.read_text())
        public_ids = self.list_identities(privacy_filter="shared") + \
                     self.list_identities(privacy_filter="public")

        manifest = {
            "schema": "stegverse_genealogy_hub_fork.v1",
            "fork_id": str(uuid.uuid4()),
            "generated_at": now(),
            "forked_from_hub_id": meta["hub_id"],
            "forked_from_namespace": self.namespace,
            "new_owner_id": new_owner_id,
            "new_namespace": new_namespace.upper(),
            "seed_identities": [
                {
                    "cid": r["cid"].replace(self.namespace, new_namespace.upper(), 1),
                    "name": r["name"],
                    "birth_year": r.get("birth_year"),
                    "birth_state": r.get("birth_state"),
                    "evidence_grade": r["evidence_grade"],
                    "notes": f"Forked from {self.namespace} hub. Original CID: {r['cid']}",
                    "privacy": "private",
                    "source_cid": r["cid"],
                }
                for r in public_ids
            ],
            "instructions": [
                "1. Create a new Knowledge Vault partition for your user_id.",
                "2. Run: python genealogy_hub.py init --owner <your_id> --namespace <YOUR_NS>",
                "3. Import seed identities from this manifest.",
                "4. Replace Grade D/C entries with primary evidence where possible.",
                "5. Add your own DNA attestation hash to link biological lineage.",
                "6. Set privacy='shared' on records you want to share with family.",
                "7. Invite others using the 'Create your own Genealogy Hub!' button.",
            ],
            "readme_url": "https://stegverse-labs.github.io/Site/genealogy-hub.html",
        }

        receipt = self._emit_receipt("ALLOW", f"Fork manifest generated for {new_namespace}.", "fork")
        manifest["receipt"] = receipt
        return manifest

    # ── Chain verification ────────────────────────────────────────────────

    def verify_chain(self) -> dict:
        records = self._load(self.ledger_path)
        errors  = []
        prev    = None
        for i, r in enumerate(records):
            stored = r.get("record_hash")
            r_copy = {k: v for k, v in r.items() if k != "record_hash"}
            computed = sha256(json.dumps(r_copy, sort_keys=True))
            if stored != computed:
                errors.append({"index": i, "cid": r.get("cid"), "error": "hash_mismatch"})
            if i > 0 and r.get("prev_hash") != prev:
                errors.append({"index": i, "cid": r.get("cid"), "error": "chain_break"})
            prev = stored
        return {"records": len(records), "errors": errors, "valid": len(errors) == 0}


# ── CLI / seed data ───────────────────────────────────────────────────────────

def seed_randolph_hub(hub_root: str = "./hub_demo", owner_id: str = "user_001"):
    """Seed the Randolph Genealogy Hub with the documented lineage."""
    hub = GenealogyHub(hub_root, owner_id, "RND")

    hub.add_source("SRC-001", "Tennessee County Records", "transcribed_primary")
    hub.add_source("SRC-002", "Missouri Census 1860", "transcribed_primary")
    hub.add_source("SRC-003", "Civil War Military Records", "primary")
    hub.add_source("SRC-004", "Oregon Death Certificate", "primary")

    lineage = [
        ("RND-c1760-001-VA", "Peyton Randolph Sr", None, "VA", None, [], "B", "Virginia origin — pending primary upgrade"),
        ("RND-1796-001-TN",  "Ruben Randolph",      1796, "TN", None, ["RND-c1760-001-VA"], "B", "SRC-001"),
        ("RND-1827-001-TN",  "Isaac Randolph",      1827, "TN", None, ["RND-1796-001-TN"],  "B", "SRC-001"),
        ("RND-1853-001-MO",  "Elijah Randolph",     1853, "MO", None, ["RND-1827-001-TN"],  "B", "SRC-002"),
        ("RND-1875-001-IN",  "Benjamin Franklin Randolph", 1875, "IN", None, ["RND-1853-001-MO"], "B", "SRC-003"),
        ("RND-1909-001-OR",  "Col. Jack Lindley Randolph", 1909, "OR", None, ["RND-1875-001-IN"], "A", "SRC-004"),
    ]

    prev_cid = None
    for cid, name, by, bs, dy, parents, grade, notes in lineage:
        r = hub.add_identity(
            cid=cid, name=name, birth_year=by, birth_state=bs,
            death_year=dy, parent_cids=parents,
            evidence_grade=grade, notes=notes, privacy="shared",
        )
        if prev_cid:
            # Update previous record's child_cids
            pass
        prev_cid = cid

    chain = hub.verify_chain()
    print(f"Randolph Hub seeded. Chain valid: {chain['valid']} ({chain['records']} records)")
    return hub


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "demo"

    if cmd == "demo":
        hub = seed_randolph_hub()
        summary = hub.public_summary()
        print(f"Public identities: {summary['public_count']}")
        fork = hub.generate_fork_manifest("new_user_002", "NEW")
        print(f"Fork manifest: {len(fork['seed_identities'])} seed identities")
        fork_path = Path("./hub_demo/fork_manifest.json")
        with open(fork_path, "w") as f:
            json.dump(fork, f, indent=2)
        print(f"Fork manifest saved to {fork_path}")

    elif cmd == "init":
        owner   = sys.argv[sys.argv.index("--owner") + 1]   if "--owner"     in sys.argv else "user_001"
        ns      = sys.argv[sys.argv.index("--namespace") + 1] if "--namespace" in sys.argv else "FAM"
        hub_dir = sys.argv[sys.argv.index("--dir") + 1]      if "--dir"       in sys.argv else f"./hub_{ns.lower()}"
        hub = GenealogyHub(hub_dir, owner, ns)
        print(f"Hub initialized: {hub_dir}")

    elif cmd == "verify":
        hub_dir = sys.argv[2]
        owner   = sys.argv[3] if len(sys.argv) > 3 else "user_001"
        ns      = sys.argv[4] if len(sys.argv) > 4 else "FAM"
        hub = GenealogyHub(hub_dir, owner, ns)
        result = hub.verify_chain()
        print(json.dumps(result, indent=2))
