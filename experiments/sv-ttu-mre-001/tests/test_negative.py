#!/usr/bin/env python3
import copy, importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("verify",ROOT/"verifier"/"verify.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
base=json.loads((ROOT/"cases"/"case_001_valid_allow.json").read_text())
def check(case,decision,code):
    got,reasons=mod.evaluate(case); assert got==decision,(got,reasons); assert code in reasons,(got,reasons)
x=copy.deepcopy(base); del x["actor"]; check(x,"FAIL_CLOSED","REQUIRED_FIELD_MISSING:actor")
x=copy.deepcopy(base); x["request"]["commit_time"]="bad"; check(x,"FAIL_CLOSED","COMMIT_TIME_UNRESOLVED")
x=copy.deepcopy(base); x["request"]["scope"]="bad"; check(x,"DENY","DELEGATION_SCOPE_MISMATCH")
x=copy.deepcopy(base); x["evidence"]["integrity"]="unknown"; check(x,"FAIL_CLOSED","EVIDENCE_FRESHNESS_UNRESOLVED")
print("negative tests: PASS")
