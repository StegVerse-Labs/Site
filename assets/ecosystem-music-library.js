(() => {
  'use strict';
  const MANIFEST_URL='data/stegmusic-library.json';
  const FAVORITES_KEY='stegmusic.library.favorites.v1';
  const $=id=>document.getElementById(id);
  const esc=v=>String(v).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
  const emit=(type,human,governed)=>window.dispatchEvent(new CustomEvent('stegmusic:emit',{detail:{type,human,governed}}));
  let manifest=null,query='',collection='all',playableOnly=false,favoritesOnly=false;
  let favorites=new Set();
  try{const parsed=JSON.parse(localStorage.getItem(FAVORITES_KEY)||'[]');favorites=new Set(Array.isArray(parsed)?parsed:[]);}catch(_){favorites=new Set();}
  const persist=()=>localStorage.setItem(FAVORITES_KEY,JSON.stringify([...favorites].sort()));
  const visible=()=>manifest.tracks.filter(t=>{
    if(collection!=='all'&&!t.collection_ids.includes(collection))return false;
    if(playableOnly&&!t.playable)return false;
    if(favoritesOnly&&!favorites.has(t.id))return false;
    if(!query.trim())return true;
    return [t.title,t.artist,...t.genres,...t.moods,...t.tags].join(' ').toLowerCase().includes(query.trim().toLowerCase());
  });
  function select(track){
    if(!track.playable||!Number.isInteger(track.runtime_index)||!window.StegMusicRuntime)return;
    window.StegMusicRuntime.selectGeneratedTrack(track.runtime_index,{reason:'library_selection',details:{library_id:manifest.library_id,collection_ids:track.collection_ids}});
    emit('music_library_track_selected',`Selected “${track.title}” from the StegMusic library.`,{rights_status:track.rights_status,source_class:'governed_music_library',captured_records:[{track_id:track.id,runtime_index:track.runtime_index}],derived_records:[{playable:true,authority:'none'}],contribution_eligibility:'not_evaluated',royalty_state:'not_realized',artifact_refs:[track.id],policy_refs:['stegmusic-library-v1','governed-service-envelope-v0']});
  }
  function favorite(track){
    const added=!favorites.has(track.id);if(added)favorites.add(track.id);else favorites.delete(track.id);persist();
    emit('music_library_favorite_changed',`${added?'Added':'Removed'} “${track.title}” ${added?'to':'from'} local favorites.`,{rights_status:'not_applicable',source_class:'browser_local_library_preference',captured_records:[{track_id:track.id,favorite:added}],derived_records:[{profile_scoped:true,cross_profile_read:false,authority:'none'}],contribution_eligibility:'candidate',royalty_state:'not_realized',policy_refs:['stegmusic-library-v1']});render();
  }
  function card(t){const fav=favorites.has(t.id);return `<article class="track"><div><strong>${esc(t.title)}</strong><span>${esc(t.artist)} · ${esc(t.genres.join(' / '))} · ${t.bpm} BPM</span><span>${esc(t.moods.join(' · '))}</span><span class="license">${t.playable?'PLAYABLE NOW':'GENERATION PROFILE'} · ${esc(t.rights_status)}</span></div><div class="player-actions">${t.playable?`<button class="sv-btn sv-btn-primary" data-lib-play="${esc(t.id)}">Select</button>`:'<span class="status pending">NOT YET RENDERED</span>'}<button class="sv-btn sv-btn-secondary" data-lib-fav="${esc(t.id)}" aria-pressed="${fav}">${fav?'★ Favorited':'☆ Favorite'}</button></div></article>`;}
  function render(){const target=$('stegmusicLibraryResults');if(!target||!manifest)return;const tracks=visible();$('stegmusicLibraryCount').textContent=`${tracks.length} of ${manifest.tracks.length} entries · ${manifest.tracks.filter(t=>t.playable).length} playable`;target.innerHTML=tracks.map(card).join('')||'<p class="muted">No library entries match these filters.</p>';target.querySelectorAll('[data-lib-play]').forEach(b=>b.onclick=()=>select(manifest.tracks.find(t=>t.id===b.dataset.libPlay)));target.querySelectorAll('[data-lib-fav]').forEach(b=>b.onclick=()=>favorite(manifest.tracks.find(t=>t.id===b.dataset.libFav)));}
  function install(){if($('stegmusicLibrary'))return;const anchor=document.querySelector('section[aria-labelledby="catalog-heading"]');if(!anchor)return;const section=document.createElement('section');section.className='card';section.id='stegmusicLibrary';section.innerHTML=`<h2 class="sv-h2">StegMusic library</h2><p class="muted">Versioned catalog, collections, local favorites, provenance, and rights posture. Profiles are indexed without being represented as rendered audio.</p><div class="search-row"><input class="field" id="stegmusicLibrarySearch" placeholder="Title, mood, genre, tag"><select class="field" id="stegmusicLibraryCollection"><option value="all">All collections</option>${manifest.collections.map(c=>`<option value="${esc(c.id)}">${esc(c.title)}</option>`).join('')}</select><label><input id="stegmusicLibraryPlayable" type="checkbox"> Playable now</label><button class="sv-btn sv-btn-secondary" id="stegmusicLibraryFavorites">Favorites only</button></div><div class="audio-notice" id="stegmusicLibraryCount"></div><div class="catalog" id="stegmusicLibraryResults"></div><p class="muted">Authority: none. Indexing does not establish ownership, licensing, custody, publication authority, or payable royalties.</p>`;anchor.insertAdjacentElement('afterend',section);$('stegmusicLibrarySearch').oninput=e=>{query=e.target.value;render();};$('stegmusicLibraryCollection').onchange=e=>{collection=e.target.value;render();};$('stegmusicLibraryPlayable').onchange=e=>{playableOnly=e.target.checked;render();};$('stegmusicLibraryFavorites').onclick=e=>{favoritesOnly=!favoritesOnly;e.currentTarget.textContent=favoritesOnly?'Showing favorites':'Favorites only';render();};render();}
  async function load(){const response=await fetch(MANIFEST_URL,{cache:'no-store'});if(!response.ok)throw new Error(`library manifest HTTP ${response.status}`);manifest=await response.json();install();emit('music_library_loaded',`Loaded ${manifest.tracks.length} governed StegMusic library entries.`,{rights_status:'mixed_manifest_declared',source_class:'governed_music_library',captured_records:[{library_id:manifest.library_id,track_count:manifest.tracks.length,collection_count:manifest.collections.length}],derived_records:[{playable_count:manifest.tracks.filter(t=>t.playable).length,generation_profile_count:manifest.tracks.filter(t=>!t.playable).length,authority:'none'}],contribution_eligibility:'not_evaluated',royalty_state:'not_realized',policy_refs:['stegmusic-library-v1']});}
  window.StegMusicLibrary=Object.freeze({load,manifest_url:MANIFEST_URL,favorites_key:FAVORITES_KEY,authority:'none'});load().catch(error=>console.error('StegMusic library failed to load',error));
})();
