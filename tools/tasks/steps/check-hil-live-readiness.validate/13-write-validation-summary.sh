echo '## HIL validation and live-readiness observation' >> "$GITHUB_STEP_SUMMARY"
echo '' >> "$GITHUB_STEP_SUMMARY"
echo 'Credential authority remains TV/TVC. This workflow consumes no project/provider secret or token and grants no activation, publication, execution, release, Master Record, review, custody, reconstruction, or wallet authority.' >> "$GITHUB_STEP_SUMMARY"
echo 'Activation-state, public-response import, artifact-verification import, HTTPS probe import/regression, Site-side Master Record release projection, Master Records return-receipt and transfer-packet, and Federal-Plus security validators are consolidated here without separate token-backed workflow entry surfaces. LinkedIn launch readiness remains isolated because its current deterministic check exposes unresolved public-page marker drift.' >> "$GITHUB_STEP_SUMMARY"
if [ -f reports/hil-federal-plus-security-validation.json ]; then
  echo '' >> "$GITHUB_STEP_SUMMARY"
  echo '### HIL Federal-Plus Security Validation' >> "$GITHUB_STEP_SUMMARY"
  echo '```json' >> "$GITHUB_STEP_SUMMARY"
  cat reports/hil-federal-plus-security-validation.json >> "$GITHUB_STEP_SUMMARY"
  echo '```' >> "$GITHUB_STEP_SUMMARY"
fi
echo '' >> "$GITHUB_STEP_SUMMARY"
if [ -f reports/hil-live-readiness.latest.json ]; then
  echo '```json' >> "$GITHUB_STEP_SUMMARY"
  cat reports/hil-live-readiness.latest.json >> "$GITHUB_STEP_SUMMARY"
  echo '```' >> "$GITHUB_STEP_SUMMARY"
else
  echo 'Live observation is intentionally omitted for pull requests, or observation JSON was not produced.' >> "$GITHUB_STEP_SUMMARY"
fi
