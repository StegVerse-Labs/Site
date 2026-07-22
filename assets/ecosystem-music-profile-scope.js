(() => {
  'use strict';

  const ACTIVE_KEY = 'stegmusic.active-profile.v1';
  const REGISTRY_KEY = 'stegmusic.profile-registry.v1';
  const RAW_GET = Storage.prototype.getItem;
  const RAW_SET = Storage.prototype.setItem;
  const RAW_REMOVE = Storage.prototype.removeItem;
  const sanitize = value => String(value || 'default').trim().toLowerCase().replace(/[^a-z0-9_-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 48) || 'default';
  const activeProfileId = sanitize(RAW_GET.call(localStorage, ACTIVE_KEY) || 'default');
  const globalKeys = new Set([ACTIVE_KEY, REGISTRY_KEY]);
  const scopedKey = key => String(key).startsWith('stegmusic.') && !globalKeys.has(String(key)) ? `stegmusic.profile.${activeProfileId}.${key}` : String(key);

  Storage.prototype.getItem = function(key) { return RAW_GET.call(this, this === localStorage ? scopedKey(key) : key); };
  Storage.prototype.setItem = function(key, value) { return RAW_SET.call(this, this === localStorage ? scopedKey(key) : key, value); };
  Storage.prototype.removeItem = function(key) { return RAW_REMOVE.call(this, this === localStorage ? scopedKey(key) : key); };

  function registry() {
    try { return JSON.parse(RAW_GET.call(localStorage, REGISTRY_KEY) || '{}'); }
    catch (_) { return {}; }
  }

  function setActiveProfile(rawId, displayName) {
    const id = sanitize(rawId);
    const entries = registry();
    entries[id] = {id, display_name: String(displayName || id).trim().slice(0, 80), last_selected_at: new Date().toISOString()};
    RAW_SET.call(localStorage, REGISTRY_KEY, JSON.stringify(entries));
    RAW_SET.call(localStorage, ACTIVE_KEY, id);
    window.location.reload();
  }

  function bind() {
    const idInput = document.getElementById('isolatedProfileId');
    const nameInput = document.getElementById('profileName');
    const switchButton = document.getElementById('switchIsolatedProfile');
    const activeLabel = document.getElementById('activeProfileScope');
    if (idInput) idInput.value = activeProfileId;
    if (activeLabel) activeLabel.textContent = `ISOLATED PROFILE · ${activeProfileId}`;
    if (switchButton) switchButton.addEventListener('click', () => setActiveProfile(idInput ? idInput.value : 'default', nameInput ? nameInput.value : activeProfileId));
  }

  window.StegMusicProfileScope = Object.freeze({activeProfileId, scopedKey, setActiveProfile, storage_isolation: 'browser_local_namespace', cross_profile_read: false});
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bind); else bind();
})();
