(() => {
  'use strict';

  const $ = id => document.getElementById(id);
  const emit = (type, human, captured = {}, derived = {}) => window.dispatchEvent(new CustomEvent('stegmusic:emit', {
    detail: {
      type,
      human,
      governed: {
        rights_status: 'stegdj_generated_local_prototype',
        source_class: 'generated_media_transport',
        captured_records: [captured],
        derived_records: [derived],
        contribution_eligibility: 'not_evaluated',
        royalty_state: 'not_realized',
        fixture: false,
        policy_refs: ['stegmusic-rights-boundary-v0', 'stegmusic-iphone-media-transport-v0']
      }
    }
  }));

  const state = {
    audio: null,
    objectUrl: null,
    rendering: false,
    playing: false,
    renderedTrackId: null,
    startedAt: null,
    hiddenAt: null,
    lastVisibility: document.visibilityState,
    lifecycle: []
  };

  const phases = [
    { start: 0, end: 15, density: 0.55, transpose: -5 },
    { start: 16, end: 31, density: 0.78, transpose: 0 },
    { start: 32, end: 47, density: 1, transpose: 7 },
    { start: 48, end: 63, density: 0.68, transpose: 0 }
  ];

  const clamp = (n, min, max) => Math.max(min, Math.min(max, n));
  const midiToHz = midi => 440 * Math.pow(2, (midi - 69) / 12);
  const currentTrack = () => window.StegMusicRuntime && window.StegMusicRuntime.getCurrentTrack ? window.StegMusicRuntime.getCurrentTrack() : null;
  const currentControls = () => ({
    energy: Number($('energy')?.value || 58),
    brightness: Number($('brightness')?.value || 38),
    bass: Number($('bass')?.value || 72),
    exploration: Number($('exploration')?.value || 32),
    volume: Number($('volume')?.value || 32),
    session_intent: $('sessionIntent')?.value || 'fine_tune'
  });

  function setNotice(text, failed = false) {
    const notice = $('audioNotice');
    if (notice) notice.textContent = text;
    const status = $('statusAudio');
    if (status) {
      status.textContent = failed ? 'AUDIO MEDIA · BLOCKED' : 'AUDIO MEDIA · ACTIVE';
      status.classList.remove('pending', 'active', 'failed');
      status.classList.add(failed ? 'failed' : 'active');
    }
  }

  function ensureAudioElement() {
    if (state.audio) return state.audio;
    const audio = document.createElement('audio');
    audio.id = 'generatedMediaPlayer';
    audio.preload = 'auto';
    audio.playsInline = true;
    audio.setAttribute('playsinline', '');
    audio.setAttribute('webkit-playsinline', '');
    audio.style.display = 'none';
    document.body.appendChild(audio);
    audio.addEventListener('play', () => {
      state.playing = true;
      state.startedAt = state.startedAt || new Date().toISOString();
      if ($('playPause')) $('playPause').textContent = 'Pause';
      setNotice('AUDIO · generated media playing through iPhone-safe transport');
    });
    audio.addEventListener('pause', () => {
      state.playing = false;
      if ($('playPause')) $('playPause').textContent = 'Play';
      if (!audio.ended) setNotice('AUDIO · paused; tap Play to resume');
    });
    audio.addEventListener('timeupdate', () => {
      if ($('progress') && Number.isFinite(audio.duration) && audio.duration > 0) $('progress').value = String(audio.currentTime / audio.duration * 100);
    });
    audio.addEventListener('ended', () => {
      state.playing = false;
      if ($('playPause')) $('playPause').textContent = 'Play';
      setNotice('AUDIO · generated composition completed');
      emit('generated_media_completed', 'Generated StegDJ media completed.', {
        track_id: state.renderedTrackId,
        duration: audio.duration,
        completed: true,
        transport: 'html_audio_blob_wav'
      }, { completion_signal: 'html_audio_ended' });
    });
    audio.addEventListener('error', () => {
      setNotice('AUDIO · generated media could not be decoded or played', true);
      emit('generated_media_playback_refused', 'Generated StegDJ media playback failed.', {
        track_id: state.renderedTrackId,
        media_error_code: audio.error && audio.error.code,
        user_agent: navigator.userAgent
      }, { failure_class: 'html_audio_decode_or_playback_failure' });
    });
    state.audio = audio;
    return audio;
  }

  function addVoice(ctx, destination, frequency, start, duration, type, level, cutoff) {
    const oscillator = ctx.createOscillator();
    const gain = ctx.createGain();
    const filter = ctx.createBiquadFilter();
    oscillator.type = type;
    oscillator.frequency.setValueAtTime(frequency, start);
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(cutoff, start);
    gain.gain.setValueAtTime(0.0001, start);
    gain.gain.exponentialRampToValueAtTime(Math.max(0.0002, level), start + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, start + duration);
    oscillator.connect(filter);
    filter.connect(gain);
    gain.connect(destination);
    oscillator.start(start);
    oscillator.stop(start + duration + 0.03);
  }

  function encodeWav(buffer) {
    const channels = buffer.numberOfChannels;
    const sampleRate = buffer.sampleRate;
    const frames = buffer.length;
    const bytesPerSample = 2;
    const dataSize = frames * channels * bytesPerSample;
    const out = new ArrayBuffer(44 + dataSize);
    const view = new DataView(out);
    const writeString = (offset, value) => { for (let i = 0; i < value.length; i += 1) view.setUint8(offset + i, value.charCodeAt(i)); };
    writeString(0, 'RIFF');
    view.setUint32(4, 36 + dataSize, true);
    writeString(8, 'WAVE');
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, channels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * channels * bytesPerSample, true);
    view.setUint16(32, channels * bytesPerSample, true);
    view.setUint16(34, 16, true);
    writeString(36, 'data');
    view.setUint32(40, dataSize, true);
    const data = Array.from({ length: channels }, (_, channel) => buffer.getChannelData(channel));
    let offset = 44;
    for (let frame = 0; frame < frames; frame += 1) {
      for (let channel = 0; channel < channels; channel += 1) {
        const sample = clamp(data[channel][frame], -1, 1);
        view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7fff, true);
        offset += 2;
      }
    }
    return new Blob([out], { type: 'audio/wav' });
  }

  async function renderCurrentTrack() {
    if (state.rendering) return null;
    const track = currentTrack();
    if (!track) throw new Error('No generated track is selected.');
    const controls = currentControls();
    state.rendering = true;
    setNotice(`AUDIO · rendering “${track.title}” for reliable media playback`);
    try {
      const sampleRate = 44100;
      const beat = 60 / track.bpm;
      const duration = Math.max(20, 64 * beat / 2 + 1);
      const OfflineCtor = window.OfflineAudioContext || window.webkitOfflineAudioContext;
      if (!OfflineCtor) throw new Error('Offline audio rendering is not supported by this browser.');
      const ctx = new OfflineCtor(2, Math.ceil(sampleRate * duration), sampleRate);
      const master = ctx.createGain();
      master.gain.value = clamp(controls.volume / 100, 0.08, 0.72);
      master.connect(ctx.destination);
      for (let step = 0; step < 64; step += 1) {
        const phase = phases.find(item => step >= item.start && step <= item.end) || phases[0];
        const time = step * beat / 2;
        let note = track.root + track.pattern[step % track.pattern.length] + phase.transpose;
        if (controls.exploration > 65 && step % 16 === 12) note += 12;
        const leadType = controls.brightness > 60 ? 'sawtooth' : controls.brightness > 35 ? 'triangle' : 'sine';
        addVoice(ctx, master, midiToHz(note), time, beat * (0.52 + phase.density * 0.28), leadType, (0.024 + controls.energy / 5200) * phase.density, 450 + controls.brightness * 34);
        if (step % 2 === 0) addVoice(ctx, master, midiToHz(track.root - 12 + (step >= 32 && step <= 47 ? 5 : 0)), time, beat * 0.88, 'sine', (0.038 + controls.bass / 2600) * phase.density, 160 + controls.bass * 6);
        if (step % 4 === 0) addVoice(ctx, master, 58 + controls.energy / 10, time, 0.12, 'sine', 0.07 * phase.density, 130);
      }
      const rendered = await ctx.startRendering();
      const blob = encodeWav(rendered);
      if (state.objectUrl) URL.revokeObjectURL(state.objectUrl);
      state.objectUrl = URL.createObjectURL(blob);
      const audio = ensureAudioElement();
      audio.src = state.objectUrl;
      audio.load();
      state.renderedTrackId = track.id;
      emit('generated_media_rendered', `Rendered “${track.title}” as a browser-local media item.`, {
        track_id: track.id,
        title: track.title,
        duration_seconds: duration,
        bytes: blob.size,
        mime_type: blob.type,
        transport: 'offline_audio_context_to_wav_blob',
        user_agent: navigator.userAgent,
        controls
      }, {
        media_session_eligible: 'mediaSession' in navigator,
        source_bytes_uploaded: false,
        catalog_license_implied: false
      });
      return audio;
    } finally {
      state.rendering = false;
    }
  }

  async function play() {
    try {
      window.StegMusicRuntime?.stopGenerated?.();
      window.dispatchEvent(new CustomEvent('stegmusic:pause-local-source'));
      const track = currentTrack();
      let audio = ensureAudioElement();
      if (!audio.src || state.renderedTrackId !== track?.id) audio = await renderCurrentTrack();
      audio.volume = clamp(Number($('volume')?.value || 32) / 100, 0.08, 1);
      await audio.play();
      state.startedAt = new Date().toISOString();
      emit('generated_media_playback_started', `Playing rendered StegDJ media “${track.title}”.`, {
        track_id: track.id,
        title: track.title,
        current_time: audio.currentTime,
        duration: Number.isFinite(audio.duration) ? audio.duration : null,
        transport: 'html_audio_blob_wav',
        visibility_state: document.visibilityState,
        user_agent: navigator.userAgent
      }, {
        iPhone_safe_transport_requested: true,
        human_audibility_confirmed: false
      });
      updateMediaSession(track);
    } catch (error) {
      setNotice(`AUDIO · ${error.message}`, true);
      emit('generated_media_playback_refused', `Generated media playback could not start: ${error.message}`, {
        error: error.message,
        user_agent: navigator.userAgent,
        visibility_state: document.visibilityState
      }, { failure_class: 'media_play_rejected_or_render_failed' });
    }
  }

  function pause(record = true) {
    const audio = ensureAudioElement();
    audio.pause();
    if (record) emit('generated_media_playback_paused', 'Paused rendered StegDJ media.', {
      track_id: state.renderedTrackId,
      current_time: audio.currentTime,
      visibility_state: document.visibilityState
    }, { transport: 'html_audio_blob_wav' });
  }

  function stop(record = true) {
    const audio = ensureAudioElement();
    audio.pause();
    audio.currentTime = 0;
    if ($('progress')) $('progress').value = '0';
    if (record) emit('generated_media_playback_stopped', 'Stopped rendered StegDJ media.', {
      track_id: state.renderedTrackId,
      visibility_state: document.visibilityState
    }, { transport: 'html_audio_blob_wav' });
  }

  function updateMediaSession(track) {
    if (!('mediaSession' in navigator)) return;
    try {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: track.title,
        artist: 'StegDJ',
        album: 'StegMusic generated prototype'
      });
      navigator.mediaSession.setActionHandler('play', play);
      navigator.mediaSession.setActionHandler('pause', () => pause(true));
      navigator.mediaSession.setActionHandler('stop', () => stop(true));
      navigator.mediaSession.setActionHandler('previoustrack', () => $('previousButton')?.click());
      navigator.mediaSession.setActionHandler('nexttrack', () => $('adaptiveNext')?.click());
    } catch (error) {
      emit('media_session_configuration_failed', 'Media Session controls could not be fully configured.', { error: error.message }, { authority: 'none' });
    }
  }

  function addConfirmationPanel() {
    const player = $('audioSelfTestResult')?.parentElement;
    if (!player || $('iphonePlaybackVerification')) return;
    const panel = document.createElement('section');
    panel.id = 'iphonePlaybackVerification';
    panel.className = 'audio-notice';
    panel.setAttribute('aria-label', 'iPhone playback verification');
    panel.innerHTML = '<strong>IPHONE PLAYBACK VERIFICATION</strong><p class="muted">Confirm only what you directly observed on this device.</p><div class="player-actions"><button class="sv-btn sv-btn-primary" type="button" data-confirm="audible">I hear audio</button><button class="sv-btn sv-btn-secondary" type="button" data-confirm="adaptive">Adaptive Next worked</button><button class="sv-btn sv-btn-secondary" type="button" data-confirm="dimmed">Continued while screen dimmed</button><button class="sv-btn sv-btn-secondary" type="button" data-confirm="locked">Continued while screen locked</button><button class="sv-btn sv-btn-secondary" type="button" data-confirm="resumed">Resumed after returning</button></div><div class="status pending" id="iphoneVerificationStatus">TARGET DEVICE · awaiting direct observation</div>';
    player.appendChild(panel);
    panel.querySelectorAll('[data-confirm]').forEach(button => button.addEventListener('click', () => {
      const kind = button.dataset.confirm;
      const audio = ensureAudioElement();
      const captured = {
        confirmation: kind,
        confirmed_at: new Date().toISOString(),
        track_id: state.renderedTrackId,
        current_time: audio.currentTime,
        paused: audio.paused,
        ended: audio.ended,
        visibility_state: document.visibilityState,
        lifecycle: state.lifecycle.slice(-20),
        user_agent: navigator.userAgent,
        media_session_available: 'mediaSession' in navigator
      };
      const human = {
        audible: 'Human confirmed audible output on this target device.',
        adaptive: 'Human confirmed Adaptive Next playback on this target device.',
        dimmed: 'Human confirmed playback continued while the screen was dimmed.',
        locked: 'Human confirmed playback continued while the screen was locked.',
        resumed: 'Human confirmed playback resumed after returning to the page.'
      }[kind];
      emit(`iphone_playback_${kind}_confirmed`, human, captured, {
        direct_human_observation: true,
        human_audibility_confirmed: kind === 'audible',
        authority: 'none'
      });
      const status = $('iphoneVerificationStatus');
      if (status) {
        status.textContent = `TARGET DEVICE · ${kind.toUpperCase()} CONFIRMED`;
        status.classList.remove('pending', 'failed');
        status.classList.add('active');
      }
    }));
  }

  function bindControls() {
    const playButton = $('playPause');
    const stopButton = $('stopButton');
    if (playButton) playButton.addEventListener('click', event => {
      event.preventDefault();
      event.stopImmediatePropagation();
      state.playing ? pause(true) : play();
    }, true);
    if (stopButton) stopButton.addEventListener('click', event => {
      event.preventDefault();
      event.stopImmediatePropagation();
      stop(true);
    }, true);
    ['previousButton', 'nextButton', 'adaptiveNext', 'surpriseButton'].forEach(id => {
      const button = $(id);
      if (!button) return;
      button.addEventListener('click', () => {
        const shouldResume = state.playing;
        stop(false);
        window.setTimeout(async () => {
          state.renderedTrackId = null;
          if (shouldResume) await play();
        }, 0);
      });
    });
    $('volume')?.addEventListener('input', () => {
      if (state.audio) state.audio.volume = clamp(Number($('volume').value) / 100, 0.08, 1);
    });
    $('progress')?.addEventListener('change', () => {
      if (!state.audio || !Number.isFinite(state.audio.duration)) return;
      state.audio.currentTime = Number($('progress').value) / 100 * state.audio.duration;
    });
  }

  function bindLifecycle() {
    const recordLifecycle = type => {
      const audio = ensureAudioElement();
      const item = {
        type,
        at: new Date().toISOString(),
        visibility_state: document.visibilityState,
        paused: audio.paused,
        current_time: audio.currentTime
      };
      state.lifecycle.push(item);
      if (state.lifecycle.length > 50) state.lifecycle.shift();
      emit('iphone_media_lifecycle_observed', `Observed media lifecycle transition: ${type}.`, item, {
        playback_continuity_observed: !audio.paused,
        human_audibility_confirmed: false
      });
    };
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'hidden') state.hiddenAt = new Date().toISOString();
      recordLifecycle(`visibility_${document.visibilityState}`);
      state.lastVisibility = document.visibilityState;
    });
    window.addEventListener('pagehide', () => recordLifecycle('pagehide'));
    window.addEventListener('pageshow', event => recordLifecycle(event.persisted ? 'pageshow_bfcache' : 'pageshow'));
    window.addEventListener('freeze', () => recordLifecycle('freeze'));
    window.addEventListener('resume', () => recordLifecycle('resume'));
  }

  addConfirmationPanel();
  bindControls();
  bindLifecycle();
  ensureAudioElement();
  window.StegMusicMediaTransport = Object.freeze({ play, pause, stop, renderCurrentTrack, getState: () => ({ ...state, audio: undefined }) });
  emit('generated_media_transport_ready', 'iPhone-safe generated media transport is ready.', {
    user_agent: navigator.userAgent,
    offline_audio_context_available: Boolean(window.OfflineAudioContext || window.webkitOfflineAudioContext),
    media_session_available: 'mediaSession' in navigator,
    html_audio_available: typeof HTMLAudioElement !== 'undefined'
  }, {
    transport: 'offline_render_to_html_audio_wav',
    human_audibility_confirmed: false
  });
})();
