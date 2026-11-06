set -euo pipefail
cp data/va-claim-assistant/chat-surface-validation.json /tmp/chat-surface-validation.before.json
git hash-object data/va-claim-assistant/chat-surface-validation.json > /tmp/chat-surface-validation.before.sha
