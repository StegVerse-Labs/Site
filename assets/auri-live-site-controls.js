"use strict";
/* Site #239 candidate, not machine-admitted or deployed. No second chat shell.
 * The existing native owner must supply the real SDK / Universal InTr client,
 * authenticated organization + Master Records readback, and KV/SKAP session.
 * JavaScript function objects alone are not trusted authority.
 */
(function (root) {
  var MODES = [
    ["live_audio", "Audio"], ["live_video", "Video"], ["live_audio_video", "Audio + video"]
  ];
  var MANIFEST = "stegverse.auri.live-mode-manifest-candidate/v1";
  var PROFILES = "stegverse.kv.auri-peripheral-capability-profiles/v1";
  var SCOPES = {
    live_audio: ["audio_capture"],
    live_video: ["video_capture"],
    live_audio_video: ["audio_capture", "video_capture"]
  };

  function create(options) {
    options = options || {};
    var native = options.nativeOwner || null;
    var mediaFactory = options.mediaFactory || null;
    var notify = options.onLocalState || function () {};
    var controller = null;
    var session = null;
    var epoch = 0;

    function report(state, detail) {
      var value = {
        schema: "stegverse.site.auri-ui-local-observation/v1",
        evidence_class: "SOURCE_ONLY_LOCAL_UI",
        state: state, detail: detail || null,
        authentic_transition_receipt: false,
        master_records_reconstruction: false
      };
      notify(value);
      return value;
    }
    function nativeReady() {
      return !!native && !!mediaFactory &&
        typeof mediaFactory.create === "function" &&
        typeof native.getVerifiedKvSession === "function" &&
        typeof native.proposeCurrentScopedManifest === "function" &&
        typeof native.submitThroughExistingUniversalInTr === "function" &&
        typeof native.independentlyVerifyOrganizationAndMasterRecords === "function" &&
        typeof native.platformGetUserMedia === "function";
    }
    function direct(command) {
      epoch++;
      if (controller) {
        if (command === "mute") { controller.mute(); }
        else if (command === "video_off") { controller.videoOff(); }
        else { controller.stop(); }
      }
      return report(command === "mute" ? "MICROPHONE_STOP_REQUESTED" :
        command === "video_off" ? "CAMERA_STOP_REQUESTED" : "STOP_REQUESTED", null);
    }
    async function begin(mode) {
      if (!Object.prototype.hasOwnProperty.call(SCOPES, mode)) {
        return report("UNSUPPORTED_MODE", null);
      }
      // No promise of actual admission, capture, hardware support, or deployment.
      if (!nativeReady()) {
        return report("NATIVE_VERIFIED_ADMISSION_NOT_INSTALLED", null);
      }
      var thisEpoch = ++epoch;
      try {
        // This is a fresh KV/SKAP read, never an inferred device-ID login.
        var context = await native.getVerifiedKvSession();
        if (thisEpoch !== epoch) { return report("CANCELLED", null); }
        if (!context || context.kv_skap_verified !== true ||
            context.relationship_current !== true ||
            typeof context.session_id !== "string" || !context.session_id ||
            typeof context.predecessor_event_ref !== "string" ||
            !context.predecessor_event_ref) {
          return report("CURRENT_KV_SKAP_AND_PREDECESSOR_REQUIRED", null);
        }
        if (session !== null && session !== context.session_id) {
          if (controller) { controller.stop(); controller = null; }
          return report("KV_SESSION_CONTINUITY_MISMATCH", null);
        }
        var proposed = await native.proposeCurrentScopedManifest(mode, context);
        if (thisEpoch !== epoch) { return report("CANCELLED", null); }
        var manifest = proposed && proposed.manifest_candidate;
        if (!proposed ||
            proposed.candidate_disposition !== "CANDIDATE_ALLOW_REQUIRES_REAL_RUNTIME_DISPOSITION" ||
            !manifest || manifest.schema !== MANIFEST ||
            manifest.capability_profile_schema !== PROFILES ||
            manifest.session_id !== context.session_id ||
            manifest.requested_mode !== mode ||
            manifest.predecessor_event_ref !== context.predecessor_event_ref ||
            JSON.stringify(manifest.capture_scopes) !== JSON.stringify(SCOPES[mode])) {
          return report("CURRENT_SCOPED_MANIFEST_UNAVAILABLE", null);
        }
        if (session === null) { session = context.session_id; }
        if (!controller) {
          controller = mediaFactory.create({
            sessionId: session,
            authorize: function (exactManifest) {
              return native.submitThroughExistingUniversalInTr(exactManifest);
            },
            verifyAuthenticAdmission: function (result, exactManifest) {
              // This MUST be a trusted owner-controlled readback, not the SDK's
              // structural verify_receipt() or a caller-supplied boolean.
              return native.independentlyVerifyOrganizationAndMasterRecords(
                result, exactManifest
              );
            },
            getUserMedia: function (scope) {
              return native.platformGetUserMedia(scope);
            },
            onLocalState: notify
          });
        }
        return await controller.begin(mode, manifest);
      } catch (error) {
        if (thisEpoch !== epoch) { return report("CANCELLED", null); }
        return report("SOURCE_UI_NON_ALLOW", {
          reason: String(error && error.message || error)
        });
      }
    }
    return {
      begin: begin,
      mute: function () { return direct("mute"); },
      videoOff: function () { return direct("video_off"); },
      stop: function () { return direct("stop"); },
      nativeReady: nativeReady,
      snapshot: function () { return {
        session_id: session, native_installed: nativeReady(),
        local_controller_created: !!controller, authority_effect: "NONE"
      }; }
    };
  }

  function mount(options) {
    options = options || {};
    var doc = options.document || root.document;
    if (!doc || !doc.getElementById) { throw new Error("EXISTING_CHAT_DOCUMENT_REQUIRED"); }
    var composer = doc.getElementById("chatForm");
    var log = doc.getElementById("chatLog");
    if (!composer || !log) { throw new Error("EXISTING_PRIMARY_CHAT_REQUIRED"); }
    if (doc.getElementById("auri-live-controls")) {
      return { state: "EXISTING_CONTROLS_PRESERVED", authority_effect: "NONE" };
    }
    var status = doc.createElement("p");
    status.id = "auri-live-status";
    status.setAttribute("role", "status");
    status.setAttribute("aria-live", "polite");
    status.textContent = "Live modes require current MyKV/SKAP and authenticated native admission.";
    var group = doc.createElement("div");
    group.id = "auri-live-controls";
    group.setAttribute("role", "group");
    group.setAttribute("aria-label", "Auri live conversation controls");
    var actions = create(Object.assign({}, options, {
      onLocalState: function (result) {
        status.textContent = ({
          NATIVE_VERIFIED_ADMISSION_NOT_INSTALLED: "Live capture unavailable: trusted native admission is not installed.",
          CURRENT_KV_SKAP_AND_PREDECESSOR_REQUIRED: "Current MyKV/SKAP consent or predecessor evidence is unavailable.",
          CURRENT_SCOPED_MANIFEST_UNAVAILABLE: "The requested capture scope has not been admitted.",
          STOP_REQUESTED: "Stop requested immediately.",
          MICROPHONE_STOP_REQUESTED: "Microphone stop requested immediately.",
          CAMERA_STOP_REQUESTED: "Camera stop requested immediately."
        })[result.state] || result.state.replace(/_/g, " ");
        if (typeof options.onLocalState === "function") { options.onLocalState(result); }
      }
    }));
    MODES.forEach(function (entry) {
      var button = doc.createElement("button");
      button.type = "button";
      button.textContent = entry[1];
      button.disabled = !actions.nativeReady();
      button.setAttribute("data-auri-mode", entry[0]);
      button.addEventListener("click", function () { void actions.begin(entry[0]); });
      group.appendChild(button);
    });
    [["mute", "Mute"], ["videoOff", "Video off"], ["stop", "Stop"]].forEach(function (entry) {
      var button = doc.createElement("button");
      button.type = "button";
      button.textContent = entry[1];
      button.setAttribute("data-auri-direct", entry[0]);
      button.addEventListener("click", function () { actions[entry[0]](); });
      group.appendChild(button);
    });
    composer.appendChild(group);
    composer.appendChild(status);
    return { actions: actions, status: status, group: group };
  }
  root.StegVerseAuriSiteControls = { create: create, mount: mount };
}(typeof window === "object" ? window : self));
