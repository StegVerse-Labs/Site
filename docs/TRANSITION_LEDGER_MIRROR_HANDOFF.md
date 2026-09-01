# Transition Ledger Mirror Handoff

Repository: `StegVerse-Labs/Site`

Every durable transition owned here is recorded first in this repository ledger. Repo replay/reconstruction must terminate without org/ecosystem replay.

Contract: `.stegverse/transition-ledger/contract.json`  
Emitter: `.stegverse/transition-ledger/emit.py`  
Durable root: `$XDG_STATE_HOME/stegverse/repo-ledgers/StegVerse-Labs/Site`

Receipts are append-only/hash-linked. Only evidence needed for organization reconstruction propagates to `StegVerse-Labs/.github`. Recording grants no authority.
