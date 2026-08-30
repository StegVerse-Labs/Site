"use strict";

(function (root) {
  var TARGET_URL = "/stegos-node/sv-dn1-browser-evidence-intr-target.json";
  var TARGET_SCHEMA = "stegos.site.sv_dn1_browser_evidence_intr_target.v1";
  var TRANSPORT_SCHEMA = "stegverse.sv-dn1.browser-observation-transport/v1";
  var INTERLOCK_SCHEMA = "stegverse.sv-dn1.browser-observation-interlock-receipt/v1";
  var RECEIPT_SCHEMA = "stegverse.sv-dn1.browser-observation-ingress-receipt/v1";
  var PROFILE = "SV-DN1:BrowserObservation";
  var POLICY = "STEGVERSE-UNIVERSAL-INTR-TRANSPORT-001";
  var TRANSPORT_PROFILE = "stegverse.universal-intr.adjacent-hop/v1";
  var ORIGIN = "STEGOS_WEB_BOOTSTRAP_EGRESS";
  var PROFILE_PATH = "/intr/profile";
  var MATERIALIZATION_PATH = "/intr/materialization";
  var UNIVERSAL_PROFILE_SCHEMA = "stegverse.universal-intr-profiled-ingress/v1";
  var HIL_PROFILE_SCHEMA = "stegverse.hil-intr-materialization-ingress-profile/v1";

  function canonical(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) return "[" + value.map(canonical).join(",") + "]";
    return "{" + Object.keys(value).sort().map(function (key) { return JSON.stringify(key) + ":" + canonical(value[key]); }).join(",") + "}";
  }
  function hex(bytes) { return Array.from(bytes, function (v) { return v.toString(16).padStart(2, "0"); }).join(""); }
  function sha256Hex(value) {
    var text = typeof value === "string" ? value : canonical(value);
    return crypto.subtle.digest("SHA-256", new TextEncoder().encode(text)).then(function (digest) { return hex(new Uint8Array(digest)); });
  }
  function sha256Uri(value) { return sha256Hex(value).then(function (digest) { return "sha256:" + digest; }); }
  function require(ok, message) { if (!ok) throw new Error(message); }

  function validateTarget(target) {
    require(target && target.schema === TARGET_SCHEMA, "SV-DN-1 evidence target schema mismatch");
    require(target.transport_origin === ORIGIN, "SV-DN-1 evidence target origin mismatch");
    require(target.credential_authority === "TV/TVC" && target.credential_requirement === "NONE", "SV-DN-1 evidence target credential boundary mismatch");
    require(target.github_token_runtime_authority === "NONE" && target.execution_authority === "NONE" && target.authority_effect === "NONE_DISCOVERY_ONLY", "SV-DN-1 evidence target authority mismatch");
    if (target.state === "AWAITING_SOVEREIGN_INTR_INGRESS") {
      require(target.ingress_url === null && target.runtime_ingress_observed === false, "Unavailable SV-DN-1 target may not expose runtime locator");
      return target;
    }
    require(target.state === "CONFORMING_SOVEREIGN_INTR_INGRESS" && target.runtime_ingress_observed === true, "SV-DN-1 evidence target state invalid");
    var parsed = new URL(String(target.ingress_url || ""), location.href);
    require(parsed.protocol === "https:" && !parsed.username && !parsed.password && !parsed.search && !parsed.hash && parsed.pathname.endsWith("/intr/materialization"), "SV-DN-1 evidence ingress must be exact credentialless HTTPS");
    return Object.assign({}, target, { ingress_url: parsed.href });
  }

  function validateLiveProfile(profile, responseUrl) {
    require(profile && (profile.schema === UNIVERSAL_PROFILE_SCHEMA || profile.schema === HIL_PROFILE_SCHEMA), "SV-DN-1 live ingress profile schema invalid");
    var observed = new URL(String(responseUrl || ""), location.href);
    require(location.protocol === "https:" && observed.protocol === "https:", "SV-DN-1 live ingress observation requires HTTPS");
    require(observed.origin === location.origin, "SV-DN-1 live ingress profile must be same-origin");
    require(!observed.username && !observed.password && !observed.search && !observed.hash && observed.pathname === PROFILE_PATH, "SV-DN-1 live ingress profile URL invalid");

    var common = {
      state: "ACTIVE_SOVEREIGN_INTR_INGRESS",
      protocol: "InTr",
      profile_path: PROFILE_PATH,
      materialization_path: MATERIALIZATION_PATH,
      event_triggered: true,
      second_user_device_required: false,
      g18_required: false,
      tls_enabled: true,
      credential_authority: "TV/TVC",
      github_token_runtime_authority: "NONE",
      execution_authority: "NONE",
      authority_effect: "NONE_DISCOVERY_EVIDENCE_ONLY"
    };
    Object.keys(common).forEach(function (key) {
      require(canonical(profile[key]) === canonical(common[key]), "SV-DN-1 live ingress profile mismatch: " + key);
    });

    var origins = profile.supported_origins;
    require(Array.isArray(origins) && origins.indexOf(ORIGIN) >= 0, "SV-DN-1 live ingress does not support web-bootstrap egress");

    if (profile.schema === UNIVERSAL_PROFILE_SCHEMA) {
      require(profile.always_on_application_receiver_required === false, "SV-DN-1 live ingress may not require always-on receiver");
      require(Array.isArray(profile.profiles) && profile.profiles.indexOf(PROFILE) >= 0, "SV-DN-1 live ingress profile not advertised");
    } else {
      require(profile.always_on_receiver_required === false, "SV-DN-1 live ingress may not require always-on receiver");
      require(profile.direct_node_credential_requirement === "NONE", "SV-DN-1 live ingress direct credential requirement invalid");
      require(profile.direct_node_tvc_authorization_required === false, "SV-DN-1 live ingress direct TVC authorization requirement invalid");
      require(profile.exact_request_validation_required === true && profile.write_once_queue_admission === true, "SV-DN-1 live ingress exact/write-once contract missing");
      require(Array.isArray(profile.additional_materialization_profiles) && profile.additional_materialization_profiles.indexOf(PROFILE) >= 0, "SV-DN-1 live ingress profile not advertised");
    }

    return validateTarget({
      schema: TARGET_SCHEMA,
      state: "CONFORMING_SOVEREIGN_INTR_INGRESS",
      ingress_url: new URL(MATERIALIZATION_PATH, location.origin).href,
      transport_origin: ORIGIN,
      runtime_ingress_observed: true,
      configuration_authority: "LIVE_SAME_ORIGIN_INTR_PROFILE_OBSERVATION",
      credential_authority: "TV/TVC",
      credential_requirement: "NONE",
      github_token_runtime_authority: "NONE",
      execution_authority: "NONE",
      authority_effect: "NONE_DISCOVERY_ONLY",
      source_profile_url: observed.href,
      source_profile_schema: profile.schema,
      sv_dn1_browser_observation_profile_observed: true
    });
  }

  function discoverLiveTarget() {
    return fetch(PROFILE_PATH, {
      method: "GET",
      cache: "no-store",
      credentials: "omit",
      headers: { Accept: "application/json" }
    }).then(function (response) {
      if (response.status !== 200) throw new Error("SV-DN-1 live ingress profile unavailable: HTTP " + response.status);
      var responseUrl = response.url;
      return response.json().then(function (profile) { return validateLiveProfile(profile, responseUrl); });
    });
  }

  function loadStaticTarget() {
    return fetch(TARGET_URL, { method: "GET", cache: "no-store", credentials: "omit", headers: { Accept: "application/json" } })
      .then(function (response) { if (!response.ok) throw new Error("SV-DN-1 evidence target unavailable: HTTP " + response.status); return response.json(); })
      .then(validateTarget);
  }

  function loadTarget() {
    return loadStaticTarget().then(function (target) {
      if (target.state === "CONFORMING_SOVEREIGN_INTR_INGRESS") return target;
      return discoverLiveTarget().catch(function () { return target; });
    }).catch(function () {
      return discoverLiveTarget();
    });
  }

  function validateBundle(bundle) {
    require(bundle && bundle.schema === "stegverse.sv-dn1.browser-resident-observation-bundle/v3", "SV-DN-1 browser bundle schema mismatch");
    require(bundle.state === "OBSERVED" && bundle.observation_class === "AUTHENTIC_ESTABLISHED_STEGVERSE_WEB_NODE", "SV-DN-1 browser bundle is not authentic observed evidence");
    var reg = bundle.node_registration || {};
    require(/^stegnode-web-/.test(String(reg.node_id || "")), "existing web-bootstrap node id required");
    require(/^stegdevice-/.test(String(reg.device_continuity_id || "")), "existing web-bootstrap device continuity id required");
    require(reg.state === "ESTABLISHED" && reg.credential_authority === "TV/TVC", "existing web-bootstrap registration invalid");
    var replay = bundle.journal_replay || {};
    require(replay.state === "PASS" && /^[a-f0-9]{64}$/.test(String(replay.tail_sha256 || "")), "SV-DN-1 browser journal replay/tail invalid");
    return bundle;
  }

  function buildTransport(bundle) {
    validateBundle(bundle);
    var reg = bundle.node_registration;
    var tail = bundle.journal_replay.tail_sha256;
    return sha256Uri(bundle).then(function (bundleSha) {
      var materializationId = "INTR-MAT-" + bundleSha.slice(7, 31);
      var interlock = {
        schema: INTERLOCK_SCHEMA,
        role: "SOURCE_EGRESS_INTERLOCK",
        materialization_id: materializationId,
        profile_id: "SV-DN-1",
        node_id: reg.node_id,
        device_continuity_id: reg.device_continuity_id,
        bundle_sha256: bundleSha,
        journal_tail_sha256: "sha256:" + tail,
        prior_receipt_hash: "sha256:" + tail,
        boundary_from: "DEVICE_SYSTEM",
        boundary_to: "STEGOS_ECOSYSTEM",
        transport_profile: TRANSPORT_PROFILE,
        universal_intr_policy_id: POLICY,
        credential_authority: "TV/TVC",
        credential_used: false,
        authority_effect: "NONE"
      };
      return sha256Uri(interlock).then(function (interlockHash) {
        interlock.receipt_hash = interlockHash;
        return {
          schema: TRANSPORT_SCHEMA,
          profile: PROFILE,
          profile_id: "SV-DN-1",
          materialization_id: materializationId,
          bundle_sha256: bundleSha,
          node_id: reg.node_id,
          device_continuity_id: reg.device_continuity_id,
          universal_intr_policy_id: POLICY,
          transport_profile: TRANSPORT_PROFILE,
          boundary_from: "DEVICE_SYSTEM",
          boundary_to: "STEGOS_ECOSYSTEM",
          source_interlock_receipt: interlock,
          previous_receipt_hash: interlockHash,
          bundle: bundle,
          request_grants_execution_authority: false,
          claim_or_fence_minted: false,
          credential_authority: "TV/TVC",
          credential_used: false,
          github_token_runtime_authority: "NONE",
          sdk_admitted: false,
          governance_decision_made: false,
          repository_writeback_performed: false,
          deployment_performed: false,
          publication_decision_made: false,
          certification_claimed: false,
          authority_effect: "NONE_TRANSPORT_ONLY"
        };
      });
    });
  }

  function validateIngressReceipt(receipt, transport, payloadSha) {
    require(receipt && receipt.schema === RECEIPT_SCHEMA && receipt.state === "INGRESS_ADMITTED", "SV-DN-1 evidence ingress receipt invalid");
    var expected = {
      profile: PROFILE,
      profile_id: "SV-DN-1",
      materialization_id: transport.materialization_id,
      bundle_sha256: transport.bundle_sha256,
      node_id: transport.node_id,
      device_continuity_id: transport.device_continuity_id,
      source_interlock_receipt_hash: transport.source_interlock_receipt.receipt_hash,
      previous_receipt_hash: transport.source_interlock_receipt.receipt_hash,
      transport_payload_sha256: payloadSha,
      universal_intr_policy_id: POLICY,
      transport_profile: TRANSPORT_PROFILE,
      boundary_from: "DEVICE_SYSTEM",
      boundary_to: "STEGOS_ECOSYSTEM",
      exact_bundle_validated: true,
      journal_replay_validated: true,
      source_interlock_validated: true,
      destination_validation: "PASS",
      lineage_verified: true,
      write_once_persisted: true,
      locator_persisted: true,
      request_grants_execution_authority: false,
      claim_or_fence_minted: false,
      sdk_admitted: false,
      governance_decision_made: false,
      repository_writeback_performed: false,
      deployment_performed: false,
      publication_decision_made: false,
      certification_claimed: false,
      credential_authority: "TV/TVC",
      credential_used: false,
      github_token_runtime_authority: "NONE",
      authority_effect: "NONE_INGRESS_ONLY"
    };
    Object.keys(expected).forEach(function (key) {
      require(canonical(receipt[key]) === canonical(expected[key]), "SV-DN-1 evidence ingress binding mismatch: " + key);
    });
    return receipt;
  }

  function send(bundle) {
    return Promise.all([loadTarget(), buildTransport(bundle)]).then(function (values) {
      var target = values[0], transport = values[1];
      if (target.state !== "CONFORMING_SOVEREIGN_INTR_INGRESS") {
        return { state: "AWAITING_SOVEREIGN_INTR_INGRESS", materialization_id: transport.materialization_id, bundle_sha256: transport.bundle_sha256, authority_effect: "NONE" };
      }
      var text = canonical(transport);
      return sha256Hex(text).then(function (payloadSha) {
        return fetch(target.ingress_url, {
          method: "POST", mode: "cors", cache: "no-store", credentials: "omit",
          headers: {
            "Content-Type": "application/json",
            "X-StegVerse-Transport": "InTr",
            "X-StegVerse-Transport-Origin": ORIGIN,
            "X-StegVerse-Payload-SHA256": payloadSha
          },
          body: text
        }).then(function (response) {
          if (response.status !== 202) throw new Error("SV-DN-1 evidence ingress rejected transport: HTTP " + response.status);
          return response.json();
        }).then(function (receipt) { return validateIngressReceipt(receipt, transport, payloadSha); });
      });
    });
  }

  root.StegVerseSVDN1BrowserEvidenceInTrEgress = Object.freeze({
    validateTarget: validateTarget,
    validateLiveProfile: validateLiveProfile,
    discoverLiveTarget: discoverLiveTarget,
    validateBundle: validateBundle,
    buildTransport: buildTransport,
    validateIngressReceipt: validateIngressReceipt,
    send: send,
    authority_effect: "NONE"
  });
}(globalThis));
