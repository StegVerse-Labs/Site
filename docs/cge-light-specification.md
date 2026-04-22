# CGE Light Specification

## Purpose

Lightweight Code Generation and Evaluation for temporary repos.
Evaluates execution correctness without full CGE overhead.
Generates merkle proofs instead of detailed reports.

## Core Functions

| Function | Input | Output | Token Needed |
|----------|-------|--------|--------------|
| `hash_operations(operations[])` | List of operations | SHA-256 hash | No |
| `build_merkle_tree(leaves[])` | Operation hashes | Merkle root | No |
| `verify_merkle_path(root, leaf, path)` | Root, leaf, proof path | Boolean | No |
| `evaluate_constraints(code, constraints[])` | Code + rules | Pass/fail + score | No |
| `sign_proof(private_key, proof)` | Key + merkle proof | Signature | Yes (TVC) |

## Merkle Tree Structure

Level 0 (leaves): hash(op1), hash(op2), hash(op3), hash(op4)
Level 1:          hash(hash(op1)+hash(op2)), hash(hash(op3)+hash(op4))
Level 2 (root):   hash(level1_left + level1_right)

## Proof Format

{
  "merkle_root": "sha256:abc123...",
  "leaf_count": 47,
  "operations_hash": "sha256:def456...",
  "evaluation_score": 0.94,
  "timestamp": "2026-04-22T01:02:00Z",
  "temp_repo": "StegGhost/temp-uuid",
  "signature": "tvc_signed..."
}

## CGE Light vs Full CGE

| Feature | CGE Light | Full CGE |
|---------|-----------|----------|
| Location | Temp repos | StegGhost/StegCGE |
| Scope | Single execution batch | Cross-repo analysis |
| Output | Merkle proof | Detailed report |
| Speed | < 1 second | 5-30 seconds |
| Token use | None (local) | Yes (cross-org) |
| Storage | Minimal | Full logs |

## Implementation

```python
# cge-light.py
import hashlib
import json
from typing import List, Dict

def hash_operation(op: Dict) -> str:
    """Hash a single operation."""
    return hashlib.sha256(json.dumps(op, sort_keys=True).encode()).hexdigest()

def build_merkle_tree(leaves: List[str]) -> str:
    """Build merkle tree from leaf hashes, return root."""
    if len(leaves) == 0:
        return hashlib.sha256(b'empty').hexdigest()
    if len(leaves) == 1:
        return leaves[0]
    
    # Pad to power of 2
    while len(leaves) & (len(leaves) - 1) != 0:
        leaves.append(leaves[-1])
    
    # Build tree bottom-up
    level = leaves
    while len(level) > 1:
        next_level = []
        for i in range(0, len(level), 2):
            combined = level[i] + level[i+1]
            next_level.append(hashlib.sha256(combined.encode()).hexdigest())
        level = next_level
    
    return level[0]

def generate_proof(leaves: List[str], leaf_index: int) -> List[str]:
    """Generate merkle proof path for a leaf."""
    proof = []
    level = leaves
    index = leaf_index
    
    while len(level) > 1:
        sibling = index ^ 1
        if sibling < len(level):
            proof.append(level[sibling])
        
        next_level = []
        for i in range(0, len(level), 2):
            if i+1 < len(level):
                combined = level[i] + level[i+1]
            else:
                combined = level[i] + level[i]
            next_level.append(hashlib.sha256(combined.encode()).hexdigest())
        
        level = next_level
        index = index // 2
    
    return proof

def verify_proof(root: str, leaf: str, proof: List[str], leaf_index: int) -> bool:
    """Verify a merkle proof."""
    current = leaf
    index = leaf_index
    
    for sibling in proof:
        if index % 2 == 0:
            combined = current + sibling
        else:
            combined = sibling + current
        current = hashlib.sha256(combined.encode()).hexdigest()
        index = index // 2
    
    return current == root
