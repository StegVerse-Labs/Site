set -euo pipefail
GITHUB_SHA="$SOURCE_SHA" GITHUB_WORKFLOW='Capture Validation Evidence' python3 scripts/capture_validation_manifest.py
