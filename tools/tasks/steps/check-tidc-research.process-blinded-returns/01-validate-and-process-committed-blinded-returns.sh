set -euo pipefail
shopt -s nullglob
returns=(data/tidc/blinded-coding/returns/*.json)
mkdir -p generated/tidc-blinded-results
if [ ${#returns[@]} -eq 0 ]; then
  echo 'No blinded return committed; external evidence remains pending.'
  exit 0
fi
for return_file in "${returns[@]}"; do
  base="$(basename "$return_file" .json)"
  python scripts/validate_tidc_blinded_return.py "$return_file"
  python scripts/create_tidc_blinded_return_receipt.py \
    "$return_file" \
    --out "generated/tidc-blinded-results/${base}.receipt.json"
  python scripts/compare_tidc_blinded_coding.py \
    "$return_file" \
    --json-out "generated/tidc-blinded-results/${base}.comparison.json" \
    --md-out "generated/tidc-blinded-results/${base}.comparison.md"
done
