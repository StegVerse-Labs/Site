"use strict";
// Synthetic source-only behavior tests. No native authority, physical media or custody.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const source = fs.readFileSync("assets/auri-live-site-controls.js", "utf8");
const sandbox = { window: {} };
vm.runInNewContext(source, sandbox);
const api = sandbox.window.StegVerseAuriSiteControls;

const SCOPES = {
  live_audio: ["audio_capture"],
  live_video: ["video_capture"],
  live_audio_video: ["audio_capture", "video_capture"]
};
const session = "fixture-kv-session";
const predecessor = "fixture-immediate-org-predecessor";
function candidate(mode, sid = session) {
  return {
    candidate_disposition: "CANDIDATE_ALLOW_REQUIRES_REAL_RUNTIME_DISPOSITION",
    manifest_candidate: {
      schema: "stegverse.auri.live-mode-manifest-candidate/v1",
      capability_profile_schema: "stegverse.kv.auri-peripheral-capability-profiles/v1",
      session_id: sid,
      requested_mode: mode,
      capture_scopes: SCOPES[mode],
      predecessor_event_ref: predecessor
    }
  };
}
function setup(overrides = {}) {
  const calls = { capture: 0, factory: 0, authorization: 0, verification: 0, stop: 0, mute: 0, videoOff: 0 };
  const native = Object.assign({
    getVerifiedKvSession: async () => ({
      kv_skap_verified: true,
      relationship_current: true,
      session_id: session,
      predecessor_event_ref: predecessor
    }),
    proposeCurrentScopedManifest: async (mode) => candidate(mode),
    submitThroughExistingUniversalInTr: async () => { calls.authorization++; return { fixture: true }; },
    independentlyVerifyOrganizationAndMasterRecords: async () => { calls.verification++; return { fixture: true }; },
    platformGetUserMedia: async () => { calls.capture++; return { getTracks: () => [] }; }
  }, overrides);
  const factory = { create(opts) {
    calls.factory++;
    return {
      begin: async (mode, manifest) => {
        assert.equal(manifest.requested_mode, mode);
        assert.equal(opts.sessionId, session);
        await opts.authorize(manifest);
        await opts.verifyAuthenticAdmission({ fixture: true }, manifest);
        return { state: "SYNTHETIC_SOURCE_ONLY", mode };
      },
      mute: () => { calls.mute++; },
      videoOff: () => { calls.videoOff++; },
      stop: () => { calls.stop++; }
    };
  }};
  return { calls, native, factory };
}
async function main() {
  let result = api.create();
  assert.equal((await result.begin("live_audio")).state, "NATIVE_VERIFIED_ADMISSION_NOT_INSTALLED");
  assert.equal(result.snapshot().session_id, null);
  assert.equal(result.mute().state, "MICROPHONE_STOP_REQUESTED");

  for (const mode of Object.keys(SCOPES)) {
    const { native, factory, calls } = setup();
    const ctrl = api.create({nativeOwner:native, mediaFactory:factory});
    const response = await ctrl.begin(mode);
    assert.equal(response.state, "SYNTHETIC_SOURCE_ONLY");
    assert.equal(response.mode, mode);
    assert.equal(ctrl.snapshot().session_id, session);
    assert.equal(calls.factory, 1);
    assert.equal(calls.authorization, 1);
    assert.equal(calls.verification, 1);
    assert.equal(calls.capture, 0, "the UI adapter itself must not activate hardware");
    ctrl.mute(); ctrl.videoOff(); ctrl.stop();
    assert.deepEqual([calls.mute,calls.videoOff,calls.stop],[1,1,1]);
  }

  {
    const { native, factory, calls } = setup({
      getVerifiedKvSession: async () => ({
        kv_skap_verified:false, relationship_current:true,
        session_id:session, predecessor_event_ref:predecessor
      })
    });
    const ctrl = api.create({nativeOwner:native,mediaFactory:factory});
    assert.equal((await ctrl.begin("live_audio")).state,"CURRENT_KV_SKAP_AND_PREDECESSOR_REQUIRED");
    assert.equal(calls.factory,0);
  }
  {
    const { native, factory, calls } = setup({
      proposeCurrentScopedManifest:async () => candidate("live_video")
    });
    const ctrl = api.create({nativeOwner:native,mediaFactory:factory});
    assert.equal((await ctrl.begin("live_audio")).state,"CURRENT_SCOPED_MANIFEST_UNAVAILABLE");
    assert.equal(calls.factory,0);
  }
  {
    let release;
    const delayed = new Promise(resolve => {release=resolve;});
    const { native, factory, calls } = setup({
      getVerifiedKvSession: () => delayed
    });
    const ctrl = api.create({nativeOwner:native,mediaFactory:factory});
    const pending = ctrl.begin("live_audio");
    ctrl.stop(); 
    release({kv_skap_verified:true,relationship_current:true,session_id:session,predecessor_event_ref:predecessor});
    assert.equal((await pending).state,"CANCELLED");
    assert.equal(calls.factory,0);
  }
  {
    const { native, factory, calls } = setup();
    const ctrl = api.create({nativeOwner:native,mediaFactory:factory});
    assert.equal((await ctrl.begin("live_audio")).state,"SYNTHETIC_SOURCE_ONLY");
    native.getVerifiedKvSession=async ()=>({
      kv_skap_verified:true,relationship_current:true,session_id:"other-session",
      predecessor_event_ref:predecessor
    });
    assert.equal((await ctrl.begin("live_video")).state,"KV_SESSION_CONTINUITY_MISMATCH");
    assert.equal(calls.stop,1);
    assert.equal(calls.factory,1);
  }
  {
    const elements={};
    function el(tag){
      return {tag,children:[],attributes:{},setAttribute(k,v){this.attributes[k]=v;},
        addEventListener(k,f){this[k]=f;},appendChild(child){this.children.push(child);if(child.id)elements[child.id]=child;}};
    }
    const form=el("form"),log=el("div");
    const doc={getElementById(id){return elements[id]||null;},createElement:el};
    elements.chatForm=form;elements.chatLog=log;
    const mounted=api.mount({document:doc});
    assert.equal(mounted.group.children.length,6);
    assert.equal(mounted.group.children.filter(x=>x.disabled===true).length,3);
    assert.equal(mounted.status.attributes.role,"status");
    assert.equal(api.mount({document:doc}).state,"EXISTING_CONTROLS_PRESERVED");
  }
  console.log("AURI_SITE_UI_SOURCE_TESTS_PASS: 3 modes, no-authority, wrong-consent, wrong-scope, cancellation, session continuity, direct stop, accessible singleton controls");
}
main().catch(e=>{console.error(e);process.exit(1);});
