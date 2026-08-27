"use strict";

(function () {
  var DB_NAME = "stegos-node-v1";
  var DB_VERSION = 1;
  var META = "meta";
  var RECEIPTS = "receipts";
  var REGISTRATION_KEY = "registration";
  var PERSONAL_KV_SYNC_KEY = "personal-kv-sync";
  var NETWORK_SYNC_KEY = "stegos-network-sync";
  var OFFLINE_PROOF_KEY = "offline-reload-proof";
  var KV_READINESS_STATE_KEY = "kv-readiness-device-state";
  var KV_READINESS_SNAPSHOT_URL = "./kv-readiness-snapshot.json";

  var KV_CAPABILITY_SHELL_PROJECTION = {
    "schema": "stegos.site.kv_capability_shell_projection.v1",
    "source_kv_schema": "stegverse.kv.activation-readiness-snapshot/v1",
    "source_kv_snapshot_git_blob": "5b2fcf27e5daebd4e90db18565b6a5444e8e4611",
    "source_kv_facts_observed_at": "2026-08-27T04:08:00Z",
    "source_stegos_view_schema": "stegos.kv_capability_shell_view.v1",
    "source_stegos_merge": "4dad89be44e472eb4a5db10bfd294ded803d1456",
    "source_stegos_reconciliation_merge": "48ddcfeb5c782c5ffbf59746e924d2f9426d4948",
    "baseline_intr_complete": true,
    "production_interlock_runtime_activated": false,
    "entry_count": 46,
    "counts": {
      "local_ready": 45,
      "local_blocked": 1,
      "governed_ready": 0,
      "governed_blocked": 46
    },
    "entries": [
      {
        "entry_type": "MODULE",
        "entry_id": "stegid-continuity",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "BLOCKED_CURRENT_IDENTITY",
        "materialize_local": false,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "current_identity_continuity_receipt_observed",
            "production_interlock_runtime_activated"
          ]
        },
        "local_blocked_reason": "BLOCKED_CURRENT_IDENTITY"
      },
      {
        "entry_type": "MODULE",
        "entry_id": "governance-steggate",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "governance_runtime_admission_observed",
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "MODULE",
        "entry_id": "stegtalk",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "MODULE",
        "entry_id": "stegwhisper",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "MODULE",
        "entry_id": "steghealth",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "MODULE",
        "entry_id": "stegfin-wallet-pay",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "skap_vault_runtime_boundary_observed",
            "tvc_resident_key_liveness_observed",
            "ready_for_owner_ingress_observed",
            "production_gateway_route_observed",
            "production_double_interlock_receipts_observed",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "MODULE",
        "entry_id": "genealogy",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "MODULE",
        "entry_id": "media-playlists-reading",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "MODULE",
        "entry_id": "family-sharing",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "MODULE",
        "entry_id": "organization-context",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "MODULE",
        "entry_id": "auri-ecosystem-chat",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "MODULE",
        "entry_id": "stegteacher-onboarding",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "MODULE",
        "entry_id": "erl-research",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "calendar-scheduling",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "tasks-reminders",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_DEVICE_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "contacts",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "email-continuity",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "benefits-claims",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "legal-records",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "insurance",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "home-household",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_DEVICE_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "vehicles",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "travel",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "education-records",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "employment-history",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "credentials-certifications",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_DEVICE_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "property-assets",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "taxes",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "subscriptions",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "purchases-warranties",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "photos-memories",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_DEVICE_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "personal-journal",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "goals-plans",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "recipes-food",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_DEVICE_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "fitness",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_DEVICE_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "device-inventory",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_DEVICE_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "software-licenses",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "digital-inheritance",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "emergency-information",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_DEVICE_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "estate-planning",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "contracts",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "professional-portfolio",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "creative-works",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_DEVICE_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "music-projects",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_DEVICE_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "family-history",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_MATERIALIZATION",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      },
      {
        "entry_type": "SERVICE",
        "entry_id": "research-libraries",
        "install_state": "INSTALLED_INACTIVE",
        "local_state": "READY_FOR_LOCAL_UI",
        "materialize_local": true,
        "governed_control": {
          "present": true,
          "enabled": false,
          "blockers": [
            "production_interlock_runtime_activated",
            "provider_session_evidence_observed"
          ]
        }
      }
    ],
    "activation_control_present": false,
    "kv_state_mutation_available": false,
    "provider_execution_available": false,
    "activation_performed": false,
    "authority_effect": "NONE"
  };

  function validateKvCapabilityShellProjection(value) {
    if (!value || value.schema !== "stegos.site.kv_capability_shell_projection.v1") throw new Error("KV capability shell schema mismatch");
    if (value.authority_effect !== "NONE") throw new Error("KV capability shell authority_effect must be NONE");
    if (value.activation_performed !== false) throw new Error("KV capability shell may not perform activation");
    if (value.activation_control_present !== false) throw new Error("KV capability shell activation control prohibited");
    if (value.kv_state_mutation_available !== false) throw new Error("KV capability shell KV mutation prohibited");
    if (value.provider_execution_available !== false) throw new Error("KV capability shell provider execution prohibited");
    if (!Array.isArray(value.entries) || value.entry_count !== value.entries.length) throw new Error("KV capability shell entry count mismatch");

    var seen = {};
    var localReady = 0;
    var localBlocked = 0;
    var governedReady = 0;
    var governedBlocked = 0;
    value.entries.forEach(function (entry) {
      if (!entry || (entry.entry_type !== "MODULE" && entry.entry_type !== "SERVICE")) throw new Error("KV capability shell entry type invalid");
      if (!entry.entry_id) throw new Error("KV capability shell entry id required");
      var key = entry.entry_type + ":" + entry.entry_id;
      if (seen[key]) throw new Error("KV capability shell duplicate entry");
      seen[key] = true;
      if (entry.install_state !== "INSTALLED_INACTIVE") throw new Error("KV capability shell entry must remain INSTALLED_INACTIVE");
      if (typeof entry.materialize_local !== "boolean") throw new Error("KV capability shell materialize_local must be boolean");
      if (!entry.governed_control || entry.governed_control.present !== true || typeof entry.governed_control.enabled !== "boolean") throw new Error("KV capability shell governed control invalid");
      if (!Array.isArray(entry.governed_control.blockers)) throw new Error("KV capability shell governed blockers invalid");
      if (entry.governed_control.enabled && entry.governed_control.blockers.length) throw new Error("enabled governed control may not retain blockers");
      if (!entry.governed_control.enabled && !entry.governed_control.blockers.length) throw new Error("disabled governed control must expose blockers");
      if (!entry.materialize_local && !entry.local_blocked_reason) throw new Error("locally blocked capability must expose reason");
      if (entry.materialize_local) localReady += 1; else localBlocked += 1;
      if (entry.governed_control.enabled) governedReady += 1; else governedBlocked += 1;
    });

    if (!value.counts ||
        value.counts.local_ready !== localReady ||
        value.counts.local_blocked !== localBlocked ||
        value.counts.governed_ready !== governedReady ||
        value.counts.governed_blocked !== governedBlocked) {
      throw new Error("KV capability shell summary mismatch");
    }
    if (value.production_interlock_runtime_activated !== true && governedReady !== 0) throw new Error("governed control enabled before production Interlock runtime");
    return value;
  }

  function capabilityCard(entry) {
    var card = document.createElement("article");
    card.className = "capability-card" + (entry.materialize_local ? "" : " capability-blocked");
    var heading = document.createElement("h4");
    heading.textContent = entry.entry_id;
    var local = document.createElement("p");
    local.className = "capability-state";
    local.textContent = "Local: " + (entry.materialize_local ? entry.local_state : entry.local_blocked_reason);
    var install = document.createElement("p");
    install.className = "capability-state";
    install.textContent = "Install state: " + entry.install_state;
    var governed = document.createElement("p");
    governed.className = entry.governed_control.enabled ? "governed-enabled" : "governed-disabled";
    governed.textContent = entry.governed_control.enabled ? "Governed action: enabled" : "Governed action: disabled";
    var blockers = document.createElement("p");
    blockers.className = "capability-state";
    blockers.textContent = entry.governed_control.enabled ? "Blockers: none" : "Blockers: " + entry.governed_control.blockers.join(", ");
    card.appendChild(heading);
    card.appendChild(local);
    card.appendChild(install);
    card.appendChild(governed);
    card.appendChild(blockers);
    return card;
  }

  function renderKvCapabilityShell(projectionValue) {
    var projection = validateKvCapabilityShellProjection(projectionValue || KV_CAPABILITY_SHELL_PROJECTION);
    var targets = {
      availableModule: document.getElementById("kv-available-modules"),
      availableService: document.getElementById("kv-available-services"),
      blockedModule: document.getElementById("kv-blocked-modules"),
      blockedService: document.getElementById("kv-blocked-services")
    };
    Object.keys(targets).forEach(function (key) {
      if (!targets[key]) throw new Error("KV capability shell target missing: " + key);
      targets[key].textContent = "";
    });

    projection.entries.forEach(function (entry) {
      var key = (entry.materialize_local ? "available" : "blocked") + (entry.entry_type === "MODULE" ? "Module" : "Service");
      targets[key].appendChild(capabilityCard(entry));
    });

    document.getElementById("kv-capability-local-ready").textContent = String(projection.counts.local_ready);
    document.getElementById("kv-capability-local-blocked").textContent = String(projection.counts.local_blocked);
    document.getElementById("kv-capability-governed-ready").textContent = String(projection.counts.governed_ready);
    document.getElementById("kv-capability-governed-blocked").textContent = String(projection.counts.governed_blocked);
    document.getElementById("kv-capability-shell-state").textContent =
      "INSTALLED_INACTIVE · source KV " + projection.source_kv_facts_observed_at +
      " · Interlock runtime " + (projection.production_interlock_runtime_activated ? "observed" : "not observed") +
      " · authority NONE";
    return projection;
  }

  function validateKvReadinessSnapshot(snapshot) {
    if (!snapshot || snapshot.schema !== "stegverse.kv.activation-readiness-snapshot/v1") throw new Error("KV readiness snapshot schema mismatch");
    if (snapshot.authority_effect !== "NONE") throw new Error("KV readiness snapshot authority_effect must be NONE");
    if (snapshot.activation_performed !== false) throw new Error("KV readiness snapshot may not perform activation");
    if (typeof snapshot.production_interlock_runtime_activated !== "boolean") throw new Error("KV readiness Interlock state must be boolean");
    if (!Array.isArray(snapshot.entries) || snapshot.entry_count !== snapshot.entries.length) throw new Error("KV readiness snapshot entry count mismatch");
    if (typeof snapshot.module_count !== "number" || typeof snapshot.service_count !== "number") throw new Error("KV readiness type counts required");

    var seen = {};
    var modules = 0;
    var services = 0;
    snapshot.entries.forEach(function (entry) {
      if (!entry || (entry.entry_type !== "MODULE" && entry.entry_type !== "SERVICE")) throw new Error("KV readiness entry type invalid");
      if (!entry.entry_id) throw new Error("KV readiness entry id required");
      var key = entry.entry_type + ":" + entry.entry_id;
      if (seen[key]) throw new Error("KV readiness duplicate entry");
      seen[key] = true;
      if (entry.install_state !== "INSTALLED_INACTIVE") throw new Error("KV readiness entry must remain INSTALLED_INACTIVE");
      if (entry.activation_performed !== false) throw new Error("KV readiness entry may not perform activation");
      if (entry.authority_effect !== "NONE") throw new Error("KV readiness entry authority_effect must be NONE");
      if (typeof entry.local_materialization !== "string" || !entry.local_materialization) throw new Error("KV readiness local state required");
      if (entry.governed_action_readiness !== "BLOCKED" && entry.governed_action_readiness !== "READY_FOR_GOVERNED_ACTION") throw new Error("KV readiness governed state invalid");
      if (!Array.isArray(entry.governed_blockers)) throw new Error("KV readiness governed blockers invalid");
      if (entry.governed_action_readiness === "READY_FOR_GOVERNED_ACTION") {
        if (entry.governed_blockers.length) throw new Error("governed-ready KV entry may not retain blockers");
        if (!snapshot.production_interlock_runtime_activated) throw new Error("governed-ready KV entry requires production Interlock runtime");
      } else if (!entry.governed_blockers.length) {
        throw new Error("blocked KV entry must expose blockers");
      }
      if (entry.entry_type === "MODULE") modules += 1; else services += 1;
    });
    if (modules !== snapshot.module_count || services !== snapshot.service_count) throw new Error("KV readiness module/service count mismatch");
    return snapshot;
  }

  function siteProjectionFromKvReadinessSnapshot(snapshot) {
    var validated = validateKvReadinessSnapshot(snapshot);
    var entries = validated.entries.map(function (entry) {
      var materialize = entry.local_materialization === "READY_FOR_LOCAL_MATERIALIZATION" ||
        entry.local_materialization === "READY_FOR_DEVICE_MATERIALIZATION" ||
        entry.local_materialization === "READY_FOR_LOCAL_UI";
      var projected = {
        entry_type: entry.entry_type,
        entry_id: entry.entry_id,
        install_state: entry.install_state,
        local_state: entry.local_materialization,
        materialize_local: materialize,
        governed_control: {
          present: true,
          enabled: entry.governed_action_readiness === "READY_FOR_GOVERNED_ACTION",
          blockers: entry.governed_blockers.slice()
        }
      };
      if (!materialize) projected.local_blocked_reason = entry.local_materialization;
      return projected;
    });
    var localReady = entries.filter(function (entry) { return entry.materialize_local; }).length;
    var governedReady = entries.filter(function (entry) { return entry.governed_control.enabled; }).length;
    return validateKvCapabilityShellProjection({
      schema: "stegos.site.kv_capability_shell_projection.v1",
      source_kv_schema: validated.schema,
      source_kv_snapshot_git_blob: null,
      source_kv_facts_observed_at: validated.facts_observed_at || null,
      source_stegos_view_schema: "stegos.kv_capability_shell_view.v1",
      source_stegos_merge: "ff6eb6348c994f6bfe8eb6fcaedd2481bce151fe",
      source_stegos_reconciliation_merge: null,
      baseline_intr_complete: validated.baseline_intr_complete === true,
      production_interlock_runtime_activated: validated.production_interlock_runtime_activated,
      entry_count: entries.length,
      counts: {
        local_ready: localReady,
        local_blocked: entries.length - localReady,
        governed_ready: governedReady,
        governed_blocked: entries.length - governedReady
      },
      entries: entries,
      activation_control_present: false,
      kv_state_mutation_available: false,
      provider_execution_available: false,
      activation_performed: false,
      authority_effect: "NONE"
    });
  }

  function sha256Prefixed(value) {
    return sha256Hex(value).then(function (digest) { return "sha256:" + digest; });
  }

  function validateKvReadinessUpdateEnvelope(envelope) {
    if (!envelope || envelope.schema !== "stegos.kv_readiness_update_envelope.v1") throw new Error("KV readiness update envelope schema mismatch");
    if (envelope.transport_binding !== "UNBOUND") throw new Error("KV readiness update transport must remain UNBOUND");
    if (envelope.transport_delivery_performed !== false) throw new Error("KV readiness update may not claim transport delivery");
    if (envelope.interlock_delivery_admission_observed !== false) throw new Error("KV readiness update may not claim Interlock delivery");
    if (envelope.activation_performed !== false) throw new Error("KV readiness update may not perform activation");
    if (envelope.kv_mutation_performed !== false) throw new Error("KV readiness update may not mutate KV");
    if (envelope.provider_operation_authorized !== false) throw new Error("KV readiness update may not authorize provider operation");
    if (envelope.execution_authority !== "NONE") throw new Error("KV readiness update execution authority must be NONE");
    if (envelope.authority_effect !== "NONE") throw new Error("KV readiness update authority_effect must be NONE");
    if (typeof envelope.prior_snapshot_sha256 !== "string" || typeof envelope.successor_snapshot_sha256 !== "string") throw new Error("KV readiness update snapshot bindings required");
    if (typeof envelope.envelope_sha256 !== "string") throw new Error("KV readiness update digest required");
    var body = Object.assign({}, envelope);
    var claimed = body.envelope_sha256;
    delete body.envelope_sha256;
    return sha256Prefixed(body).then(function (actual) {
      if (actual !== claimed) throw new Error("KV readiness update envelope digest mismatch");
      return envelope;
    });
  }

  function buildKvReadinessBrowserState(snapshot, projection, previousState, envelope) {
    return sha256Prefixed(snapshot).then(function (snapshotDigest) {
      var body = {
        schema: "stegos.site.kv_device_readiness_state.v1",
        current_snapshot_sha256: snapshotDigest,
        current_facts_observed_at: snapshot.facts_observed_at || null,
        current_projection: projection,
        applied_update_count: previousState ? previousState.applied_update_count + 1 : 0,
        last_applied_envelope_sha256: envelope ? envelope.envelope_sha256 : null,
        last_prior_snapshot_sha256: previousState ? previousState.current_snapshot_sha256 : null,
        local_state_refresh_performed: !!previousState,
        transport_delivery_performed: false,
        interlock_delivery_admission_observed: false,
        kv_mutation_performed: false,
        activation_performed: false,
        provider_operation_authorized: false,
        execution_authority: "NONE",
        authority_effect: "NONE"
      };
      return sha256Prefixed(body).then(function (stateDigest) {
        body.state_sha256 = stateDigest;
        return body;
      });
    });
  }

  function validateKvReadinessBrowserState(state) {
    if (!state || state.schema !== "stegos.site.kv_device_readiness_state.v1") return Promise.reject(new Error("KV browser readiness state schema mismatch"));
    if (state.transport_delivery_performed !== false) return Promise.reject(new Error("KV browser state may not claim transport delivery"));
    if (state.interlock_delivery_admission_observed !== false) return Promise.reject(new Error("KV browser state may not claim Interlock delivery"));
    if (state.kv_mutation_performed !== false) return Promise.reject(new Error("KV browser state may not mutate KV"));
    if (state.activation_performed !== false) return Promise.reject(new Error("KV browser state may not perform activation"));
    if (state.provider_operation_authorized !== false) return Promise.reject(new Error("KV browser state may not authorize provider operation"));
    if (state.execution_authority !== "NONE" || state.authority_effect !== "NONE") return Promise.reject(new Error("KV browser state authority boundary invalid"));
    if (typeof state.applied_update_count !== "number" || state.applied_update_count < 0) return Promise.reject(new Error("KV browser state update count invalid"));
    try {
      validateKvCapabilityShellProjection(state.current_projection);
    } catch (error) {
      return Promise.reject(error);
    }
    var body = Object.assign({}, state);
    var claimed = body.state_sha256;
    delete body.state_sha256;
    return sha256Prefixed(body).then(function (actual) {
      if (actual !== claimed) throw new Error("KV browser readiness state digest mismatch");
      return state;
    });
  }

  function loadCanonicalKvReadinessSnapshot() {
    return fetch(KV_READINESS_SNAPSHOT_URL, { cache: "no-store" }).then(function (response) {
      if (!response.ok) throw new Error("KV readiness snapshot unavailable");
      return response.json();
    }).then(validateKvReadinessSnapshot);
  }

  function initializeKvReadinessBrowserState() {
    return getMeta(KV_READINESS_STATE_KEY).then(function (existing) {
      if (existing) return validateKvReadinessBrowserState(existing);
      return loadCanonicalKvReadinessSnapshot().then(function (snapshot) {
        var projection = siteProjectionFromKvReadinessSnapshot(snapshot);
        if (canonicalize(projection.entries) !== canonicalize(validateKvCapabilityShellProjection(KV_CAPABILITY_SHELL_PROJECTION).entries)) {
          throw new Error("initial KV readiness snapshot/projection drift");
        }
        return buildKvReadinessBrowserState(snapshot, projection, null, null).then(function (state) {
          return putMeta(KV_READINESS_STATE_KEY, state);
        });
      });
    });
  }

  function applyKvReadinessUpdate(envelope, priorSnapshot, successorSnapshot) {
    return Promise.all([
      getMeta(KV_READINESS_STATE_KEY),
      validateKvReadinessUpdateEnvelope(envelope),
      Promise.resolve(validateKvReadinessSnapshot(priorSnapshot)),
      Promise.resolve(validateKvReadinessSnapshot(successorSnapshot))
    ]).then(function (values) {
      var state = values[0];
      if (!state) throw new Error("KV browser readiness state not initialized");
      return validateKvReadinessBrowserState(state).then(function () {
        return Promise.all([sha256Prefixed(priorSnapshot), sha256Prefixed(successorSnapshot)]).then(function (digests) {
          if (state.current_snapshot_sha256 !== digests[0]) throw new Error("stale or replayed KV readiness update");
          if (envelope.prior_snapshot_sha256 !== state.current_snapshot_sha256) throw new Error("KV readiness envelope prior digest mismatch");
          if (envelope.successor_snapshot_sha256 !== digests[1]) throw new Error("KV readiness envelope successor digest mismatch");
          var priorKeys = priorSnapshot.entries.map(function (entry) { return entry.entry_type + ":" + entry.entry_id; }).sort();
          var successorKeys = successorSnapshot.entries.map(function (entry) { return entry.entry_type + ":" + entry.entry_id; }).sort();
          if (canonicalize(priorKeys) !== canonicalize(successorKeys)) throw new Error("KV readiness entry identity drift");
          var projection = siteProjectionFromKvReadinessSnapshot(successorSnapshot);
          return buildKvReadinessBrowserState(successorSnapshot, projection, state, envelope).then(function (updated) {
            return putMeta(KV_READINESS_STATE_KEY, updated).then(function () {
              renderKvCapabilityShell(projection);
              return updated;
            });
          });
        });
      });
    });
  }

  function bytesToHex(bytes) {
    var out = "";
    for (var i = 0; i < bytes.length; i += 1) out += bytes[i].toString(16).padStart(2, "0");
    return out;
  }

  function canonicalize(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) return "[" + value.map(canonicalize).join(",") + "]";
    return "{" + Object.keys(value).sort().map(function (key) {
      return JSON.stringify(key) + ":" + canonicalize(value[key]);
    }).join(",") + "}";
  }

  function sha256Hex(value) {
    var text = typeof value === "string" ? value : canonicalize(value);
    return crypto.subtle.digest("SHA-256", new TextEncoder().encode(text)).then(function (digest) {
      return bytesToHex(new Uint8Array(digest));
    });
  }

  function openDb() {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onupgradeneeded = function () {
        var db = request.result;
        if (!db.objectStoreNames.contains(META)) db.createObjectStore(META, { keyPath: "key" });
        if (!db.objectStoreNames.contains(RECEIPTS)) db.createObjectStore(RECEIPTS, { keyPath: "receipt_number" });
      };
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error || new Error("StegOS Node storage unavailable")); };
    });
  }

  function txDone(tx) {
    return new Promise(function (resolve, reject) {
      tx.oncomplete = function () { resolve(); };
      tx.onerror = function () { reject(tx.error || new Error("StegOS Node storage transaction failed")); };
      tx.onabort = function () { reject(tx.error || new Error("StegOS Node storage transaction aborted")); };
    });
  }

  function getMeta(key) {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(META, "readonly");
        var req = tx.objectStore(META).get(key);
        req.onsuccess = function () { resolve(req.result ? req.result.value : null); };
        req.onerror = function () { reject(req.error); };
        tx.oncomplete = function () { db.close(); };
      });
    });
  }

  function putMeta(key, value) {
    return openDb().then(function (db) {
      var tx = db.transaction(META, "readwrite");
      tx.objectStore(META).put({ key: key, value: value });
      return txDone(tx).then(function () { db.close(); return value; });
    });
  }

  function getReceipts() {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(RECEIPTS, "readonly");
        var req = tx.objectStore(RECEIPTS).getAll();
        req.onsuccess = function () {
          var rows = req.result || [];
          rows.sort(function (a, b) { return a.receipt_number - b.receipt_number; });
          resolve(rows);
        };
        req.onerror = function () { reject(req.error); };
        tx.oncomplete = function () { db.close(); };
      });
    });
  }

  function putReceipt(receipt) {
    return openDb().then(function (db) {
      var tx = db.transaction(RECEIPTS, "readwrite");
      tx.objectStore(RECEIPTS).put(receipt);
      return txDone(tx).then(function () { db.close(); return receipt; });
    });
  }

  function validateGenesis(receipt) {
    if (!receipt || receipt.schema !== "stegos.node_handoff_receipt.v1") throw new Error("Invalid Receipt #1 schema");
    if (receipt.receipt_number !== 1 || receipt.transition !== "NODE_REGISTERED") throw new Error("Invalid Receipt #1 transition");
    if (receipt.prior_state !== "UNREGISTERED" || receipt.resulting_state !== "REGISTERED") throw new Error("Invalid Receipt #1 states");
    if (receipt.continuity_parent !== "GENESIS") throw new Error("Invalid Receipt #1 continuity parent");
    if (receipt.authority_effect !== "NONE") throw new Error("Receipt #1 cannot grant external authority");
    if (receipt.credential_authority !== "TV/TVC") throw new Error("Credential authority mismatch");
    var body = Object.assign({}, receipt);
    var claimed = body.receipt_sha256;
    delete body.receipt_sha256;
    return sha256Hex(body).then(function (actual) {
      if (actual !== claimed) throw new Error("Receipt #1 digest mismatch");
      return receipt;
    });
  }

  function deriveIdentity(deviceBindingSha256, label, prefix) {
    return sha256Hex(label + ":" + deviceBindingSha256).then(function (digest) {
      return prefix + digest.slice(0, 24);
    });
  }

  function createGenesis(deviceBindingSha256) {
    return Promise.all([
      deriveIdentity(deviceBindingSha256, "stegos-node", "SV-NODE-"),
      deriveIdentity(deviceBindingSha256, "stegos-interlock", "SV-IL-")
    ]).then(function (ids) {
      var body = {
        schema: "stegos.node_handoff_receipt.v1",
        receipt_number: 1,
        transition: "NODE_REGISTERED",
        prior_state: "UNREGISTERED",
        resulting_state: "REGISTERED",
        continuity_parent: "GENESIS",
        node_id: ids[0],
        interlock_id: ids[1],
        device_binding_sha256: deviceBindingSha256,
        authority_effect: "NONE",
        heartbeat_authority: "StegVerse-Labs/.github",
        credential_authority: "TV/TVC"
      };
      return sha256Hex(body).then(function (digest) {
        return Object.assign({}, body, { receipt_sha256: digest });
      });
    });
  }

  function registerDevice() {
    return Promise.all([getMeta(REGISTRATION_KEY), getReceipts()]).then(function (values) {
      var existing = values[0];
      var receipts = values[1];
      if (existing && receipts.length) {
        return validateGenesis(receipts[0]).then(function () { return existing; });
      }
      var random = new Uint8Array(32);
      crypto.getRandomValues(random);
      return sha256Hex(bytesToHex(random)).then(function (commitment) {
        random.fill(0);
        return createGenesis(commitment);
      }).then(function (receipt) {
        return validateGenesis(receipt).then(function () {
          var registration = {
            schema: "stegos.node_registration_projection.v1",
            state: "REGISTERED",
            node_id: receipt.node_id,
            interlock_id: receipt.interlock_id,
            device_binding_sha256: receipt.device_binding_sha256,
            receipt_number: 1,
            receipt_sha256: receipt.receipt_sha256,
            knowledge_vault_materialization_enabled: true,
            hardware_attestation_claimed: false,
            credential_authority: "TV/TVC",
            authority_effect: "NONE"
          };
          return putReceipt(receipt).then(function () { return putMeta(REGISTRATION_KEY, registration); });
        });
      });
    });
  }

  function sectionFor(receipt) {
    var transition = String(receipt.transition || receipt.event || "").toUpperCase();
    if (transition.indexOf("REGISTER") >= 0) return "Device Registration";
    if (transition.indexOf("KV") >= 0 || transition.indexOf("VAULT") >= 0) return "KnowledgeVault";
    if (transition.indexOf("HEARTBEAT") >= 0 || transition.indexOf("SYNC") >= 0) return "HeartBeat";
    if (transition.indexOf("MODULE") >= 0) return "Modules";
    if (transition.indexOf("INSTALL") >= 0) return "Installation";
    if (transition.indexOf("EXTERNAL") >= 0 || transition.indexOf("CONNECT") >= 0) return "External Connections";
    if (transition.indexOf("STATE") >= 0) return "Device State";
    return "Other";
  }

  function historyProjection() {
    return Promise.all([
      getMeta(REGISTRATION_KEY),
      getMeta(PERSONAL_KV_SYNC_KEY),
      getMeta(NETWORK_SYNC_KEY),
      getMeta(OFFLINE_PROOF_KEY),
      getReceipts()
    ]).then(function (values) {
      var registration = values[0];
      var receipts = values[4];
      var sections = {};
      receipts.forEach(function (receipt) {
        var section = sectionFor(receipt);
        if (!sections[section]) sections[section] = [];
        sections[section].push(receipt);
      });
      return {
        schema: "stegos.offline_device_history_projection.v1",
        offline_capable: true,
        current_network_required: false,
        registration: registration,
        local_receipt_head: receipts.length ? {
          receipt_number: receipts[receipts.length - 1].receipt_number,
          receipt_sha256: receipts[receipts.length - 1].receipt_sha256
        } : null,
        last_personal_kv_sync: values[1],
        last_stegos_network_sync: values[2],
        offline_reload_proof: values[3],
        sections: sections,
        canonical_chain_receipt_count: receipts.length,
        section_views_are_filtered_projections: true,
        competing_logs_allowed: false,
        wall_clock_is_causal_order: false,
        credential_authority: "TV/TVC",
        authority_effect: "NONE"
      };
    });
  }

  function validateOfflineReloadProof(proof, projection) {
    if (!proof) return Promise.resolve(null);
    if (proof.schema !== "stegos.node_offline_reload_proof.v1") throw new Error("Invalid offline reload proof schema");
    if (!projection || !projection.registration || !projection.local_receipt_head) throw new Error("Offline reload proof requires registered local continuity");
    var invariants = {
      service_worker_controlled: true,
      offline_observed: true,
      current_network_required: false,
      network_topology_claimed: false,
      heartbeat_interlock_observation_verified: false,
      physical_activation_claimed: false,
      network_activation_claimed: false,
      credential_authority: "TV/TVC",
      authority_effect: "NONE"
    };
    Object.keys(invariants).forEach(function (key) {
      if (proof[key] !== invariants[key]) throw new Error("Invalid offline proof invariant " + key);
    });
    if (proof.node_id !== projection.registration.node_id) throw new Error("Offline proof Node mismatch");
    if (proof.interlock_id !== projection.registration.interlock_id) throw new Error("Offline proof Interlock mismatch");
    if (proof.local_receipt_head.receipt_number !== projection.local_receipt_head.receipt_number ||
        proof.local_receipt_head.receipt_sha256 !== projection.local_receipt_head.receipt_sha256) {
      throw new Error("Offline proof local head mismatch");
    }
    if (proof.canonical_chain_receipt_count !== projection.canonical_chain_receipt_count) throw new Error("Offline proof receipt count mismatch");
    var body = Object.assign({}, proof);
    var claimed = body.proof_sha256;
    delete body.proof_sha256;
    return sha256Hex(body).then(function (actual) {
      if (actual !== claimed) throw new Error("Offline reload proof digest mismatch");
      return proof;
    });
  }

  function recordOfflineReloadProof() {
    return historyProjection().then(function (projection) {
      if (!projection.registration || !projection.local_receipt_head) return null;
      var controlled = Boolean(navigator.serviceWorker && navigator.serviceWorker.controller);
      var offline = navigator.onLine === false;
      if (!controlled || !offline) return projection.offline_reload_proof || null;
      var body = {
        schema: "stegos.node_offline_reload_proof.v1",
        node_id: projection.registration.node_id,
        interlock_id: projection.registration.interlock_id,
        local_receipt_head: projection.local_receipt_head,
        canonical_chain_receipt_count: projection.canonical_chain_receipt_count,
        service_worker_controlled: true,
        offline_observed: true,
        current_network_required: false,
        network_topology_claimed: false,
        heartbeat_interlock_observation_verified: false,
        physical_activation_claimed: false,
        network_activation_claimed: false,
        credential_authority: "TV/TVC",
        authority_effect: "NONE",
        observed_at: new Date().toISOString()
      };
      return sha256Hex(body).then(function (digest) {
        var proof = Object.assign({}, body, { proof_sha256: digest });
        return putMeta(OFFLINE_PROOF_KEY, proof).then(function () { return proof; });
      });
    });
  }

  function syncText(sync) {
    if (!sync) return "Not yet observed";
    var head = sync.receipt_number ? "Receipt #" + sync.receipt_number : "Observed";
    return sync.observed_at ? head + " · " + sync.observed_at : head;
  }

  function offlineProofText(proof) {
    if (!proof) return "Not yet observed";
    return proof.offline_observed && proof.service_worker_controlled ? "Recorded" : "Invalid";
  }

  function render() {
    return historyProjection().then(function (projection) {
      var registerButton = document.getElementById("register-device");
      var state = document.getElementById("node-state");
      var nodeId = document.getElementById("node-id");
      var receiptHead = document.getElementById("local-receipt-head");
      var personal = document.getElementById("personal-kv-sync");
      var network = document.getElementById("network-sync");
      var offlineProof = document.getElementById("offline-reload-proof");
      var kv = document.getElementById("knowledge-vault-state");
      var history = document.getElementById("history");

      if (projection.registration) {
        state.textContent = "REGISTERED";
        nodeId.textContent = projection.registration.node_id;
        registerButton.disabled = true;
        registerButton.textContent = "Device Registered";
        kv.textContent = "Available";
      } else {
        state.textContent = "UNREGISTERED";
        nodeId.textContent = "Not registered";
        kv.textContent = "Locked until Receipt #1";
      }
      receiptHead.textContent = projection.local_receipt_head ? "Receipt #" + projection.local_receipt_head.receipt_number : "None";
      personal.textContent = syncText(projection.last_personal_kv_sync);
      network.textContent = syncText(projection.last_stegos_network_sync);
      if (offlineProof) offlineProof.textContent = offlineProofText(projection.offline_reload_proof);
      history.innerHTML = "";

      Object.keys(projection.sections).forEach(function (sectionName) {
        var section = document.createElement("section");
        section.className = "history-section";
        var heading = document.createElement("h3");
        heading.textContent = sectionName;
        var links = document.createElement("p");
        links.className = "section-links";
        links.innerHTML = '<a href="#about-' + sectionName.toLowerCase().replace(/[^a-z0-9]+/g, "-") + '">What is this?</a> · <button type="button" class="link-button">View receipts</button>';
        var list = document.createElement("ol");
        list.hidden = true;
        projection.sections[sectionName].forEach(function (receipt) {
          var item = document.createElement("li");
          item.textContent = "Receipt #" + receipt.receipt_number + " — " + (receipt.transition || receipt.event || "Transition");
          list.appendChild(item);
        });
        links.querySelector("button").addEventListener("click", function () { list.hidden = !list.hidden; });
        section.appendChild(heading);
        section.appendChild(links);
        section.appendChild(list);
        history.appendChild(section);
      });
      return projection;
    });
  }

  function observeOfflineReloadWhenReady() {
    if (!("serviceWorker" in navigator)) return Promise.resolve(null);
    return navigator.serviceWorker.ready.then(function () {
      return recordOfflineReloadProof();
    }).then(function (proof) {
      if (proof) return render().then(function () { return proof; });
      return null;
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initializeKvReadinessBrowserState().then(function (state) {
      renderKvCapabilityShell(state.current_projection);
    }).catch(function (error) {
      var shellState = document.getElementById("kv-capability-shell-state");
      if (shellState) shellState.textContent = "FAIL_CLOSED: " + error.message;
    });
    var button = document.getElementById("register-device");
    button.addEventListener("click", function () {
      button.disabled = true;
      button.textContent = "Registering…";
      registerDevice().then(render).catch(function (error) {
        button.disabled = false;
        button.textContent = "Register Device";
        document.getElementById("node-error").textContent = "FAIL_CLOSED: " + error.message;
      });
    });
    render();
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("./service-worker.js").then(observeOfflineReloadWhenReady).catch(function (error) {
        document.getElementById("node-error").textContent = "FAIL_CLOSED: " + error.message;
      });
    }
  });

  window.StegOSNodeProjection = {
    registerDevice: registerDevice,
    historyProjection: historyProjection,
    validateGenesis: validateGenesis,
    validateOfflineReloadProof: validateOfflineReloadProof,
    recordOfflineReloadProof: recordOfflineReloadProof,
    kvCapabilityShellProjection: function () { return validateKvCapabilityShellProjection(KV_CAPABILITY_SHELL_PROJECTION); },
    renderKvCapabilityShell: renderKvCapabilityShell,
    validateKvReadinessSnapshot: validateKvReadinessSnapshot,
    initializeKvReadinessBrowserState: initializeKvReadinessBrowserState,
    applyKvReadinessUpdate: applyKvReadinessUpdate,
    validateKvReadinessBrowserState: validateKvReadinessBrowserState
  };
}());
