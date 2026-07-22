#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "ecosystem-music.html"
SCOPE = ROOT / "assets" / "ecosystem-music-profile-scope.js"


def fail(message: str) -> int:
    print(f"STEGMUSIC_PROFILE_ISOLATION_ACCESSIBILITY_FAIL: {message}")
    return 1


def main() -> int:
    for path in (PAGE, SCOPE):
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    page = PAGE.read_text(encoding="utf-8")
    scope = SCOPE.read_text(encoding="utf-8")

    page_markers = (
        'id="isolatedProfileId"',
        'id="switchIsolatedProfile"',
        'id="activeProfileScope"',
        'assets/ecosystem-music-profile-scope.js',
        'aria-label="Primary"',
        'aria-current="page"',
        'role="tablist"',
        'role="tabpanel"',
        'aria-live="polite"',
        'aria-label="Generated audio controls"',
        'aria-label="User-owned local audio player"',
        'id="main-content"',
    )
    scope_markers = (
        'stegmusic.active-profile.v1',
        'stegmusic.profile-registry.v1',
        'stegmusic.profile.${activeProfileId}.${key}',
        'cross_profile_read: false',
        "storage_isolation: 'browser_local_namespace'",
        'window.location.reload()',
        'Storage.prototype.getItem',
        'Storage.prototype.setItem',
        'Storage.prototype.removeItem',
    )

    for marker in page_markers:
        if marker not in page:
            return fail(f"page missing marker: {marker}")
    for marker in scope_markers:
        if marker not in scope:
            return fail(f"profile scope missing marker: {marker}")

    if page.index('assets/ecosystem-music-profile-scope.js') > page.index('assets/ecosystem-music.js'):
        return fail("profile scope must load before music runtimes")

    ids = re.findall(r'\bid="([^"]+)"', page)
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        return fail(f"duplicate ids: {', '.join(duplicates)}")

    for input_id in ('musicSearch', 'localAudioFile', 'progress', 'volume', 'sessionIntent', 'feedbackText', 'isolatedProfileId', 'profileName'):
        if f'for="{input_id}"' not in page and f'aria-label="' not in page.split(f'id="{input_id}"', 1)[-1][:180]:
            return fail(f"control lacks visible or aria label: {input_id}")

    print("STEGMUSIC_PROFILE_ISOLATION_ACCESSIBILITY_PASS")
    print("profile_storage=browser_local_namespaced")
    print("cross_profile_read=false")
    print("accessibility_contract=present")
    print("invited_tester_server_isolation=not_claimed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
