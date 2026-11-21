set -euo pipefail
node --check assets/workspace-ecosystem-review.js
node --check assets/workspace-ecosystem-review-ui.js
node --test tests/workspace-ecosystem-review.test.cjs
