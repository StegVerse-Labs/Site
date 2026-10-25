set +e
python scripts/check_coherent_transition_threshold_activation.py > coherent-transition-threshold-activation.log 2>&1
code=$?
cat coherent-transition-threshold-activation.log
if [ "$code" -eq 0 ]; then
  echo "activation_gate=PASS" >> "$GITHUB_STEP_SUMMARY"
else
  echo "activation_gate=BLOCKED" >> "$GITHUB_STEP_SUMMARY"
fi
exit 0
