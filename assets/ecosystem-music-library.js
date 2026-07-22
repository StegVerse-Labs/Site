(() => {
  'use strict';

  const MANIFEST_URL = 'data/stegmusic-library.json';
  const FAVORITES_KEY = 'stegmusic.library.favorites.v1';
  const $ = id => document.getElementById(id);
  const escapeHtml = value => String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
  const emit = (type, human, governed) => window.dispatchEvent(new CustomEvent('stegmusic:emit', {detail:{type,human,governed}}));
  const parseFavorites = () => {
    try {
      const parsed = JSON.parse(localStorage.getItem(FAVORITES_KEY) || '[]');
      return new Set(Array.isArray(parsed) ? parsed : []);
    } catch (_) {
      return new Set();
    }
  };

  let manifest = null;
  let favorites = parseFavorites();
  let activeCollection = 'all';
  let query = '';
  let playableOnly = false;

  function persistFavorites() {
    localStorage.setItem(FAVORITES_KEY, JSON.stringify([...favorites].sort()));
  }

  function libraryTracks() {
    if (!manifest) return [];
    const q = query.trim().toLowerCase();
    return manifest.tracks.filter(track => {
      if (activeCollection !== 'all' && !track.collection_ids.includes(activeCollection)) return false;
      if (playableOnly && !track.playable) return false;
      if (!q) return true;
      const searchable = [track.title, track.artist, ...track.genres, ...track.moods, ...track.tags].join(' ').toLowerCase();
      return searchable.includes(q);
    });
  }

  function selectTrack(track) {
    if (!track.playable || !Number.isInteger(track.runtime_index) || !window.StegMusicRuntime) return;
    window.StegMusicRuntime.selectGeneratedTrack(track.runtime_index, {
      reason: 'library_selection',
      details: {library_id: manifest.library_id, collection_ids: track.collection_ids}
    });
    emit('music_library_track_selected', `Selected “${track.title}” from the StegMusic library.`, {
      rights_status: track.rights_status,
      source_class: 'governed_music_library',
      captured_records: [{track_id:track.id, library_id:manifest.library_id, runtime_index:track.runtime_index}],
      derived_records: [{playable:true, authority:'none'}],
      contribution_eligibility: 'not_evaluated',
      royalty_state: 'not_realized',
      artifact_refs: [track.id],
      policy_refs: ['stegmusic-library-v1','governed-service-envelope-v0']
    });
  }

  function toggleFavorite(track) {
    const added = !favorites.has(track.id);
    if (added) favorites.add(track.id); else favorites.delete(track.id);
    persistFavorites();
    emit('music_library_favorite_changed', `${added ? 'Added' : 'Removed'} “${track.title}” ${added ? 'to' : 'from'} local favorites.`, {
      rights_status: 'not_applicable',
      source_class: 'browser_local_library_preference',
      captured_records: [{track_id:track.id, favorite:added}],
      derived_records: [{profile_scoped:true, cross_profile_read:false, authority:'none'}],
      contribution_eligibility: 'candidate',
      royalty_state: 'not_realized',
      policy_refs: ['stegmusic-library-v1','cross-service-projection-v0']
    });
    render();
  }

  function trackCard(track) {
    const favorite = favorites.has(track.id);
    const state = track.playable ? 'PLAYABLE NOW' : 'GENERATION PROFILE';
    const action = track.playable
      ? `<button class="sv-btn sv-btn-primary" type="button" data-library-play="${escapeHtml(track.id)}">Select</button>`
      : '<span class="status pending">NOT YET RENDERED</span>';
    return `<article class="track" data-library-track="${escapeHtml(track.id)}"><div><strong>${escapeHtml(track.title)}</strong><span>${escapeHtml(track.artist)} · ${escapeHtml(track.genres.join(' / '))} · ${track.bpm} BPM</span><span>${escapeHtml(track.moods.join(' · '))}</span><span class="license">${state} · ${escapeHtml(track.rights_status)}</span></div><div class="player-actions">${action}<button class="sv-btn sv-btn-secondary" type="button" data-library-favorite="${escapeHtml(track.id)}" aria-pressed="${favorite}">${favorite ? '★ Favorited' : '☆ Favorite'}</button></div></article>`;
  }

  function render() {
    const target = $('stegmusicLibraryResults');
    if (!target || !manifest) return;
    const tracks = libraryTracks();
    $('stegmusicLibraryCount').textContent = `${tracks.length} of ${manifest.tracks.length} library entries · ${manifest.tracks.filter(t => t.playable).length} playable`;
    target.innerHTML = tracks.map(trackCard).join('') || '<p class="muted">No library entries match these filters.</p>';
    target.querySelectorAll('[data-library-play]').forEach(button => button.addEventListener('click', () => selectTrack(manifest.tracks.find(t => t.id === button.dataset.libraryPlay))));
    target.querySelectorAll('[data-library-favorite]').forEach(button => button.addEventListener('click', () => toggleFavorite(manifest.tracks.find(t => t.id === button.dataset.libraryFavorite))));
  }

  function installUi() {
    if ($('stegmusicLibrary')) return;
    const anchor = document.querySelector('section[aria-labelledby="catalog-heading"]');
    if (!anchor) return;
    const section = document.createElement('section');
    section.className = 'card';
    section.id = 'stegmusicLibrary';
    section.setAttribute('aria-labelledby', 'stegmusic-library-heading');
    const collectionOptions = manifest.collections.map(collection => `<option value="${escapeHtml(collection.id)}">${escapeHtml(collection.title)}</option>`).join('');
    section.innerHTML = `<h2 class="sv-h2" id="stegmusic-library-heading">StegMusic library</h2><p class="muted">Versioned generated catalog, collections, local favorites, provenance, and rights posture. Generation profiles are indexed without being represented as rendered audio.</p><div class="search-row"><label class="muted" for="stegmusicLibrarySearch">Search library</label><input class="field" id="stegmusicLibrarySearch" placeholder="Title, mood, genre, tag"><label class="muted" for="stegmusicLibraryCollection">Collection</label><select class="field" id="stegmusicLibraryCollection"><option value="all">All collections</option>${collectionOptions}</select><label><input id="stegmusicLibraryPlayable" type="checkbox"> Playable now</label><button class="sv-btn sv-btn-secondary" type="button" id="stegmusicLibraryFavorites">Favorites only</button></div><div class="audio-notice" id="stegmusicLibraryCount" role="status" aria-live="polite"></div><div class="catalog" id="stegmusicLibraryResults"></div><p class="muted">Library authority: none. Indexing does not establish ownership, licensing, custody, publication authority, or payable royalty entitlement.</p>`;
    anchor.insertAdjacentElement('afterend', section);
    $('stegmusicLibrarySearch').addEventListener('input', event => {query = event.target.value; render();});
    $('stegmusicLibraryCollection').addEventListener('change', event => {activeCollection = event.target.value; render();});
    $('stegmusicLibraryPlayable').addEventListener('change', event => {playableOnly = event.target.checked; render();});
    let favoritesOnly = false;
    $('stegmusicLibraryFavorites').addEventListener('click', event => {
      favoritesOnly = !favoritesOnly;
      event.currentTarget.textContent = favoritesOnly ? 'Showing favorites' : 'Favorites only';
      event.currentTarget.setAttribute('aria-pressed', String(favoritesOnly));
      const original = libraryTracks;
      if (favoritesOnly) {
        const visible = manifest.tracks.filter(track => favorites.has(track.id));
        $('stegmusicLibraryResults').innerHTML = visible.map(trackCard).join('') || '<p class="muted">No local favorites yet.</p>';
        $('stegmusicLibraryCount').textContent = `${visible.length} local favorites`;
        $('stegmusicLibraryResults').querySelectorAll('[data-library-play]').forEach(button => button.addEventListener('click', () => selectTrack(manifest.tracks.find(t => t.id === button.dataset.libraryPlay))));
        $('stegmusicLibraryResults').querySelectorAll('[data-library-favorite]').forEach(button => button.addEventListener('click', () => toggleFavorite(manifest.tracks.find(t => t.id === button.dataset.libraryFavorite))));
      } else {
        void original;
        render();
      }
    });
    render();
  }

  async function load() {
    try {
      const response = await fetch(MANIFEST_URL, {cache:'no-store'});
      if (!response.ok) throw new Error(`library manifest HTTP ${response.status}`);
      manifest = await response.json();
      if (!manifest || !Array.isArray(manifest.tracks) || !Array.isArray(manifest.collections)) throw new Error('library manifest invalid');
      installUi();
      emit('music_library_loaded', `Loaded ${manifest.tracks.length} governed StegMusic library entries.`, {
        rights_status: 'mixed_manifest_declared',
        source_class: 'governed_music_library',
        captured_records: [{library_id:manifest.library_id, schema_version:manifest.schema_version, track_count:manifest.tracks.length, collection_count:manifest.collections.length}],
        derived_records: [{playable_count:manifest.tracks.filter(t => t.playable).length, generation_profile_count:manifest.tracks.filter(t => !t.playable).length, authority:'none'}],
        contribution_eligibility: 'not_evaluated',
        royalty_state: 'not_realized',
        policy_refs: ['stegmusic-library-v1','governed-service-envelope-v0']
      });
    } catch (error) {
      console.error('StegMusic library failed to load', error);
    }
  }

  window.StegMusicLibrary = Object.freeze({load, manifest_url:MANIFEST_URL, favorites_key:FAVORITES_KEY, authority:'none'});
  load();
})();
