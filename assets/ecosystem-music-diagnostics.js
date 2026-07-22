(() => {
  'use strict';

  const $ = id => document.getElementById(id);
  const delay = ms => new Promise(resolve => window.setTimeout(resolve, ms));

  function setResult(text, mode) {
    const el = $('audioSelfTestResult');
    if (!el) return;
    el.textContent = text;
    el.classList.remove('pending', 'active', 'failed');
    el.classList.add(mode);
  }

  function record(type, human, captured, derived) {
    window.dispatchEvent(new CustomEvent('stegmusic:emit', {
      detail: {
        type,
        human,
        governed: {
          rights_status: 'not_applicable',
          source_class: 'browser_runtime_diagnostic',
          captured_records: [captured],
          derived_records: [derived],
          contribution_eligibility: 'not_evaluated',
          royalty_state: 'not_realized',
          fixture: false
        }
      }
    }));
  }

  async function runSelfTest() {
    const button = $('audioSelfTest');
    const play = $('playPause');
    const progress = $('progress');
    const notice = $('audioNotice');
    const raw = $('rawEvents');

    if (!button || !play || !progress || !notice || !raw) {
      setResult('SELF-TEST · FAILED · required controls missing', 'failed');
      return;
    }

    button.disabled = true;
    setResult('SELF-TEST · RUNNING · starting browser audio', 'pending');
    const before = Number(progress.value);
    const startedAt = new Date().toISOString();

    try {
      if (play.textContent.trim().toLowerCase() !== 'pause') play.click();
      await delay(1800);

      const after = Number(progress.value);
      const audioActive = /running locally|active/i.test(notice.textContent);
      const playbackEvent = raw.textContent.includes('"event_type":"playback_started"');
      const advanced = after !== before;
      const passed = audioActive && playbackEvent && advanced;

      if (play.textContent.trim().toLowerCase() === 'pause') play.click();

      const captured = {
        started_at: startedAt,
        completed_at: new Date().toISOString(),
        user_agent: navigator.userAgent,
        progress_before: before,
        progress_after: after,
        audio_notice: notice.textContent,
        audio_active: audioActive,
        playback_event_observed: playbackEvent,
        composition_progress_advanced: advanced
      };

      if (!passed) {
        setResult('SELF-TEST · FAILED · inspect governed diagnostic event', 'failed');
        record('audio_self_test_failed', 'Browser audio self-test failed.', captured, {
          result: 'FAIL',
          authority: 'none',
          audible_output_confirmed: false,
          reason: !audioActive ? 'audio_context_not_active' : !playbackEvent ? 'playback_event_missing' : 'composition_did_not_advance'
        });
        return;
      }

      setResult('SELF-TEST · PASS · engine active, composition advanced, event emitted', 'active');
      record('audio_self_test_passed', 'Browser audio self-test passed.', captured, {
        result: 'PASS',
        authority: 'none',
        audible_output_confirmed: false,
        browser_runtime_execution_confirmed: true
      });
    } catch (error) {
      if (play.textContent.trim().toLowerCase() === 'pause') play.click();
      setResult(`SELF-TEST · FAILED · ${error.message}`, 'failed');
      record('audio_self_test_failed', `Browser audio self-test failed: ${error.message}`, {
        started_at: startedAt,
        completed_at: new Date().toISOString(),
        user_agent: navigator.userAgent,
        error: error.message
      }, {
        result: 'ERROR',
        authority: 'none',
        audible_output_confirmed: false
      });
    } finally {
      button.disabled = false;
    }
  }

  function loadIntentCompositionController() {
    if (window.StegMusicIntentComposition || document.querySelector('script[data-stegmusic-intent-composition]')) return;
    const script = document.createElement('script');
    script.src = 'assets/ecosystem-music-intent-composition.js';
    script.async = false;
    script.dataset.stegmusicIntentComposition = 'v1';
    document.body.appendChild(script);
  }

  const button = $('audioSelfTest');
  if (button) button.addEventListener('click', runSelfTest);
  loadIntentCompositionController();
  window.StegMusicDiagnostics = Object.freeze({ runSelfTest, loadIntentCompositionController });
})();