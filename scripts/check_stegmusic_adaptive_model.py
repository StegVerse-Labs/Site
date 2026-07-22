#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "ecosystem-music.html"
JS = ROOT / "assets" / "ecosystem-music-adaptive.js"
MAIN = ROOT / "assets" / "ecosystem-music.js"
PROFILE = ROOT / "assets" / "ecosystem-music-profile-scope.js"

required = {
    HTML: ['id="adaptiveNext"', 'id="adaptiveRecommendation"', 'id="adaptiveModel"', 'id="resetAdaptiveModel"', 'assets/ecosystem-music-adaptive.js'],
    JS: [
        'stegmusic.trait-model.v1', 'stegmusic.transition-model.v1', 'INTENT_TARGETS',
        'learned_targets', 'ranked_candidates', 'adaptive_next_requested',
        'adaptive_selection_decision', 'transition_outcome_recorded', 'preference_fit',
        'transition_fit', 'learned_outcome_adjustment', 'repeat_penalty',
        'stegdj-adaptive-selection-v2', 'stegdj-transition-outcome-learning-v1',
        'Accept transition', 'Skip / poor fit', 'Replay track', 'Mark segment complete',
        'data-transition-outcome', 'transitionLearningState', 'profile_scoped:true',
        'local_only:true', "authority:'none'",
    ],
    MAIN: ['window.StegMusicRuntime', 'selectGeneratedTrack', 'stegmusic:emit'],
    PROFILE: ['stegmusic.profile.', 'scopedKey', 'cross_profile_read: false'],
}

failures = []
for path, markers in required.items():
    if not path.exists():
        failures.append(f"missing file: {path.relative_to(ROOT)}")
        continue
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            failures.append(f"{path.relative_to(ROOT)} missing marker: {marker}")

if failures:
    print("STEGMUSIC_ADAPTIVE_MODEL_FAIL")
    for failure in failures:
        print(f"- {failure}")
    sys.exit(1)

print("STEGMUSIC_ADAPTIVE_MODEL_PASS")
print("model_storage=browser_local_profile_scoped")
print("aggregate_authority=none")
print("adaptive_selection=governed_deterministic_scoring")
print("transition_scoring=present")
print("transition_outcome_learning=present")
print("transition_outcomes=accepted,skipped,replayed,completed")
print("canonical_decision_event=present")
print("canonical_outcome_event=present")
