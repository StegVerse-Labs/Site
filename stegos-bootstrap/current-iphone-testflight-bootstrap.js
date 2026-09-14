import { loadValidatedCurrentIphoneUnsignedIpa } from "./current-iphone-unsigned-ipa-materializer.js";
import { executeCurrentIphoneTestflightSigning } from "./current-iphone-testflight-signing-action.js";
import { buildCurrentIphoneTvcTestflightUploadRequest } from "./current-iphone-tvc-testflight-upload-request.js";
import { executeCurrentIphoneTvcTestflightByteIngress } from "./current-iphone-tvc-testflight-byte-ingress.js";
import { validateKvBoundEphemeralProjectionContext } from "./kv-bound-ephemeral-projection-context.js";

function stageError(stage, error) {
  const reason = String(error && error.message ? error.message : error);
  throw new Error(`current_iphone_testflight_bootstrap:${stage}:${reason}`);
}

async function runStage(stage, fn) {
  try {
    return await fn();
  } catch (error) {
    stageError(stage, error);
  }
}

export async function executeStaticCurrentIphoneTestflightBootstrap({
  fetchImpl = fetch,
  tvcProviderRoute,
  projectionContext,
} = {}) {
  const projection = await runStage("projection_validation", async () =>
    validateKvBoundEphemeralProjectionContext(projectionContext));

  const source = await runStage("unsigned_ipa_materialization", async () =>
    loadValidatedCurrentIphoneUnsignedIpa({ fetchImpl }));

  const signing = await runStage("current_iphone_signing", async () =>
    executeCurrentIphoneTestflightSigning({
      unsignedIpa: source.unsignedIpa,
      unsignedIpaSha256: source.unsignedIpaSha256,
      sourceCommit: source.sourceCommit,
      buildNumber: source.buildNumber,
      fetchImpl,
      tvcProviderRoute,
    }));

  const tvcUploadRequest = await runStage("tvc_upload_request_build", async () =>
    buildCurrentIphoneTvcTestflightUploadRequest(signing));

  const tvcBuildUpload = await runStage("tvc_native_build_upload", async () =>
    executeCurrentIphoneTvcTestflightByteIngress({
      uploadRequest: tvcUploadRequest,
      signedIpa: signing.signedIpa,
      fetchImpl,
      providerRoute: tvcProviderRoute,
    }));

  return Object.freeze({
    schema: "stegos.current-iphone-testflight-static-bootstrap-result/v1",
    state: "TVC_NATIVE_BUILD_UPLOAD_COMMITTED",
    source_manifest: source.manifest,
    projection_context: projection,
    signing_receipt: signing,
    tvc_upload_request: tvcUploadRequest,
    tvc_build_upload: tvcBuildUpload,
    signedIpa: signing.signedIpa,
    next_required_boundary: "TESTFLIGHT_PROCESSING_INSTALL_OBSERVATION",
    authority_effect: "NONE_USER_INITIATED_BOOTSTRAP_EVIDENCE_ONLY",
  });
}
