#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "ecosystem-music.html"
RUNTIME = ROOT / "assets" / "ecosystem-music-diagnostics.js"
MEDIA_TRANSPORT = ROOT / "assets" / "ecosystem-music-media-transport.js"
IPHONE_VERIFICATION = ROOT / "assets" / "ecosystem-music-iphone-verification.js"
ENHANCEMENT = ROOT / "assets" / "ecosystem-music-enhancement.js"


def fail(message: str) -> int:
    print(f"STEGMUSIC_BROWSER_SELF_TEST_FAIL: {message}")
    return 1


def main() -> int:
    for path in (PAGE, RUNTIME, MEDIA_TRANSPORT, IPHONE_VERIFICATION, ENHANCEMENT):
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    page = PAGE.read_text(encoding="utf-8")
    runtime = RUNTIME.read_text(encoding="utf-8")
    transport = MEDIA_TRANSPORT.read_text(encoding="utf-8")
    guided = IPHONE_VERIFICATION.read_text(encoding="utf-8")
    enhancement = ENHANCEMENT.read_text(encoding="utf-8")

    page_markers = (
        'id="audioSelfTest"',
        'id="audioSelfTestResult"',
        'Run audio self-test',
        'assets/ecosystem-music-diagnostics.js',
        'confirms browser execution, not audibility',
    )
    runtime_markers = (
        "StegMusicDiagnostics",
        "audio_self_test_passed",
        "audio_self_test_failed",
        "composition_progress_advanced",
        "playback_event_observed",
        "audible_output_confirmed: false",
        "browser_runtime_execution_confirmed: true",
        "generated_media_transport_confirmed",
        "guided_verification_runtime_confirmed",
        "loudness_harmony_enhancement_confirmed",
        "assets/ecosystem-music-media-transport.js",
        "assets/ecosystem-music-iphone-verification.js",
        "assets/ecosystem-music-enhancement.js",
        "window.dispatchEvent(new CustomEvent('stegmusic:emit'",
    )
    transport_markers = (
        "OfflineAudioContext",
        "encodeWav",
        "generatedMediaPlayer",
        "html_audio_blob_wav",
        "navigator.mediaSession",
        "visibilitychange",
        "pagehide",
        "pageshow",
        "iphonePlaybackVerification",
        "I hear audio",
        "iphone_playback_${kind}_confirmed",
        "human_audibility_confirmed: kind === 'audible'",
        "source_bytes_uploaded: false",
        "window.StegMusicMediaTransport",
    )
    guided_markers = (
        "stegmusic.iphone-verification.v1",
        "GUIDED TEST",
        "Export verification receipt",
        "stegmusic-iphone-verification-receipt-v1",
        "local_file_playback_verified",
        "screen_dim_continuity_verified",
        "screen_lock_continuity_verified",
        "return_resume_verified",
        "iphone_guided_verification_step_completed",
        "window.StegMusicIphoneVerification",
    )
    enhancement_markers = (
        "createDynamicsCompressor",
        "compressor.threshold.value = -20",
        "output.gain.value = 1.28",
        "normalize(rendered, 0.94)",
        "audio.volume = 1",
        "chordProgressions",
        "harmony_voice_count",
        "complexity_level",
        "progressive_chord_pad_bass_countermelody",
        "double_attenuation_removed: true",
        "source_bytes_uploaded: false",
        "window.StegMusicEnhancement",
    )

    for marker in page_markers:
        if marker not in page:
            return fail(f"page missing marker: {marker}")
    for marker in runtime_markers:
        if marker not in runtime:
            return fail(f"runtime missing marker: {marker}")
    for marker in transport_markers:
        if marker not in transport:
            return fail(f"media transport missing marker: {marker}")
    for marker in guided_markers:
        if marker not in guided:
            return fail(f"guided verification missing marker: {marker}")
    for marker in enhancement_markers:
        if marker not in enhancement:
            return fail(f"enhancement missing marker: {marker}")

    if page.index("assets/ecosystem-music-diagnostics.js") < page.index("assets/ecosystem-music.js"):
        return fail("diagnostics runtime must load after the base music runtime")
    if "audible_output_confirmed: true" in runtime:
        return fail("automated self-test must not claim audible output")
    if "source_audio_upload" not in transport and "source_bytes_uploaded: false" not in transport:
        return fail("media transport must retain the no-upload boundary")
    if "source_bytes_uploaded: false" not in enhancement:
        return fail("enhancement must retain the no-upload boundary")

    print("STEGMUSIC_BROWSER_SELF_TEST_PASS")
    print("authority_effect=NONE")
    print("audibility_claim=human_confirmation_only")
    print("generated_media_transport=offline_render_to_html_audio_wav")
    print("guided_iphone_verification=enabled")
    print("loudness_strategy=compression_plus_peak_normalization")
    print("harmony_strategy=chord_pad_bass_countermelody")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
