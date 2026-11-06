set -euo pipefail
test -s /tmp/chat-surface-validation.before.json
test -s /tmp/chat-surface-validation.before.sha
cp /tmp/chat-surface-validation.before.json data/va-claim-assistant/chat-surface-validation.json
test "$(git hash-object data/va-claim-assistant/chat-surface-validation.json)" = "$(cat /tmp/chat-surface-validation.before.sha)"
test -z "$(git status --porcelain -- data/va-claim-assistant/chat-surface-validation.json)"
echo 'VA_CLAIMS_CHAT_REPOSITORY_WRITEBACK=NONE'
echo 'VA_CLAIMS_CHAT_ARTIFACT_CUSTODY=NONE'
