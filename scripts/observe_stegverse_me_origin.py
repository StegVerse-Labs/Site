#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import ssl
from pathlib import Path
from urllib import error, request
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/stegverse-me-origin-observation-contract.json"
OPAQUE_SAMPLE = "sv1_" + "A" * 43


class ObservationError(RuntimeError):
    pass


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ObservationError("redirect_rejected")


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def validate_target(base_url: str, contract: dict) -> str:
    parsed = urlsplit(base_url)
    if parsed.scheme != "https" or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ObservationError("https_origin_required")
    if parsed.hostname not in contract["allowed_https_hosts"]:
        raise ObservationError("origin_host_not_admitted")
    if parsed.path not in ("", "/"):
        raise ObservationError("origin_base_path_must_be_root")
    port = f":{parsed.port}" if parsed.port and parsed.port != 443 else ""
    return f"https://{parsed.hostname}{port}"


def validate_headers(headers, contract: dict) -> None:
    lowered = {str(k).lower(): str(v) for k, v in headers.items()}
    for key, expected in contract["required_response_headers"].items():
        if lowered.get(key) != expected:
            raise ObservationError(f"required_header_mismatch:{key}")


def validate_route_result(status: int, headers, contract: dict) -> None:
    if status != 200:
        raise ObservationError(f"canonical_route_status_invalid:{status}")
    validate_headers(headers, contract)


def observe(base_url: str) -> dict:
    contract = load_contract()
    origin = validate_target(base_url, contract)
    context = ssl.create_default_context()
    opener = request.build_opener(NoRedirect, request.HTTPSHandler(context=context))

    paths = [
        "/",
        f"/n/{OPAQUE_SAMPLE}/",
        f"/n/{OPAQUE_SAMPLE}/services.html",
    ]
    observations = []
    for path in paths:
        req = request.Request(
            origin + path,
            method="GET",
            headers={"User-Agent": "StegVerse-Personal-Origin-Observer/1"},
        )
        try:
            with opener.open(req, timeout=15) as response:
                status = int(response.status)
                headers = dict(response.headers.items())
                response.read(1024)
        except ObservationError:
            raise
        except error.HTTPError as exc:
            raise ObservationError(f"canonical_route_http_error:{exc.code}") from exc
        except Exception as exc:
            raise ObservationError(f"canonical_route_transport_error:{type(exc).__name__}") from exc
        validate_route_result(status, headers, contract)
        observations.append({"path": path, "status": status})

    isolation_req = request.Request(
        origin + "/api/stegverse-node",
        method="GET",
        headers={"User-Agent": "StegVerse-Personal-Origin-Observer/1"},
    )
    try:
        with opener.open(isolation_req, timeout=15) as response:
            isolation_status = int(response.status)
    except error.HTTPError as exc:
        isolation_status = int(exc.code)
    except ObservationError:
        raise
    except Exception as exc:
        raise ObservationError(f"isolation_transport_error:{type(exc).__name__}") from exc
    if isolation_status != 404:
        raise ObservationError(f"shared_gateway_api_not_isolated:{isolation_status}")

    return {
        "schema": "stegverse.site.personal-origin-observation/v1",
        "state": "VERIFIED",
        "origin": origin,
        "tls_webpki_verified_by_client": True,
        "redirects_followed": False,
        "authorization_header_sent": False,
        "cookie_sent": False,
        "canonical_routes": observations,
        "shared_gateway_api_isolated": True,
        "private_kv_readback_performed": False,
        "authenticated_interlock_admission_performed": False,
        "dns_mutation_performed": False,
        "dns_target_emitted": False,
        "credential_authority": "TV/TVC",
        "authority_effect": "NONE",
        "activation_effect": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--origin", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = observe(args.origin)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
