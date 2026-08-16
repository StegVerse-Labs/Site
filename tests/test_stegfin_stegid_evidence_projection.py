from hashlib import sha1
from pathlib import Path

ASSET = Path(__file__).parents[1] / "assets" / "stegfin-phone" / "device-wallet-identity.js"
EXPECTED_UPSTREAM_BLOB = "efc2c9c21d369bbc3d6817599f74496f918d721b"


def git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def test_exact_released_stegfin_blob_is_projected():
    data = ASSET.read_bytes()
    assert git_blob_sha(data) == EXPECTED_UPSTREAM_BLOB


def test_sanitized_admission_evidence_is_directly_projected():
    text = ASSET.read_text(encoding="utf-8")
    for marker in (
        "stegverse-stegid-device-wallet-v1",
        "latest-admission",
        "stegverse.stegid.sanitized_admission_evidence.v1",
        "IDENTITY_CONTINUITY_VALID",
        "DEVICE_ADMITTED",
        "DEVICE_POSSESSION",
        "HUMAN_CONTINUITY",
        "IDENTITY_CONTINUITY",
        "granted_capabilities",
        "PREPARE",
        "stegid_admission_evidence",
        "evidence_sha256",
    ):
        assert marker in text


def test_authority_and_secret_boundaries_remain_fail_closed():
    text = ASSET.read_text(encoding="utf-8")
    for marker in (
        "TV/TVC",
        "credential_requirement !== 'NONE'",
        "non_tv_tvc_secret_or_token_used !== false",
        "wallet_secret_exported !== false",
        "private_key_present !== false",
        "seed_present !== false",
        "granted_capabilities.includes('SIGN')",
        "granted_capabilities.includes('BROADCAST')",
        "protected credential field prohibited",
    ):
        assert marker in text
