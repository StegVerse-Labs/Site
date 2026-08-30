from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_stegverse_me_origin_bundle import INLINE_MARKER, SCHEMA, build_bundle
from scripts.observe_stegverse_me_origin import ObservationError, load_contract, validate_headers, validate_route_result, validate_target


class HeaderMap(dict):
    def items(self):
        return super().items()


class PersonalOriginBundleTests(unittest.TestCase):
    def test_bundle_is_deterministic_public_only_and_manifested(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            first = build_bundle(root)
            before = (root / "stegverse-me-origin-manifest.json").read_bytes()
            second = build_bundle(root)
            after = (root / "stegverse-me-origin-manifest.json").read_bytes()
            self.assertEqual(first, second)
            self.assertEqual(before, after)
            self.assertEqual(first["schema"], SCHEMA)
            self.assertFalse(first["private_kv_included"])
            self.assertFalse(first["credential_material_included"])
            self.assertFalse(first["dns_target_included"])
            self.assertEqual(first["authority_effect"], "NONE")
            self.assertFalse(first["activation_effect"])
            self.assertEqual(len(first["files"]), 7)
            for name, digest in first["files"].items():
                self.assertTrue((root / name).is_file(), name)
                self.assertRegex(digest, r"^sha256:[a-f0-9]{64}$")

    def test_root_inlines_canonical_resolver_without_private_values(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            build_bundle(root)
            text = (root / "index.html").read_text(encoding="utf-8")
            self.assertNotIn(INLINE_MARKER, text)
            self.assertIn("StegVerseOpaqueNodeResolver.deriveOpaqueNode", text)
            self.assertIn("stegos-web-bootstrap-v1", text)
            self.assertIn("Private KV has not been read", text)
            self.assertNotIn("node-private-raw-id", text)
            self.assertNotIn("device-private-raw-id", text)

    def test_origin_services_navigation_stays_on_personal_origin(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            build_bundle(root)
            text = (root / "services.html").read_text(encoding="utf-8")
            self.assertIn('<a href="/">My KV</a>', text)
            self.assertIn('src="./services-state.js"', text)
            self.assertIn('src="./services.js"', text)

    def test_observation_contract_requires_https_and_admitted_host(self) -> None:
        contract = load_contract()
        self.assertEqual(validate_target("https://stegverse.me", contract), "https://stegverse.me")
        with self.assertRaises(ObservationError):
            validate_target("http://stegverse.me", contract)
        with self.assertRaises(ObservationError):
            validate_target("https://example.com", contract)
        with self.assertRaises(ObservationError):
            validate_target("https://stegverse.me/path", contract)

    def test_observation_headers_are_non_authorizing(self) -> None:
        contract = load_contract()
        headers = HeaderMap({
            "X-StegVerse-Credential-Authority": "TV/TVC",
            "X-StegVerse-Authority-Effect": "NONE",
            "X-StegVerse-Activation-Effect": "false",
            "X-StegVerse-Route-Possession-Grants-Access": "false",
            "X-StegVerse-Private-KV-Readback": "false",
        })
        validate_headers(headers, contract)
        validate_route_result(200, headers, contract)
        bad = HeaderMap(headers)
        bad["X-StegVerse-Private-KV-Readback"] = "true"
        with self.assertRaises(ObservationError):
            validate_headers(bad, contract)

    def test_observation_contract_cannot_emit_dns_from_source(self) -> None:
        contract = load_contract()
        self.assertFalse(contract["source_state_can_verify_origin"])
        self.assertFalse(contract["ci_state_can_verify_origin"])
        self.assertFalse(contract["dns_target_output_allowed_before_verified_origin"])
        self.assertEqual(contract["authority_effect"], "NONE")
        self.assertFalse(contract["activation_effect"])


if __name__ == "__main__":
    unittest.main()
