"use strict";

(function () {
  var DB_NAME = "stegos-node-v1";
  var DB_VERSION = 2;
  var META = "meta";
  var RECEIPTS = "receipts";
  var INTR_OUTBOX = "intr_outbox";
  var HIL_DB_NAME = "stegverse-hil-v3";
  var HIL_STORE_NAME = "response_files";
  var HIL_RECORD_KEY = "stegverse.hil.submissions.v1";
  var GITHUB_RUNTIME_AUTHORITY_FIELD = "github" + "_token_runtime_authority";
  var HIL_PRIMARY_SHA256 = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462";
  var HIL_PROMPT_SHA256 = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c";
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
      " · governed capability activation predicate " + (projection.production_interlock_runtime_activated ? "satisfied" : "not satisfied") +
      " · device-local InTr state is separate · authority NONE";
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

  var KV_INTR_RECEIPT_FIELDS = [
    "schema",
    "receipt_id",
    "packet_id",
    "hop_index",
    "direction",
    "from_role",
    "to_role",
    "operation_hash",
    "payload_hash",
    "prior_receipt_hash",
    "boundary_identity_ref",
    "boundary_verification",
    "transition_state",
    "secret_plaintext_present",
    "authority_transfer",
    "recorded_at",
    "receipt_hash"
  ].sort();

  var KV_INTR_DELIVERY_ADMISSION_FIELDS = [
    "schema",
    "envelope_sha256",
    "envelope_payload_sha256",
    "prior_snapshot_sha256",
    "successor_snapshot_sha256",
    "intr_receipt_hash",
    "intr_packet_id",
    "intr_operation_hash",
    "intr_direction",
    "intr_hop_index",
    "intr_from_role",
    "intr_to_role",
    "device_boundary_identity_ref",
    "transport_binding",
    "transport_delivery_performed",
    "interlock_delivery_admission_observed",
    "kv_mutation_performed",
    "activation_performed",
    "provider_operation_authorized",
    "execution_authority",
    "authority_effect",
    "admission_sha256"
  ].sort();

  function isSha256Uri(value) {
    return typeof value === "string" && /^sha256:[0-9a-f]{64}$/.test(value);
  }

  function validateKvReadinessIntrReceipt(receipt, envelope, expectedDeviceBoundaryRef) {
    if (!receipt || receipt.schema !== "stegverse.intr.hop_receipt/v1") {
      return Promise.reject(new Error("KV readiness InTr receipt schema mismatch"));
    }
    var actualFields = Object.keys(receipt).sort();
    if (canonicalize(actualFields) !== canonicalize(KV_INTR_RECEIPT_FIELDS)) {
      return Promise.reject(new Error("KV readiness InTr receipt canonical field mismatch"));
    }
    if (typeof receipt.receipt_id !== "string" || !receipt.receipt_id) return Promise.reject(new Error("KV readiness InTr receipt_id required"));
    if (typeof receipt.packet_id !== "string" || !receipt.packet_id) return Promise.reject(new Error("KV readiness InTr packet_id required"));
    if (receipt.direction !== "FORWARD") return Promise.reject(new Error("KV readiness InTr direction must be FORWARD"));
    if (receipt.hop_index !== 1) return Promise.reject(new Error("KV readiness InTr hop_index must be 1"));
    if (receipt.from_role !== "KV" || receipt.to_role !== "DEVICE") return Promise.reject(new Error("KV readiness InTr hop must be KV->DEVICE"));
    if (typeof expectedDeviceBoundaryRef !== "string" || !expectedDeviceBoundaryRef) return Promise.reject(new Error("expected device boundary required"));
    if (receipt.boundary_identity_ref !== expectedDeviceBoundaryRef) return Promise.reject(new Error("KV readiness InTr device boundary mismatch"));
    if (receipt.boundary_verification !== "VERIFIED") return Promise.reject(new Error("KV readiness InTr boundary must be VERIFIED"));
    if (receipt.transition_state !== "RECEIVED") return Promise.reject(new Error("KV readiness InTr transition must be RECEIVED"));
    if (receipt.secret_plaintext_present !== false) return Promise.reject(new Error("KV readiness InTr receipt may not contain secret plaintext"));
    if (receipt.authority_transfer !== false) return Promise.reject(new Error("KV readiness InTr receipt may not transfer authority"));
    if (!isSha256Uri(receipt.operation_hash)) return Promise.reject(new Error("KV readiness InTr operation_hash invalid"));
    if (!isSha256Uri(receipt.payload_hash)) return Promise.reject(new Error("KV readiness InTr payload_hash invalid"));
    if (receipt.prior_receipt_hash !== null && typeof receipt.prior_receipt_hash !== "string") {
      return Promise.reject(new Error("KV readiness InTr prior_receipt_hash must be string or null"));
    }
    if (typeof receipt.recorded_at !== "string" || !receipt.recorded_at) return Promise.reject(new Error("KV readiness InTr recorded_at required"));
    if (!isSha256Uri(receipt.receipt_hash)) return Promise.reject(new Error("KV readiness InTr receipt_hash invalid"));

    return sha256Prefixed(envelope).then(function (payloadDigest) {
      if (receipt.payload_hash !== payloadDigest) throw new Error("KV readiness InTr payload does not bind exact envelope");
      var body = Object.assign({}, receipt);
      var claimed = body.receipt_hash;
      delete body.receipt_hash;
      return sha256Prefixed(body).then(function (actual) {
        if (claimed !== actual) throw new Error("KV readiness InTr receipt hash mismatch");
        return receipt;
      });
    });
  }

  function validateKvReadinessIntrDeliveryAdmission(admission, envelope, priorSnapshot, successorSnapshot, intrReceipt, expectedDeviceBoundaryRef) {
    if (!admission || admission.schema !== "stegos.kv_readiness_intr_delivery_admission.v1") {
      return Promise.reject(new Error("KV readiness delivery admission schema mismatch"));
    }
    var admissionFields = Object.keys(admission).sort();
    if (canonicalize(admissionFields) !== canonicalize(KV_INTR_DELIVERY_ADMISSION_FIELDS)) {
      return Promise.reject(new Error("KV readiness delivery admission canonical field mismatch"));
    }
    if (admission.transport_binding !== "INTR_KV_DEVICE") return Promise.reject(new Error("KV readiness delivery admission transport binding mismatch"));
    if (admission.transport_delivery_performed !== true) return Promise.reject(new Error("KV readiness delivery admission must prove transport delivery"));
    if (admission.interlock_delivery_admission_observed !== true) return Promise.reject(new Error("KV readiness delivery admission must prove Interlock admission"));
    if (admission.kv_mutation_performed !== false) return Promise.reject(new Error("KV readiness delivery admission may not mutate KV"));
    if (admission.activation_performed !== false) return Promise.reject(new Error("KV readiness delivery admission may not activate capabilities"));
    if (admission.provider_operation_authorized !== false) return Promise.reject(new Error("KV readiness delivery admission may not authorize provider operation"));
    if (admission.execution_authority !== "NONE") return Promise.reject(new Error("KV readiness delivery admission execution authority must be NONE"));
    if (admission.authority_effect !== "NONE") return Promise.reject(new Error("KV readiness delivery admission authority_effect must be NONE"));
    if (admission.intr_direction !== "FORWARD" || admission.intr_hop_index !== 1 || admission.intr_from_role !== "KV" || admission.intr_to_role !== "DEVICE") {
      return Promise.reject(new Error("KV readiness delivery admission canonical hop mismatch"));
    }
    if (admission.device_boundary_identity_ref !== expectedDeviceBoundaryRef) return Promise.reject(new Error("KV readiness delivery admission device boundary mismatch"));
    if (admission.envelope_sha256 !== envelope.envelope_sha256) return Promise.reject(new Error("KV readiness delivery admission envelope binding mismatch"));
    if (admission.prior_snapshot_sha256 !== envelope.prior_snapshot_sha256) return Promise.reject(new Error("KV readiness delivery admission prior binding mismatch"));
    if (admission.successor_snapshot_sha256 !== envelope.successor_snapshot_sha256) return Promise.reject(new Error("KV readiness delivery admission successor binding mismatch"));
    if (admission.intr_receipt_hash !== intrReceipt.receipt_hash || admission.intr_packet_id !== intrReceipt.packet_id || admission.intr_operation_hash !== intrReceipt.operation_hash) {
      return Promise.reject(new Error("KV readiness delivery admission InTr receipt binding mismatch"));
    }
    if (!isSha256Uri(admission.admission_sha256)) return Promise.reject(new Error("KV readiness delivery admission digest required"));

    return Promise.all([
      validateKvReadinessUpdateEnvelope(envelope),
      Promise.resolve(validateKvReadinessSnapshot(priorSnapshot)),
      Promise.resolve(validateKvReadinessSnapshot(successorSnapshot)),
      validateKvReadinessIntrReceipt(intrReceipt, envelope, expectedDeviceBoundaryRef),
      sha256Prefixed(envelope),
      sha256Prefixed(priorSnapshot),
      sha256Prefixed(successorSnapshot)
    ]).then(function (values) {
      if (admission.envelope_payload_sha256 !== values[4]) throw new Error("KV readiness delivery admission payload digest mismatch");
      if (admission.prior_snapshot_sha256 !== values[5]) throw new Error("KV readiness delivery admission prior snapshot digest mismatch");
      if (admission.successor_snapshot_sha256 !== values[6]) throw new Error("KV readiness delivery admission successor snapshot digest mismatch");
      var body = Object.assign({}, admission);
      var claimed = body.admission_sha256;
      delete body.admission_sha256;
      return sha256Prefixed(body).then(function (actual) {
        if (claimed !== actual) throw new Error("KV readiness delivery admission digest mismatch");
        return admission;
      });
    });
  }

  function applyAdmittedKvReadinessDelivery(admission, envelope, priorSnapshot, successorSnapshot, intrReceipt, expectedDeviceBoundaryRef) {
    return Promise.all([
      getMeta(KV_READINESS_STATE_KEY),
      validateKvReadinessIntrDeliveryAdmission(admission, envelope, priorSnapshot, successorSnapshot, intrReceipt, expectedDeviceBoundaryRef)
    ]).then(function (values) {
      var currentState = values[0];
      if (!currentState) throw new Error("KV browser readiness state not initialized");
      return validateKvReadinessBrowserState(currentState).then(function () {
        if (admission.prior_snapshot_sha256 !== currentState.current_snapshot_sha256) {
          throw new Error("stale or replayed admitted KV readiness delivery");
        }
        return applyKvReadinessUpdate(envelope, priorSnapshot, successorSnapshot).then(function (updatedState) {
          if (updatedState.last_applied_envelope_sha256 !== admission.envelope_sha256) throw new Error("admitted KV readiness apply envelope binding mismatch");
          if (updatedState.last_prior_snapshot_sha256 !== admission.prior_snapshot_sha256) throw new Error("admitted KV readiness apply prior binding mismatch");
          if (updatedState.current_snapshot_sha256 !== admission.successor_snapshot_sha256) throw new Error("admitted KV readiness apply successor binding mismatch");
          if (updatedState.transport_delivery_performed !== false || updatedState.interlock_delivery_admission_observed !== false) {
            throw new Error("browser readiness state must remain transport-neutral");
          }
          var body = {
            schema: "stegos.site.kv_readiness_admitted_device_apply.v1",
            device_boundary_identity_ref: expectedDeviceBoundaryRef,
            delivery_admission_sha256: admission.admission_sha256,
            intr_receipt_hash: admission.intr_receipt_hash,
            envelope_sha256: envelope.envelope_sha256,
            prior_device_state_sha256: currentState.state_sha256,
            prior_snapshot_sha256: admission.prior_snapshot_sha256,
            successor_snapshot_sha256: admission.successor_snapshot_sha256,
            updated_device_state: updatedState,
            updated_device_state_sha256: updatedState.state_sha256,
            transport_delivery_performed: true,
            interlock_delivery_admission_observed: true,
            local_state_refresh_performed: true,
            kv_mutation_performed: false,
            activation_performed: false,
            provider_operation_authorized: false,
            execution_authority: "NONE",
            authority_effect: "NONE"
          };
          return sha256Prefixed(body).then(function (digest) {
            return Object.assign({}, body, { apply_receipt_sha256: digest });
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
        if (!db.objectStoreNames.contains(INTR_OUTBOX)) db.createObjectStore(INTR_OUTBOX, { keyPath: "materialization_id" });
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


  function sha256Uri(value) {
    return sha256Hex(value).then(function (digest) { return "sha256:" + digest; });
  }

  function isSha256Uri(value) {
    return /^sha256:[a-f0-9]{64}$/.test(String(value || ""));
  }

  function openHilDb() {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(HIL_DB_NAME);
      request.onsuccess = function () {
        var db = request.result;
        if (!db.objectStoreNames.contains(HIL_STORE_NAME)) {
          db.close();
          reject(new Error("HIL staged packet store unavailable"));
          return;
        }
        resolve(db);
      };
      request.onerror = function () { reject(request.error || new Error("HIL staged packet storage unavailable")); };
      request.onupgradeneeded = function () {
        request.transaction.abort();
      };
    });
  }

  function hilParticipantRecords() {
    try {
      var value = JSON.parse(localStorage.getItem(HIL_RECORD_KEY) || "[]");
      return Array.isArray(value) ? value : [];
    } catch (_error) {
      return [];
    }
  }

  function pendingHilMaterializationIds() {
    var ids = {};
    hilParticipantRecords().forEach(function (record) {
      var request = record && record.intr_materialization_request;
      if (
        request &&
        record.intr_materialization_state === "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION" &&
        request.state === "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION" &&
        typeof request.materialization_id === "string"
      ) {
        ids[request.materialization_id] = true;
      }
    });
    return ids;
  }

  function getHilStagedPackets() {
    return openHilDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(HIL_STORE_NAME, "readonly");
        var req = tx.objectStore(HIL_STORE_NAME).getAll();
        req.onsuccess = function () { resolve(req.result || []); };
        req.onerror = function () { reject(req.error || new Error("HIL staged packet read failed")); };
        tx.oncomplete = function () { db.close(); };
      });
    });
  }

  function validateHilMaterializationRequest(staged) {
    if (!staged || !staged.bytes || !staged.provenance_manifest || !staged.intr_transport_intent || !staged.intr_materialization_request) {
      return Promise.reject(new Error("HIL staged packet incomplete"));
    }
    var intent = staged.intr_transport_intent;
    var request = staged.intr_materialization_request;
    var expectedRequestFields = {
      schema: "stegverse.universal-intr-materialization-request/v1",
      state: "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION",
      transport_schema: "stegverse.universal-intr-transport/v1",
      transport_protocol: "InTr",
      downstream_owner_ref: "StegVerse-Labs/.github#246",
      event_triggered: true,
      always_on_receiver_required: false,
      second_user_device_required: false,
      receiver_unavailable_disposition: "DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",
      exact_packet_transport_retry_allowed: true,
      blind_consequence_retry_allowed: false,
      interlock_required: true,
      request_grants_execution_authority: false,
      claim_or_fence_minted: false,
      transport_grants_execution_authority: false,
      credential_authority: "TV/TVC",
      authority_transfer: false,
      authority_effect: "NONE_REQUEST_ONLY"
    };
    expectedRequestFields[GITHUB_RUNTIME_AUTHORITY_FIELD] = "NONE";
    Object.keys(expectedRequestFields).forEach(function (key) {
      if (canonicalize(request[key]) !== canonicalize(expectedRequestFields[key])) {
        throw new Error("HIL materialization request invariant mismatch: " + key);
      }
    });
    if (
      canonicalize(request.destination) !== canonicalize({ boundary: "STEGOS_ECOSYSTEM", subsystem: "HIL:Ingress" }) ||
      canonicalize(request.boundary_path) !== canonicalize(["DEVICE_SYSTEM", "STEGOS_ECOSYSTEM"])
    ) throw new Error("HIL materialization destination invalid");
    if (!/^INTR-MAT-[a-f0-9]{24}$/.test(String(request.materialization_id || ""))) throw new Error("HIL materialization id invalid");
    if (!isSha256Uri(request.request_hash) || !isSha256Uri(request.transport_intent_hash) || !isSha256Uri(request.payload_hash)) {
      throw new Error("HIL materialization digest invalid");
    }
    if (
      intent.schema !== "stegverse.universal-intr-transport/v1" ||
      intent.protocol !== "InTr" ||
      intent.source?.boundary !== "DEVICE_SYSTEM" ||
      intent.source?.subsystem !== "Site:HIL" ||
      intent.destination?.boundary !== "STEGOS_ECOSYSTEM" ||
      intent.destination?.subsystem !== "HIL:Ingress" ||
      intent.transport_semantics?.event_triggered !== true ||
      intent.transport_semantics?.always_on_receiver_required !== false ||
      intent.transport_semantics?.second_user_device_required !== false ||
      intent.authority?.transport_grants_execution_authority !== false ||
      intent.authority?.credential_authority !== "TV/TVC"
    ) throw new Error("HIL Universal InTr intent invalid");
    if (
      request.operation_id !== intent.operation_id ||
      request.packet_id !== intent.packet_id ||
      request.payload_hash !== intent.payload_hash
    ) throw new Error("HIL materialization request transport identity mismatch");
    var expectedPayloadRef = "indexeddb://" + HIL_DB_NAME + "/" + HIL_STORE_NAME + "/" + encodeURIComponent("response:" + intent.operation_id);
    if (request.payload_ref !== expectedPayloadRef) throw new Error("HIL materialization payload_ref mismatch");

    var bytes = staged.bytes instanceof ArrayBuffer ? new Uint8Array(staged.bytes) : new Uint8Array(staged.bytes);
    return Promise.all([
      sha256Hex(bytes),
      sha256Uri(staged.provenance_manifest),
      sha256Uri(intent)
    ]).then(function (digests) {
      var responseDigest = digests[0];
      var provenanceDigest = digests[1];
      var intentDigest = digests[2];
      if (responseDigest !== staged.response_sha256) throw new Error("HIL staged PDF hash mismatch");
      if (staged.provenance_manifest.response_sha256 !== responseDigest) throw new Error("HIL provenance response hash mismatch");
      var binding = {
        schema: "stegverse.hil.intr_payload_binding/v1",
        protocol: "HIL-PROTOCOL-v1.1",
        response_sha256: "sha256:" + responseDigest,
        provenance_sha256: provenanceDigest,
        primary_sha256: "sha256:" + HIL_PRIMARY_SHA256,
        prompt_sha256: "sha256:" + HIL_PROMPT_SHA256
      };
      return sha256Uri(binding).then(function (payloadDigest) {
        var requestBody = Object.assign({}, request);
        delete requestBody.request_hash;
        return sha256Uri(requestBody).then(function (requestDigest) {
          if (payloadDigest !== intent.payload_hash || payloadDigest !== request.payload_hash) throw new Error("HIL payload binding mismatch");
          if (intentDigest !== request.transport_intent_hash) throw new Error("HIL transport intent hash mismatch");
          if (requestDigest !== request.request_hash) throw new Error("HIL materialization request hash mismatch");
          var identityBasis = {
            transport_intent_hash: intentDigest,
            operation_id: intent.operation_id,
            packet_id: intent.packet_id,
            payload_hash: intent.payload_hash,
            destination: intent.destination
          };
          return sha256Uri(identityBasis).then(function (identityDigest) {
            if (request.materialization_id !== "INTR-MAT-" + identityDigest.slice(7, 31)) throw new Error("HIL materialization identity mismatch");
            return {
              request: request,
              intent: intent,
              response_sha256: responseDigest,
              provenance_sha256: provenanceDigest
            };
          });
        });
      });
    });
  }

  function getIntrOutbox() {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(INTR_OUTBOX, "readonly");
        var req = tx.objectStore(INTR_OUTBOX).getAll();
        req.onsuccess = function () {
          var rows = req.result || [];
          rows.sort(function (a, b) { return String(a.materialization_id).localeCompare(String(b.materialization_id)); });
          resolve(rows);
        };
        req.onerror = function () { reject(req.error || new Error("StegOS InTr outbox read failed")); };
        tx.oncomplete = function () { db.close(); };
      });
    });
  }

  function putIntrOutbox(entry) {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(INTR_OUTBOX, "readwrite");
        var store = tx.objectStore(INTR_OUTBOX);
        var read = store.get(entry.materialization_id);
        read.onerror = function () { reject(read.error || new Error("StegOS InTr outbox collision read failed")); };
        read.onsuccess = function () {
          if (read.result) {
            if (canonicalize(read.result) !== canonicalize(entry)) {
              tx.abort();
              reject(new Error("StegOS InTr outbox write-once collision"));
              return;
            }
            return;
          }
          store.add(entry);
        };
        tx.oncomplete = function () { db.close(); resolve(entry); };
        tx.onabort = function () { db.close(); };
        tx.onerror = function () { reject(tx.error || new Error("StegOS InTr outbox write failed")); };
      });
    });
  }

  function importPendingHilIntrToNodeOutbox() {
    return getMeta(REGISTRATION_KEY).then(function (registration) {
      if (!registration || registration.state !== "REGISTERED") throw new Error("Receipt #1 is required before HIL InTr outbox admission");
      var pendingIds = pendingHilMaterializationIds();
      return getHilStagedPackets().then(function (packets) {
        return packets.reduce(function (promise, staged) {
          return promise.then(function (results) {
            var request = staged && staged.intr_materialization_request;
            if (!request || !pendingIds[request.materialization_id]) return results;
            return validateHilMaterializationRequest(staged).then(function (validated) {
              var entryBody = {
                schema: "stegos.node_intr_outbox_entry.v1",
                state: "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY",
                node_id: registration.node_id,
                interlock_id: registration.interlock_id,
                materialization_id: validated.request.materialization_id,
                request_hash: validated.request.request_hash,
                transport_intent_hash: validated.request.transport_intent_hash,
                payload_hash: validated.request.payload_hash,
                response_sha256: validated.response_sha256,
                provenance_sha256: validated.provenance_sha256,
                destination: validated.request.destination,
                downstream_owner_ref: validated.request.downstream_owner_ref,
                materialization_request: validated.request,
                network_delivery_observed: false,
                runtime_materialization_observed: false,
                receiver_receipt_observed: false,
                tvc_receipt_observed: false,
                request_grants_execution_authority: false,
                claim_or_fence_minted: false,
                credential_authority: "TV/TVC",
                authority_effect: "NONE_LOCAL_CONTINUITY_ONLY"
              };
              entryBody[GITHUB_RUNTIME_AUTHORITY_FIELD] = "NONE";
              return sha256Uri(entryBody).then(function (digest) {
                var entry = Object.assign({}, entryBody, { outbox_entry_hash: digest });
                return putIntrOutbox(entry).then(function () {
                  results.push(entry);
                  return results;
                });
              });
            });
          });
        }, Promise.resolve([]));
      });
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

  function renderIntrOutboxStatus() {
    var node = document.getElementById("hil-intr-outbox");
    if (!node) return Promise.resolve([]);
    return getIntrOutbox().then(function (rows) {
      var pending = rows.filter(function (row) {
        return row && row.state === "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY" && row.network_delivery_observed === false;
      });
      node.textContent = pending.length ? String(pending.length) + " pending locally" : "None pending";
      return rows;
    }).catch(function (error) {
      node.textContent = "FAIL_CLOSED";
      throw error;
    });
  }

  function reconcilePendingHilIntrOutbox() {
    return getMeta(REGISTRATION_KEY).then(function (registration) {
      if (!registration || registration.state !== "REGISTERED") return [];
      return importPendingHilIntrToNodeOutbox();
    }).then(function (entries) {
      return renderIntrOutboxStatus().then(function () { return entries; });
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
      registerDevice().then(render).then(reconcilePendingHilIntrOutbox).catch(function (error) {
        button.disabled = false;
        button.textContent = "Register Device";
        document.getElementById("node-error").textContent = "FAIL_CLOSED: " + error.message;
      });
    });
    render().then(reconcilePendingHilIntrOutbox).catch(function (error) {
      document.getElementById("node-error").textContent = "FAIL_CLOSED: " + error.message;
    });
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
    validateKvReadinessIntrReceipt: validateKvReadinessIntrReceipt,
    validateKvReadinessIntrDeliveryAdmission: validateKvReadinessIntrDeliveryAdmission,
    applyAdmittedKvReadinessDelivery: applyAdmittedKvReadinessDelivery,
    validateKvReadinessBrowserState: validateKvReadinessBrowserState,
    validateHilMaterializationRequest: validateHilMaterializationRequest,
    getIntrOutbox: getIntrOutbox,
    importPendingHilIntrToNodeOutbox: importPendingHilIntrToNodeOutbox,
    reconcilePendingHilIntrOutbox: reconcilePendingHilIntrOutbox
  };
}());
