#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "ecosystem-music.html"
RUNTIME = ROOT / "assets" / "ecosystem-music-diagnostics.js"
MEDIA_TRANSPORT = ROOT / "assets" / "ecosystem-music-media-transport.js"
IPHONE_VERIFICATION = ROOT / "assets" / "ecosystem-music-iphone-verification.js"
SIX_TRACK = ROOT / "assets" / "ecosystem-music-six-track-registry.js"
STYLE_REGISTRY = ROOT / "assets" / "stegmusic-style-characteristics.json"
STYLE_RESOLVER = ROOT / "assets" / "ecosystem-music-style-resolver.js"
ENHANCEMENT = ROOT / "assets" / "ecosystem-music-enhancement.js"


def fail(message: str) -> int:
    print(f"STEGMUSIC_BROWSER_SELF_TEST_FAIL: {message}")
    return 1


def require(text: str, markers: tuple[str, ...], label: str) -> int | None:
    for marker in markers:
        if marker not in text:
            return fail(f"{label} missing marker: {marker}")
    return None


def main() -> int:
    paths = (PAGE, RUNTIME, MEDIA_TRANSPORT, IPHONE_VERIFICATION, SIX_TRACK, STYLE_REGISTRY, STYLE_RESOLVER, ENHANCEMENT)
    for path in paths:
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    page = PAGE.read_text(encoding="utf-8")
    runtime = RUNTIME.read_text(encoding="utf-8")
    runtime_compact = "".join(runtime.split())
    transport = MEDIA_TRANSPORT.read_text(encoding="utf-8")
    guided = IPHONE_VERIFICATION.read_text(encoding="utf-8")
    six_track = SIX_TRACK.read_text(encoding="utf-8")
    style_registry = STYLE_REGISTRY.read_text(encoding="utf-8")
    style_resolver = STYLE_RESOLVER.read_text(encoding="utf-8")
    enhancement = ENHANCEMENT.read_text(encoding="utf-8")
    enhancement_compact = "".join(enhancement.split())

    checks = (
        (page, ('id="audioSelfTest"', 'id="audioSelfTestResult"', 'Run audio self-test', 'assets/ecosystem-music-diagnostics.js', 'confirms browser execution, not audibility'), 'page'),
        (runtime, ('StegMusicDiagnostics', 'audio_self_test_passed', 'audio_self_test_failed', 'composition_progress_advanced', 'playback_event_observed', 'generated_media_transport_confirmed', 'guided_verification_runtime_confirmed', 'six_track_registry_confirmed', 'style_resolver_confirmed', 'loudness_harmony_enhancement_confirmed', 'assets/ecosystem-music-style-resolver.js', "window.dispatchEvent(new CustomEvent('stegmusic:emit'"), 'runtime'),
        (transport, ('OfflineAudioContext', 'encodeWav', 'generatedMediaPlayer', 'html_audio_blob_wav', 'navigator.mediaSession', 'visibilitychange', 'pagehide', 'pageshow', 'iphonePlaybackVerification', 'I hear audio', "human_audibility_confirmed: kind === 'audible'", 'source_bytes_uploaded: false', 'window.StegMusicMediaTransport'), 'media transport'),
        (guided, ('stegmusic.iphone-verification.v1', 'GUIDED TEST', 'Export verification receipt', 'screen_dim_continuity_verified', 'screen_lock_continuity_verified', 'return_resume_verified', 'window.StegMusicIphoneVerification'), 'guided verification'),
        (six_track, ('StegMusicSixTrackRegistry', 'track_count:tracks.length', 'enhanced_renderer_compatible:true'), 'six-track registry'),
        (style_registry, ('stegmusic-style-characteristics-v1', 'edm_high_energy_bass_drop', 'drop_prominence', 'minimum_drop_count', 'audible_pre_drop_contrast', 'sub_bass_entry_at_drop', 'external_vocabularies_are_reference_only'), 'style registry'),
        (style_resolver, ('StegMusicStyleResolver', 'getActiveProfile', 'explicit_characteristics_control_rendering', 'stegmusic_style_profile_applied', 'edm_high_energy_bass_drop'), 'style resolver'),
        (enhancement, ('createDynamicsCompressor', 'compressor.threshold.value=-20', 'output.gain.value=1.28', 'normalize(rendered,.94)', 'audio.volume=1', 'chordProgressions', 'edmDropPhases', 'pre_drop_tension', 'bass_drop', 'larger_drop', 'dropCount>=2', 'profile_required_events_encoded', 'clear_buildup_encoded', 'audible_pre_drop_contrast_encoded', 'sub_bass_entry_at_drop_encoded', 'rhythmic_density_increase_at_drop_encoded', 'secondary_release_encoded', 'source_bytes_uploaded:false', 'window.StegMusicEnhancement'), 'enhancement'),
    )
    for text, markers, label in checks:
        result = require(text, markers, label)
        if result is not None:
            return result

    if "audible_output_confirmed:false" not in runtime_compact:
        return fail("runtime missing false automated audibility boundary")
    if "browser_runtime_execution_confirmed:true" not in runtime_compact:
        return fail("runtime missing true browser execution result")
    if "audible_output_confirmed:true" in runtime_compact:
        return fail("automated self-test must not claim audible output")
    if "human_audibility_confirmed:true" in enhancement_compact:
        return fail("renderer must not claim human audibility")
    if page.index("assets/ecosystem-music-diagnostics.js") < page.index("assets/ecosystem-music.js"):
        return fail("diagnostics runtime must load after the base music runtime")

    print("STEGMUSIC_BROWSER_SELF_TEST_PASS")
    print("authority_effect=NONE")
    print("audibility_claim=human_confirmation_only")
    print("generated_media_transport=offline_render_to_html_audio_wav")
    print("guided_iphone_verification=enabled")
    print("style_registry=governed_explicit_characteristics")
    print("style_profile=edm_high_energy_bass_drop")
    print("arrangement_strategy=profile_governed_36_bar_two_drop_arc")
    print("bass_strategy=withheld_pre_drop_then_sub_bass_release")
    print("loudness_strategy=compression_plus_peak_normalization")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
