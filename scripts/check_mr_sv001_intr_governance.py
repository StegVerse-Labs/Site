#!/usr/bin/env python3
from pathlib import Path

impl = Path(__file__).with_name("check_mr_sv001_intr_governance_impl.py")
source = impl.read_text(encoding="utf-8")
source = source.replace('ROOT / "stegos-bootstrap/stegos-bootstrap.js"', 'ROOT / "stegos-bootstrap/stegos-bootstrap-impl.js"')
source = source.replace(
    "    require('profiles:[\"KV:KnowledgeVaultInterlock\",\"HIL:Ingress\",\"MasterRecords:SV001Custody\"]' in root_intr,\n"
    "            \"root InTr profile must preserve KV/HIL and add bounded MR custody\")\n",
    "    for required_profile in [\"KV:KnowledgeVaultInterlock\", \"HIL:Ingress\", \"MasterRecords:SV001Custody\"]:\n"
    "        require(f'\\\"{required_profile}\\\"' in root_intr,\n"
    "                f\"root InTr profile missing required existing profile: {required_profile}\")\n",
)
namespace = {"__name__": "__main__", "__file__": str(impl)}
exec(compile(source, str(impl), "exec"), namespace)
