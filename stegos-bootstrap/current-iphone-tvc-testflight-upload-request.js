const PROVIDER_SCHEMA = "stegverse.tvc.app-store-connect-provider-operation-request/v1";
const PROVIDER = "APPLE_APP_STORE_CONNECT";
const CANONICAL_BUNDLE_ID = "org.stegverse.stegosmobile";
const FILE_NAME = "StegOSMobile-signed-testflight.ipa";

function fail(reason) { throw new Error(`current_iphone_tvc_testflight_upload_request:${reason}`); }
function hex(bytes) { return Array.from(new Uint8Array(bytes), (b) => b.toString(16).padStart(2, "0")).join(""); }
function canonicalize(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonicalize).join(",")}]`;
  return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalize(value[key])}`).join(",")}}`;
}
async function commitment(value) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(canonicalize(value)));
  return `sha256:${hex(digest)}`;
}

export async function buildCurrentIphoneTvcTestflightUploadRequest(signingReceipt) {
  if (signingReceipt?.schema !== "stegverse.stegos.current-iphone-ipa-signing-receipt/v1") fail("signing_receipt_schema_invalid");
  if (signingReceipt?.goal_task_id !== "STEG-BROWSER-EPHEMERAL-RUNTIME-BINDING-001") fail("goal_task_invalid");
  if (signingReceipt?.cosv_id !== "40000100100000") fail("cosv_invalid");
  if (signingReceipt?.execution_surface !== "CURRENT_USER_IPHONE") fail("execution_surface_invalid");
  if (signingReceipt?.codesign_structure_verified !== true || signingReceipt?.entitlements_verified !== true) fail("signed_ipa_verification_incomplete");
  if (signingReceipt?.private_key_destroyed !== true) fail("private_key_not_destroyed");
  if (!(signingReceipt?.signedIpa instanceof ArrayBuffer)) fail("signed_ipa_bytes_invalid");
  if (!/^sha256:[0-9a-f]{64}$/.test(signingReceipt?.signed_ipa_sha256 || "")) fail("signed_ipa_sha256_invalid");
  if (signingReceipt.signedIpa.byteLength !== signingReceipt?.tvc_upload_input?.artifact_size) fail("signed_ipa_size_mismatch");
  if (signingReceipt.tvc_upload_input?.artifact_sha256 !== signingReceipt.signed_ipa_sha256) fail("signed_ipa_commitment_mismatch");
  if (signingReceipt.tvc_upload_input?.platform !== "IOS") fail("platform_invalid");
  if (signingReceipt.tvc_upload_input?.app_store_connect_app_id !== signingReceipt.app_store_connect_app_id) fail("app_resource_id_mismatch");
  if (signingReceipt.tvc_upload_input?.app_store_connect_app_resolution_commitment !== signingReceipt.app_store_connect_app_resolution_commitment) fail("app_resolution_commitment_mismatch");
  if ((typeof signingReceipt.build_number !== "string" && typeof signingReceipt.build_number !== "number") || String(signingReceipt.build_number).length === 0) fail("build_number_invalid");

  const digestHex = signingReceipt.signed_ipa_sha256.slice("sha256:".length);
  const artifact = Object.freeze({
    artifact_ref: `artifact://stegos/current-iphone/${digestHex}/${FILE_NAME}`,
    artifact_sha256: signingReceipt.signed_ipa_sha256,
    artifact_size: signingReceipt.signedIpa.byteLength,
    file_name: FILE_NAME,
    app_id: signingReceipt.app_store_connect_app_id,
    app_resource_resolution_commitment: signingReceipt.app_store_connect_app_resolution_commitment,
    bundle_id: CANONICAL_BUNDLE_ID,
    bundle_version: String(signingReceipt.build_number),
    platform: "IOS",
  });
  const inputCommitment = await commitment(artifact);
  return Object.freeze({
    schema: PROVIDER_SCHEMA,
    provider: PROVIDER,
    credential_authority: "TV/TVC",
    credential_custody: "SKAP_SEALED_TV_TVC_OWNED",
    credential_material_export_allowed: false,
    github_actions_credential_access: false,
    consumer_credential_access: false,
    same_authenticated_session_required: true,
    request_id: `stegos-testflight-${digestHex.slice(0, 16)}`,
    provider_operation: "UPLOAD_TESTFLIGHT_BUILD",
    operation_input_commitment: inputCommitment,
    artifact,
    steps: Object.freeze([
      Object.freeze({ method: "POST", path: "/v1/buildUploads", body: null }),
      Object.freeze({ method: "POST", path: "/v1/buildUploadFiles", body: null }),
    ]),
    authority_effect: "NONE_REQUEST_MATERIALIZATION_ONLY",
  });
}
