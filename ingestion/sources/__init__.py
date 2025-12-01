from typing import Dict, Any

from .cfp_collegefootballplayoff import fetch_cfp_data_from_cfp_site


def fetch_from_source(source_type: str, source_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dispatch to the correct fetcher based on 'type' in config.
    Each fetcher returns a standard dict with keys:
      - last_updated (ISO string)
      - sources (list)
      - cfp_source_id (optional)
      - conf_source_id (optional)
      - rankings (list)
      - games (list)
      - polls (list)
      - conferences (list)
    """
    if source_type == "cfp_collegefootballplayoff":
        return fetch_cfp_data_from_cfp_site(source_config)

    raise ValueError(f"Unknown source type: {source_type}")
