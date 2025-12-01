# CFP Data Ingestion – Source Notes

This folder contains the **live CFP data file** used by the site:

- `cfp-data.json` – updated automatically by `.github/workflows/cfp_ingest.yml`

## How updates work

1. GitHub Actions runs `tools/cfp_ingest.py`
2. The script fetches JSON from the URL in the `CFP_SOURCE_URL` secret
3. The script normalizes `last_updated` and writes `data/cfp-data.json`
4. If there are changes, the workflow commits and pushes them back to the repo

## CFP_SOURCE_URL

Set this as a GitHub Actions secret on the `site` repo:

- Name: `CFP_SOURCE_URL`
- Value: a URL returning JSON like:

```jsonc
{
  "last_updated": "2025-11-29T21:00:00Z",
  "sources": [
    { "id": "1", "label": "College Football Playoff", "url": "https://collegefootballplayoff.com" }
  ],
  "cfp_source_id": "1",
  "conf_source_id": "4",
  "rankings": [],
  "games": [],
  "polls": [],
  "conferences": []
}
