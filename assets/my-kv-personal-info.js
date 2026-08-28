(function (root, factory) {
  "use strict";
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.StegVerseMyKVPersonalInfo = api;
}(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  var PROFILE_SCHEMA = "stegverse.kv.personal-contact-profile/v1";
  var CONNECTION_STATES = [
    "UNMAPPED",
    "MAPPED_CREDENTIAL_REQUIRED",
    "CREDENTIAL_BOUND",
    "SESSION_VERIFIED",
    "REVOKED"
  ];
  var FORBIDDEN_KEYS = [
    "password", "secret", "token", "access_token", "refresh_token",
    "app_password", "credential", "credential_value", "private_key",
    "seed", "mnemonic"
  ];

  function clone(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function normalizeEmail(value) {
    var address = String(value || "").trim().toLowerCase();
    var at = address.lastIndexOf("@");
    if (at <= 0 || at === address.length - 1) throw new Error("Valid email address required");
    var local = address.slice(0, at);
    var domain = address.slice(at + 1);
    if (!local || domain.indexOf(".") <= 0 || domain.endsWith(".")) {
      throw new Error("Valid routable email address required");
    }
    return address;
  }

  function newProfile() {
    return {
      schema: PROFILE_SCHEMA,
      email_addresses: [],
      authority_effect: "NONE"
    };
  }

  function assertNoForbiddenKeys(value, path) {
    path = path || "profile";
    if (Array.isArray(value)) {
      value.forEach(function (item, index) {
        assertNoForbiddenKeys(item, path + "[" + index + "]");
      });
      return;
    }
    if (!value || typeof value !== "object") return;
    Object.keys(value).forEach(function (key) {
      var lower = key.toLowerCase();
      if (FORBIDDEN_KEYS.some(function (token) { return lower.indexOf(token) !== -1; })) {
        throw new Error("Secret-bearing field prohibited at " + path + "." + key);
      }
      assertNoForbiddenKeys(value[key], path + "." + key);
    });
  }

  function validateProfile(profile) {
    var errors = [];
    if (!profile || typeof profile !== "object") return ["Profile must be an object"];
    try { assertNoForbiddenKeys(profile); } catch (error) { errors.push(error.message); }
    if (profile.schema !== PROFILE_SCHEMA) errors.push("Profile schema mismatch");
    if (profile.authority_effect !== "NONE") errors.push("Profile may not grant authority");
    if (!Array.isArray(profile.email_addresses)) return errors.concat(["email_addresses must be an array"]);

    var seen = Object.create(null);
    var primaries = 0;
    profile.email_addresses.forEach(function (entry, index) {
      var prefix = "email_addresses[" + index + "]";
      var address;
      try { address = normalizeEmail(entry.address); } catch (error) {
        errors.push(prefix + ": " + error.message);
        return;
      }
      if (seen[address]) errors.push(prefix + ": duplicate email address");
      seen[address] = true;
      if (typeof entry.label !== "string" || !entry.label.trim()) errors.push(prefix + ": label required");
      if (entry.primary === true) primaries += 1;
      else if (entry.primary !== false) errors.push(prefix + ": primary must be boolean");
      if (entry.email_continuity_enabled !== true && entry.email_continuity_enabled !== false) {
        errors.push(prefix + ": email_continuity_enabled must be boolean");
      }
      if (CONNECTION_STATES.indexOf(entry.connection_state) === -1) errors.push(prefix + ": invalid connection state");
      if (entry.connection_state === "UNMAPPED") {
        if (entry.mapping_id !== null) errors.push(prefix + ": unmapped email may not have mapping_id");
      } else {
        if (typeof entry.mapping_id !== "string" || !/^kv-email:[a-f0-9]{64}$/.test(entry.mapping_id)) {
          errors.push(prefix + ": mapped email requires canonical mapping_id");
        }
        if (entry.email_continuity_enabled !== true) errors.push(prefix + ": mapped email must enable continuity");
      }
    });
    if (primaries > 1) errors.push("At most one primary email address is allowed");
    return errors;
  }

  function assertValid(profile) {
    var errors = validateProfile(profile);
    if (errors.length) throw new Error(errors.join("; "));
    return profile;
  }

  function addEmail(profile, input) {
    var updated = clone(profile);
    var address = normalizeEmail(input.address);
    if (updated.email_addresses.some(function (entry) {
      return normalizeEmail(entry.address) === address;
    })) throw new Error("Email address already exists");

    if (input.primary === true) {
      updated.email_addresses.forEach(function (entry) { entry.primary = false; });
    }
    updated.email_addresses.push({
      address: address,
      label: String(input.label || "personal").trim() || "personal",
      primary: input.primary === true,
      email_continuity_enabled: false,
      mapping_id: null,
      connection_state: "UNMAPPED"
    });
    return assertValid(updated);
  }

  function removeEmail(profile, address) {
    var normalized = normalizeEmail(address);
    var updated = clone(profile);
    updated.email_addresses = updated.email_addresses.filter(function (entry) {
      return normalizeEmail(entry.address) !== normalized;
    });
    return assertValid(updated);
  }

  function setPrimary(profile, address) {
    var normalized = normalizeEmail(address);
    var updated = clone(profile);
    var found = false;
    updated.email_addresses.forEach(function (entry) {
      var match = normalizeEmail(entry.address) === normalized;
      entry.primary = match;
      found = found || match;
    });
    if (!found) throw new Error("Email address not found");
    return assertValid(updated);
  }

  function applyMapping(profile, address, mapping) {
    var normalized = normalizeEmail(address);
    if (!mapping || typeof mapping !== "object") throw new Error("Canonical mapping result required");
    if (mapping.email_address && normalizeEmail(mapping.email_address) !== normalized) {
      throw new Error("Mapping/email binding mismatch");
    }
    if (!/^kv-email:[a-f0-9]{64}$/.test(String(mapping.mapping_id || ""))) {
      throw new Error("Canonical mapping_id required");
    }
    if (mapping.mapping_state !== "MAPPED_CREDENTIAL_REQUIRED") {
      throw new Error("Initial Site mapping may only enter MAPPED_CREDENTIAL_REQUIRED");
    }
    var updated = clone(profile);
    var found = false;
    updated.email_addresses.forEach(function (entry) {
      if (normalizeEmail(entry.address) === normalized) {
        found = true;
        entry.email_continuity_enabled = true;
        entry.mapping_id = mapping.mapping_id;
        entry.connection_state = mapping.mapping_state;
      }
    });
    if (!found) throw new Error("Email address not found");
    return assertValid(updated);
  }

  function connectionGuidance(entry) {
    switch (entry.connection_state) {
      case "MAPPED_CREDENTIAL_REQUIRED":
        return {
          action: "COMPLETE_SKAP_CREDENTIAL_SETUP",
          message: "Complete setup in SKAP Vault to activate this email connection."
        };
      case "CREDENTIAL_BOUND":
        return {
          action: "VERIFY_PROVIDER_SESSION",
          message: "Credential reference is bound. Verify the provider session through the canonical KV bridge."
        };
      case "SESSION_VERIFIED":
        return {
          action: "GOVERNED_INGRESS_PENDING_OR_AVAILABLE",
          message: "Provider session is verified. Governed ingress remains subject to KV/Interlock admission."
        };
      case "REVOKED":
        return {
          action: "REAUTHORIZE_MAPPING",
          message: "This mapping is revoked. Start a new owner-authorized connection flow."
        };
      default:
        return {
          action: "OPTIONAL_CONNECT",
          message: "Stored as personal information only. Mailbox access is not enabled."
        };
    }
  }

  function connectEmail(profile, address, bridge) {
    var normalized = normalizeEmail(address);
    if (!bridge || typeof bridge.mapEmail !== "function") {
      return Promise.reject(new Error("FAIL_CLOSED: canonical KV email mapping bridge unavailable; no connection state changed"));
    }
    var entry = profile.email_addresses.find(function (candidate) {
      return normalizeEmail(candidate.address) === normalized;
    });
    if (!entry) return Promise.reject(new Error("Email address not found"));
    if (entry.connection_state !== "UNMAPPED") {
      return Promise.reject(new Error("Email address is already mapped or revoked"));
    }
    return Promise.resolve(bridge.mapEmail({
      schema: "stegverse.site.my-kv.email-map-request/v1",
      address: normalized,
      label: entry.label,
      primary: entry.primary,
      requested_capability: "email-continuity",
      credential_destination: "SKAP_VAULT",
      authority_effect: "NONE"
    })).then(function (mapping) {
      assertNoForbiddenKeys(mapping, "mapping");
      return applyMapping(profile, normalized, mapping);
    });
  }

  function persistProfile(profile, bridge) {
    assertValid(profile);
    if (!bridge || typeof bridge.saveProfile !== "function") {
      return Promise.resolve({
        persisted: false,
        state: "DRAFT_ONLY",
        message: "Connected KV profile bridge unavailable; changes remain on this page only."
      });
    }
    return Promise.resolve(bridge.saveProfile(clone(profile))).then(function (result) {
      if (!result || result.persisted !== true) throw new Error("FAIL_CLOSED: KV profile persistence was not confirmed");
      return { persisted: true, state: "KV_PERSISTED", message: "Personal information saved to KnowledgeVault." };
    });
  }

  function loadProfile(bridge) {
    if (!bridge || typeof bridge.loadProfile !== "function") {
      return Promise.resolve({ profile: newProfile(), state: "DRAFT_ONLY" });
    }
    return Promise.resolve(bridge.loadProfile()).then(function (profile) {
      assertValid(profile);
      return { profile: clone(profile), state: "KV_LOADED" };
    });
  }

  return {
    PROFILE_SCHEMA: PROFILE_SCHEMA,
    CONNECTION_STATES: CONNECTION_STATES.slice(),
    newProfile: newProfile,
    normalizeEmail: normalizeEmail,
    validateProfile: validateProfile,
    addEmail: addEmail,
    removeEmail: removeEmail,
    setPrimary: setPrimary,
    applyMapping: applyMapping,
    connectionGuidance: connectionGuidance,
    connectEmail: connectEmail,
    persistProfile: persistProfile,
    loadProfile: loadProfile,
    assertNoForbiddenKeys: assertNoForbiddenKeys
  };
}));
