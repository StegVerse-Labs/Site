(() => {
  'use strict';

  const $ = id => document.getElementById(id);
  const clamp = (n, min, max) => Math.max(min, Math.min(max, n));
  const midiToHz = midi => 440 * Math.pow(2, (midi - 69) / 12);
  const delay = ms => new Promise(resolve => window.setTimeout(resolve, ms));
  const emit = (type, human, captured = {}, derived = {}) => window.dispatchEvent(new CustomEvent('stegmusic:emit', {
    detail: {
      type,
      human,
      governed: {
        rights_status: 'stegdj_generated_local_prototype',
        source_class: 'generated_media_enhancement',
        captured_records: [captured],
        derived_records: [derived],
        contribution_eligibility: 'not_evaluated',
        royalty_state: 'not_realized',
        fixture: false,
        policy_refs: ['stegmusic-rights-boundary-v0', 'stegmusic-loudness-harmony-v0']
      }
    }
  }));

  const state = { audio: null, objectUrl: null, trackId: null, playing: false, rendering: false, resumeAfterSelection: false };
  const chordProgressions = [
    [[0, 3, 7], [5, 8, 12], [3, 7, 10], [7, 10, 14]],
    [[0, 4, 7], [7, 11, 14], [9, 12, 16], [5, 9, 12]],
    [[0, 3, 7, 10], [5, 8, 12, 15], [7, 10, 14, 17], [3, 7, 10, 14]]
  ];

  const controls = () => ({
    energy: Number($('energy')?.value || 58),
    brightness: Number($('brightness')?.value || 38),
    bass: Number($('bass')?.value || 72),
    exploration: Number($('exploration')?.value || 32),
    volume: Number($('volume')?.value || 32),
    intent: $('sessionIntent')?.value || 'fine_tune'
  });

  function setNotice(text, failed = false) {
    if ($('audioNotice')) $('audioNotice').textContent = text;
    const status = $('statusAudio');
    if (status) {
      status.textContent = failed ? 'AUDIO ENHANCEMENT · BLOCKED' : 'AUDIO ENHANCEMENT · ACTIVE';
      status.classList.remove('pending', 'active', 'failed');
      status.classList.add(failed ? 'failed' : 'active');
    }
  }

  function audioElement() {
    if (state.audio) return state.audio;
    state.audio = $('generatedMediaPlayer') || document.createElement('audio');
    if (!state.audio.id) {
      state.audio.id = 'generatedMediaPlayer';
      state.audio.preload = 'auto';
      state.audio.playsInline = true;
      state.audio.style.display = 'none';
      document.body.appendChild(state.audio);
    }
    state.audio.addEventListener('play', () => {
      state.playing = true;
      if ($('playPause')) $('playPause').textContent = 'Pause';
      setNotice('AUDIO · normalized harmonic mix playing');
    });
    state.audio.addEventListener('pause', () => {
      state.playing = false;
      if ($('playPause')) $('playPause').textContent = 'Play';
    });
    state.audio.addEventListener('timeupdate', () => {
      if ($('progress') && Number.isFinite(state.audio.duration) && state.audio.duration > 0) $('progress').value = String(state.audio.currentTime / state.audio.duration * 100);
    });
    return state.audio;
  }

  function voice(ctx, destination, frequency, start, duration, type, level, cutoff, pan = 0, attack = 0.015) {
    const oscillator = ctx.createOscillator();
    const filter = ctx.createBiquadFilter();
    const gain = ctx.createGain();
    const panner = ctx.createStereoPanner ? ctx.createStereoPanner() : null;
    oscillator.type = type;
    oscillator.frequency.setValueAtTime(frequency, start);
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(cutoff, start);
    gain.gain.setValueAtTime(0.0001, start);
    gain.gain.exponentialRampToValueAtTime(Math.max(0.0002, level), start + attack);
    gain.gain.exponentialRampToValueAtTime(0.0001, start + duration);
    oscillator.connect(filter);
    filter.connect(gain);
    if (panner) {
      panner.pan.setValueAtTime(clamp(pan, -1, 1), start);
      gain.connect(panner);
      panner.connect(destination);
    } else gain.connect(destination);
    oscillator.start(start);
    oscillator.stop(start + duration + 0.04);
  }

  function percussion(ctx, destination, start, level, bright) {
    const length = Math.max(1, Math.floor(ctx.sampleRate * 0.09));
    const buffer = ctx.createBuffer(1, length, ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < length; i += 1) data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / length, 2.5);
    const source = ctx.createBufferSource();
    const filter = ctx.createBiquadFilter();
    const gain = ctx.createGain();
    source.buffer = buffer;
    filter.type = 'highpass';
    filter.frequency.value = 1800 + bright * 45;
    gain.gain.setValueAtTime(level, start);
    gain.gain.exponentialRampToValueAtTime(0.0001, start + 0.1);
    source.connect(filter);
    filter.connect(gain);
    gain.connect(destination);
    source.start(start);
  }

  function normalize(buffer, targetPeak = 0.94) {
    let peak = 0;
    for (let channel = 0; channel < buffer.numberOfChannels; channel += 1) {
      const data = buffer.getChannelData(channel);
      for (let i = 0; i < data.length; i += 1) peak = Math.max(peak, Math.abs(data[i]));
    }
    const gain = peak > 0 ? Math.min(8, targetPeak / peak) : 1;
    for (let channel = 0; channel < buffer.numberOfChannels; channel += 1) {
      const data = buffer.getChannelData(channel);
      for (let i = 0; i < data.length; i += 1) data[i] = clamp(data[i] * gain, -1, 1);
    }
    return { peakBefore: peak, normalizationGain: gain, targetPeak };
  }

  function encodeWav(buffer) {
    const channels = buffer.numberOfChannels;
    const frames = buffer.length;
    const sampleRate = buffer.sampleRate;
    const out = new ArrayBuffer(44 + frames * channels * 2);
    const view = new DataView(out);
    const text = (offset, value) => { for (let i = 0; i < value.length; i += 1) view.setUint8(offset + i, value.charCodeAt(i)); };
    text(0, 'RIFF'); view.setUint32(4, 36 + frames * channels * 2, true); text(8, 'WAVE'); text(12, 'fmt ');
    view.setUint32(16, 16, true); view.setUint16(20, 1, true); view.setUint16(22, channels, true);
    view.setUint32(24, sampleRate, true); view.setUint32(28, sampleRate * channels * 2, true);
    view.setUint16(32, channels * 2, true); view.setUint16(34, 16, true); text(36, 'data');
    view.setUint32(40, frames * channels * 2, true);
    let offset = 44;
    for (let frame = 0; frame < frames; frame += 1) {
      for (let channel = 0; channel < channels; channel += 1) {
        const sample = clamp(buffer.getChannelData(channel)[frame], -1, 1);
        view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7fff, true);
        offset += 2;
      }
    }
    return new Blob([out], { type: 'audio/wav' });
  }

  async function render() {
    if (state.rendering) return null;
    const track = window.StegMusicRuntime?.getCurrentTrack?.();
    if (!track) throw new Error('No generated track is selected.');
    state.rendering = true;
    setNotice(`AUDIO · building harmonic mix for “${track.title}”`);
    try {
      const c = controls();
      const OfflineCtor = window.OfflineAudioContext || window.webkitOfflineAudioContext;
      if (!OfflineCtor) throw new Error('Offline audio rendering is unavailable.');
      const sampleRate = 44100;
      const beat = 60 / track.bpm;
      const duration = Math.max(24, 64 * beat / 2 + 2);
      const ctx = new OfflineCtor(2, Math.ceil(sampleRate * duration), sampleRate);
      const mix = ctx.createGain();
      const compressor = ctx.createDynamicsCompressor();
      const output = ctx.createGain();
      compressor.threshold.value = -20;
      compressor.knee.value = 18;
      compressor.ratio.value = 4.5;
      compressor.attack.value = 0.008;
      compressor.release.value = 0.18;
      output.gain.value = 1.28;
      mix.connect(compressor);
      compressor.connect(output);
      output.connect(ctx.destination);

      const progression = chordProgressions[c.exploration > 66 ? 2 : c.brightness > 48 ? 1 : 0];
      const complexity = clamp(Math.round(1 + c.exploration / 22 + c.energy / 35), 2, 8);
      for (let bar = 0; bar < 8; bar += 1) {
        const chord = progression[bar % progression.length];
        const chordStart = bar * beat * 4;
        chord.forEach((interval, index) => {
          voice(ctx, mix, midiToHz(track.root + interval), chordStart, beat * 3.8, index % 2 ? 'triangle' : 'sine', 0.055 + c.energy / 5000, 900 + c.brightness * 25, (index - 1.5) * 0.28, 0.12);
        });
        voice(ctx, mix, midiToHz(track.root - 12 + chord[0]), chordStart, beat * 3.5, 'sine', 0.11 + c.bass / 1100, 180 + c.bass * 7, 0, 0.025);
      }

      for (let step = 0; step < 64; step += 1) {
        const time = step * beat / 2;
        const phaseDensity = step < 16 ? 0.62 : step < 32 ? 0.82 : step < 48 ? 1 : 0.72;
        let note = track.root + track.pattern[step % track.pattern.length] + (step >= 32 && step < 48 ? 7 : 0);
        if (c.exploration > 65 && step % 16 === 12) note += 12;
        const leadType = c.brightness > 60 ? 'sawtooth' : c.brightness > 35 ? 'triangle' : 'sine';
        voice(ctx, mix, midiToHz(note), time, beat * 0.42, leadType, (0.07 + c.energy / 1800) * phaseDensity, 700 + c.brightness * 40, step % 2 ? 0.18 : -0.18);
        if (complexity >= 4 && step % 2 === 1) voice(ctx, mix, midiToHz(note - 12 + (step % 8 === 7 ? 5 : 0)), time + beat * 0.08, beat * 0.34, 'triangle', 0.035 * phaseDensity, 950 + c.brightness * 18, step % 4 === 1 ? -0.42 : 0.42);
        if (complexity >= 6 && step % 4 === 2) voice(ctx, mix, midiToHz(note + 7), time + beat * 0.16, beat * 0.24, 'sine', 0.025 * phaseDensity, 1600, 0.55);
        if (step % 4 === 0) voice(ctx, mix, 52 + c.energy / 8, time, 0.16, 'sine', 0.19, 140, 0);
        if (step % 2 === 0 && complexity >= 3) percussion(ctx, mix, time + beat * 0.25, 0.045 + c.energy / 5000, c.brightness);
        if (complexity >= 7 && step % 8 === 7) percussion(ctx, mix, time + beat * 0.37, 0.028, c.brightness + 20);
      }

      const rendered = await ctx.startRendering();
      const normalized = normalize(rendered, 0.94);
      const blob = encodeWav(rendered);
      if (state.objectUrl) URL.revokeObjectURL(state.objectUrl);
      state.objectUrl = URL.createObjectURL(blob);
      const audio = audioElement();
      audio.pause();
      audio.src = state.objectUrl;
      audio.volume = 1;
      audio.load();
      state.trackId = track.id;
      emit('generated_harmonic_mix_rendered', `Rendered louder harmonic StegDJ mix “${track.title}”.`, {
        track_id: track.id,
        title: track.title,
        duration_seconds: duration,
        bytes: blob.size,
        compressor: { threshold_db: -20, knee_db: 18, ratio: 4.5, attack_seconds: 0.008, release_seconds: 0.18 },
        output_gain: 1.28,
        peak_before_normalization: normalized.peakBefore,
        normalization_gain: normalized.normalizationGain,
        normalized_target_peak: normalized.targetPeak,
        harmony_voice_count: progression[0].length,
        complexity_level: complexity,
        html_audio_volume: 1,
        controls: c,
        source_bytes_uploaded: false
      }, {
        perceived_loudness_strategy: 'compression_output_gain_peak_normalization',
        harmony_strategy: 'progressive_chord_pad_bass_countermelody',
        clipping_prevention: 'normalized_peak_0_94',
        human_audibility_confirmed: false
      });
      return audio;
    } finally {
      state.rendering = false;
    }
  }

  async function play() {
    try {
      window.StegMusicMediaTransport?.stop?.(false);
      const track = window.StegMusicRuntime?.getCurrentTrack?.();
      let audio = audioElement();
      if (!audio.src || state.trackId !== track?.id) audio = await render();
      audio.volume = 1;
      await audio.play();
      emit('enhanced_media_playback_started', `Playing louder harmonic mix “${track.title}”.`, {
        track_id: track.id,
        html_audio_volume: audio.volume,
        player_volume_control: Number($('volume')?.value || 32),
        user_agent: navigator.userAgent
      }, { transport: 'normalized_compressed_wav_html_audio' });
    } catch (error) {
      setNotice(`AUDIO · ${error.message}`, true);
      emit('enhanced_media_playback_refused', `Enhanced playback failed: ${error.message}`, { error: error.message }, { authority: 'none' });
    }
  }

  function pause() { audioElement().pause(); }
  function stop() { const audio = audioElement(); audio.pause(); audio.currentTime = 0; if ($('progress')) $('progress').value = '0'; }

  function replaceButton(id, handler) {
    const old = $(id);
    if (!old) return;
    const fresh = old.cloneNode(true);
    old.replaceWith(fresh);
    fresh.addEventListener('click', event => { event.preventDefault(); handler(); });
  }

  async function initialize() {
    for (let i = 0; i < 80 && !window.StegMusicRuntime; i += 1) await delay(50);
    if (!window.StegMusicRuntime) return;
    replaceButton('playPause', () => state.playing ? pause() : play());
    replaceButton('stopButton', stop);
    ['previousButton', 'nextButton', 'adaptiveNext', 'surpriseButton'].forEach(id => {
      const button = $(id);
      if (!button) return;
      button.addEventListener('click', () => {
        const resume = state.playing;
        stop();
        window.setTimeout(async () => {
          state.trackId = null;
          if (resume) await play();
        }, 20);
      });
    });
    $('volume')?.addEventListener('input', () => {
      state.trackId = null;
      setNotice('AUDIO · volume change will be applied on the next rendered mix');
    });
    window.StegMusicEnhancement = Object.freeze({ play, pause, stop, render, getState: () => ({ ...state, audio: undefined }) });
    emit('stegmusic_loudness_harmony_ready', 'Loudness normalization and harmonic complexity enhancement is ready.', {
      compressor_available: typeof OfflineAudioContext !== 'undefined' || typeof webkitOfflineAudioContext !== 'undefined',
      target_peak: 0.94,
      html_audio_volume: 1
    }, { double_attenuation_removed: true, harmony_enabled: true });
  }

  initialize();
})();
