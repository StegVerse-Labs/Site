from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "assets" / "stegfin-phone" / "app.js"


def text() -> str:
    return APP.read_text(encoding="utf-8")


def test_wallet_review_is_fail_closed_and_user_only() -> None:
    source = text()
    for marker in (
        "function validateReviewableHandoff(local)",
        "receipt.state !== WALLET_READY",
        "receipt.credential_authority !== 'TV/TVC'",
        "receipt.credential_requirement !== 'NONE'",
        "receipt.non_tv_tvc_secret_or_token_used !== false",
        "receipt.hosted_runtime_required !== false",
        "handoff.chain_id !== '0x2105'",
        "candidate.chain_id !== '0x2105'",
        "candidate.requires_user_wallet_signature !== true",
        "handoff.wallet_is_only_signing_authority !== true",
        "handoff.explicit_wallet_confirmation_required !== true",
        "handoff.automatic_signing !== false",
        "handoff.automatic_broadcast !== false",
        "route.decision !== 'ROUTE_ADMITTED'",
        "route.authority !== 'TV/TVC'",
        "route.credential_requirement !== 'NONE'",
        "button.disabled = !reviewable",
    ):
        assert marker in source


def test_wallet_review_surfaces_exact_bounded_candidate() -> None:
    source = text()
    for marker in (
        "candidate.purpose === 'exact_erc20_approval'",
        "candidate.exact_allowance_atomic",
        "candidate.unlimited_allowance === false",
        "Spender / SwapRouter02",
        "Quote minimum out",
        "Fee tier",
        "Slippage ceiling",
        "Gas estimate",
        "Gas reserve sufficient",
        "StegID capability",
        "Yes · USER_ONLY",
        "Signed",
        "Broadcast",
    ):
        assert marker in source


def test_wallet_review_cannot_contact_or_operate_wallet() -> None:
    source = text()
    for forbidden in (
        "eth_sendRawTransaction",
        "eth_sendTransaction",
        "personal_sign",
        "eth_sign",
        "wallet_requestPermissions",
        "wallet_addEthereumChain",
        "window.ethereum.request",
        "Authorization",
        "Bearer ",
        "GITHUB_TOKEN",
        "RENDER_API_KEY",
    ):
        assert forbidden not in source
    assert "Review only: this control never contacts a wallet, signs, broadcasts, or settles." in source
    assert "No wallet action occurred." in source
