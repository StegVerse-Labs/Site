set -euo pipefail
grep -F 'PILOT · NOT CONFIRMATORY' technology-induced-discovery-clustering.html
grep -F 'Site is the public mirror, not proof authority' technology-induced-discovery-clustering.html
grep -F 'DESCRIPTIVE_NOT_VALIDATION' scripts/compare_tidc_blinded_coding.py
grep -F 'Disagreements must be retained' scripts/compare_tidc_blinded_coding.py
grep -F 'human_replication: not established' scripts/compare_tidc_blinded_coding.py
grep -F 'receipt != reliability' docs/TIDC_BLINDED_CODING_ADJUDICATION_PROTOCOL.md
