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
        policy_refs: ['stegmusic-rights-boundary-v0', 'stegmusic-loudness-harmony-v0', 'stegmusic-arrangement-arc-v0']
      }
    }
  }));

  const state = { audio: null, objectUrl: null, trackId: null, playing: false, rendering: false, resumeAfterSelection: false };
  const chordProgressions = [
    [[0, 3, 7], [5, 8, 12], [3, 7, 10], [7, 10, 14]],
    [[0, 4, 7], [7, 11, 14], [9, 12, 16], [5, 9, 12]],
    [[0, 3, 7, 10], [5, 8, 12, 15], [7, 10, 14, 17], [3, 7, 10, 14]]
  ];
  const arrangementPhases = Object.freeze([
    { id: 'intro', bars: 4, density: 0.48, leadOctave: 0, bassPulse: 2 },
    { id: 'build', bars: 4, density: 0.72, leadOctave: 0, bassPulse: 1 },
    { id: 'peak', bars: 4, density: 1.0, leadOctave: 12, bassPulse: 1 },
    { id: 'breakdown', bars: 4, density: 0.38, leadOctave: -12, bassPulse: 2 },
    { id: 'return', bars: 4, density: 0.86, leadOctave: 0, bassPulse: 1 }
  ]);

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
      setNotice('AUDIO · long-form normalized harmonic mix playing');
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
    setNotice(`AUDIO · building long-form harmonic mix for “${track.title}”`);
    try {
      const c = controls();
      const OfflineCtor = window.OfflineAudioContext || window.webkitOfflineAudioContext;
      if (!OfflineCtor) throw new Error('Offline audio rendering is unavailable.');
      const sampleRate = 44100;
      const beat = 60 / track.bpm;
      const totalBars = arrangementPhases.reduce((sum, phase) => sum + phase.bars, 0);
      const duration = totalBars * beat * 4 + 2;
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
      let barOffset = 0;
      arrangementPhases.forEach((phase, phaseIndex) => {
        for (let localBar = 0; localBar < phase.bars; localBar += 1) {
          const bar = barOffset + localBar;
          const chordIndex = (bar + (phaseIndex >= 2 ? phaseIndex : 0)) % progression.length;
          const chord = progression[chordIndex];
          const chordStart = bar * beat * 4;
          const padLevel = (0.045 + c.energy / 5600) * phase.density;
          chord.forEach((interval, index) => {
            const inversion = phase.id === 'return' && localBar >= 2 && index === 0 ? 12 : 0;
            voice(ctx, mix, midiToHz(track.root + interval + inversion), chordStart, beat * 3.88, index % 2 ? 'triangle' : 'sine', padLevel, 780 + c.brightness * 27, (index - 1.5) * 0.28, phase.id === 'intro' ? 0.22 : 0.1);
          });
          const bassRoot = track.root - 24 + chord[0];
          voice(ctx, mix, midiToHz(bassRoot), chordStart, beat * 3.9, 'sine', (0.13 + c.bass / 900) * Math.max(0.62, phase.density), 145 + c.bass * 5.5, 0, 0.035);
          voice(ctx, mix, midiToHz(bassRoot + 12), chordStart + beat * 2, beat * 1.85, 'triangle', (0.035 + c.bass / 4200) * phase.density, 260 + c.bass * 6, phaseIndex % 2 ? 0.08 : -0.08, 0.02);
          for (let pulse = phase.bassPulse; pulse < 4; pulse += phase.bassPulse) {
            voice(ctx, mix, midiToHz(bassRoot + (pulse === 3 && complexity >= 6 ? 7 : 0)), chordStart + beat * pulse, beat * 0.82, 'sine', (0.07 + c.bass / 1800) * phase.density, 180 + c.bass * 5, 0, 0.012);
          }
        }
        barOffset += phase.bars;
      });

      const totalSteps = totalBars * 8;
      for (let step = 0; step < totalSteps; step += 1) {
        const time = step * beat / 2;
        const bar = Math.floor(step / 8);
        let traversed = 0;
        const phase = arrangementPhases.find(candidate => {
          traversed += candidate.bars;
          return bar < traversed;
        }) || arrangementPhases[arrangementPhases.length - 1];
        const phaseDensity = phase.density;
        let note = track.root + track.pattern[step % track.pattern.length] + phase.leadOctave;
        if (phase.id === 'peak' && step % 16 === 12) note += 7;
        if (phase.id === 'return' && step % 16 >= 12) note += 5;
        if (c.exploration > 65 && step % 16 === 12) note += 12;
        const leadType = c.brightness > 60 ? 'sawtooth' : c.brightness > 35 ? 'triangle' : 'sine';
        const leadActive = phase.id !== 'breakdown' || step % 4 === 0;
        if (leadActive) voice(ctx, mix, midiToHz(note), time, beat * (phase.id === 'intro' ? 0.7 : 0.42), leadType, (0.065 + c.energy / 1900) * phaseDensity, 650 + c.brightness * 42, step % 2 ? 0.2 : -0.2);
        if (complexity >= 4 && step % 2 === 1 && phase.id !== 'intro') voice(ctx, mix, midiToHz(note - 12 + (step % 8 === 7 ? 5 : 0)), time + beat * 0.08, beat * 0.34, 'triangle', 0.034 * phaseDensity, 900 + c.brightness * 20, step % 4 === 1 ? -0.44 : 0.44);
        if (complexity >= 6 && step % 4 === 2 && (phase.id === 'peak' || phase.id === 'return')) voice(ctx, mix, midiToHz(note + 7), time + beat * 0.16, beat * 0.24, 'sine', 0.026 * phaseDensity, 1650, 0.58);
        if (step % 4 === 0 && phase.id !== 'breakdown') voice(ctx, mix, 50 + c.energy / 7, time, 0.18, 'sine', 0.18 * phaseDensity, 130, 0);
        if (step % 2 === 0 && complexity >= 3 && phase.id !== 'intro') percussion(ctx, mix, time + beat * 0.25, (0.042 + c.energy / 5200) * phaseDensity, c.brightness);
        if (complexity >= 7 && step % 8 === 7 && phase.id === 'peak') percussion(ctx, mix, time + beat * 0.37, 0.03, c.brightness + 20);
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
      emit('generated_harmonic_mix_rendered', `Rendered long-form louder harmonic StegDJ mix “${track.title}”.`, {
        track_id: track.id,
        title: track.title,
        duration_seconds: duration,
        total_bars: totalBars,
        arrangement_phases: arrangementPhases.map(phase => phase.id),
        bytes: blob.size,
        compressor: { threshold_db: -20, knee_db: 18, ratio: 4.5, attack_seconds: 0.008, release_seconds: 0.18 },
        output_gain: 1.28,
        peak_before_normalization: normalized.peakBefore,
        normalization_gain: normalized.normalizationGain,
        normalized_target_peak: normalized.targetPeak,
        harmony_voice_count: progression[0].length,
        complexity_level: complexity,
        sustained_sub_bass: true,
        harmonic_bass_pulses: true,
        html_audio_volume: 1,
        controls: c,
        source_bytes_uploaded: false
      }, {
        perceived_loudness_strategy: 'compression_output_gain_peak_normalization',
        harmony_strategy: 'progressive_chord_pad_bass_countermelody',
        arrangement_strategy: 'intro_build_peak_breakdown_return',
        bass_strategy: 'sustained_sub_bass_plus_harmonic_pulses',
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
      emit('enhanced_media_playback_started', `Playing long-form louder harmonic mix “${track.title}”.`, {
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
    emit('stegmusic_loudness_harmony_ready', 'Long-form loudness, bass continuity, and harmonic complexity enhancement is ready.', {
      compressor_available: typeof OfflineAudioContext !== 'undefined' || typeof webkitOfflineAudioContext !== 'undefined',
      target_peak: 0.94,
      arrangement_phases: arrangementPhases.map(phase => phase.id),
      html_audio_volume: 1
    }, { double_attenuation_removed: true, harmony_enabled: true, long_form_arrangement_enabled: true, sustained_bass_enabled: true });
  }

  initialize();
})();
