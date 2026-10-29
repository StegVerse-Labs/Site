"""The live StegOS Node observation follows the deployed bootstrap graph.

Pages serves this repository's root at the CNAME origin, so the deployed
projection at https://stegverse.org/stegos-node/ is byte-for-byte the source
tree. Serving the tree through the observer's fetch seam reproduces the
deployed observation without any network access.
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://stegverse.org"
LIVE_URL = f"{ORIGIN}/stegos-node/"

_spec = importlib.util.spec_from_file_location(
    "check_stegos_node_projection_impl",
    ROOT / "scripts" / "check_stegos_node_projection_impl.py",
)
observer = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(observer)


def deployed_fetch(url: str) -> str:
    """Return the deployed bytes for url: the source file at the same path."""
    parsed = urlparse(url)
    if f"{parsed.scheme}://{parsed.netloc}" != ORIGIN:
        raise ValueError(f"unexpected origin {url}")
    path = parsed.path.lstrip("/")
    if path.endswith("/") or not path:
        path += "index.html"
    target = ROOT / path
    if not target.is_file():
        raise ValueError(f"live observation returned HTTP 404 for {url}")
    return target.read_text(encoding="utf-8")


def claims() -> tuple[str, str]:
    return observer.BASE_CLAIM.read_text(encoding="utf-8"), observer.OFFLINE_CLAIM.read_text(encoding="utf-8")


class LiveObservationTests(unittest.TestCase):
    def test_deployed_projection_verifies_through_bootstrap_graph(self) -> None:
        base_claim, offline_claim = claims()
        failures = observer.validate_live_projection(
            LIVE_URL, base_claim, offline_claim, require_offline_proof=True, fetch=deployed_fetch
        )
        self.assertEqual(failures, [])

    def test_bootstrap_alone_does_not_satisfy_implementation_markers(self) -> None:
        # If the observer stops following document.written scripts, the
        # implementation markers are absent and the observation fails closed.
        base_claim, offline_claim = claims()

        def bootstrap_only(url: str) -> str:
            if "stegos-node-impl.js" in url:
                return ""
            return deployed_fetch(url)

        failures = observer.validate_live_projection(
            LIVE_URL, base_claim, offline_claim, require_offline_proof=True, fetch=bootstrap_only
        )
        self.assertIn("projection missing stegos.node_handoff_receipt.v1", failures)

    def test_unreachable_written_script_fails_closed(self) -> None:
        base_claim, offline_claim = claims()

        def missing_impl(url: str) -> str:
            if "stegos-node-impl.js" in url:
                raise ValueError(f"live observation returned HTTP 404 for {url}")
            return deployed_fetch(url)

        failures = observer.validate_live_projection(
            LIVE_URL, base_claim, offline_claim, require_offline_proof=True, fetch=missing_impl
        )
        self.assertEqual(len(failures), 1)
        self.assertTrue(failures[0].startswith("live observation failed:"))

    def test_written_scripts_resolve_against_the_origin(self) -> None:
        bootstrap = (ROOT / "stegos-node" / "stegos-node.js").read_text(encoding="utf-8")
        written = observer.document_written_script_urls(bootstrap)
        self.assertTrue(any("stegos-node-impl.js" in url for url in written))
        for url in written:
            deployed_fetch(observer.urljoin(LIVE_URL, url))


if __name__ == "__main__":
    unittest.main()
