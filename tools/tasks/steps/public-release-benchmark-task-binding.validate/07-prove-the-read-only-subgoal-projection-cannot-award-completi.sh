set -euo pipefail
python -m pytest tests/test_economic_roadmap_subgoals.py -v
python scripts/project_economic_roadmap_subgoals.py > /dev/null
