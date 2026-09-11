import { loadValidatedCurrentIphoneUnsignedIpa } from "./current-iphone-unsigned-ipa-materializer.js";
import { executeCurrentIphoneTestflightSigning } from "./current-iphone-testflight-signing-action.js";
import { validateKvBoundEphemeralProjectionContext } from "./kv-bound-ephemeral-projection-context.js";

export async function executeStaticCurrentIphoneTestflightBootstrap({
  fetchImpl = fetch,
  tvcProviderRoute,
  projectionContext,
} = {}) {
  const projection = validateKvBoundEphemeralProjectionContext(projectionContext);
  const source = await loadValidatedCurrentIphoneUnsignedIpa({ fetchImpl });
  const signing = await executeCurrentIphoneTestflightSigning({
    unsignedIpa: source.unsignedIpa,
    unsignedIpaSha256: source.unsignedIpaSha256,
    sourceCommit: source.sourceCommit,
    buildNumber: source.buildNumber,
    fetchImpl,
    tvcProviderRoute,
  });
  return Object.freeze({
    schema: "stegos.current-iphone-testflight-static-bootstrap-result/v1",
    state: "SIGNED_IPA_VERIFIED_AWAITING_TVC_NATIVE_BUILD_UPLOAD",
    source_manifest: source.manifest,
    projection_context: projection,
    signing_receipt: signing,
    signedIpa: signing.signedIpa,
    authority_effect: "NONE_USER_INITIATED_BOOTSTRAP_EVIDENCE_ONLY",
  });
}
