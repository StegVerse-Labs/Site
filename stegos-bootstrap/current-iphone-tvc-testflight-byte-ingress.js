import { TVC_PROVIDER_ROUTE } from "./current-iphone-tvc-provider-client.js";

const RESULT_SCHEMA = "stegverse.tvc.app-store-connect-build-upload-result/v1";
const RECEIPT_SCHEMA = "stegverse.tvc.current-iphone-testflight-byte-ingress-receipt/v1";

function fail(reason) { throw new Error(`current_iphone_tvc_testflight_byte_ingress:${reason}`); }

function byteIngressRoute(providerRoute = TVC_PROVIDER_ROUTE) {
  if (typeof providerRoute !== "string" || !providerRoute.endsWith("/v1/provider-operation")) fail("provider_route_invalid");
  return `${providerRoute}/testflight-byte-ingress`;
}

function descriptorHeader(value) {
  const json = JSON.stringify(value);
  const bytes = new TextEncoder().encode(json);
  let binary = "";
  const stride = 0x8000;
  for (let offset = 0; offset < bytes.length; offset += stride) {
    binary += String.fromCharCode(...bytes.subarray(offset, offset + stride));
  }
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}

function validateResult(value, request) {
  if (value?.schema !== RESULT_SCHEMA) fail("result_schema_invalid");
  if (value?.artifact_sha256 !== request?.artifact?.artifact_sha256) fail("result_artifact_sha256_mismatch");
  if (value?.artifact_size !== request?.artifact?.artifact_size) fail("result_artifact_size_mismatch");
  if (typeof value?.build_upload_id !== "string" || !value.build_upload_id) fail("build_upload_id_invalid");
  if (typeof value?.build_upload_file_id !== "string" || !value.build_upload_file_id) fail("build_upload_file_id_invalid");
  const receipt = value?.tvc_byte_ingress_receipt;
  if (receipt?.schema !== RECEIPT_SCHEMA) fail("byte_ingress_receipt_schema_invalid");
  if (receipt?.request_id !== request.request_id) fail("byte_ingress_receipt_request_id_mismatch");
  if (receipt?.artifact_sha256 !== request.artifact.artifact_sha256 || receipt?.artifact_size !== request.artifact.artifact_size) fail("byte_ingress_receipt_artifact_mismatch");
  if (receipt?.artifact_persisted_by_tvc !== false) fail("byte_ingress_artifact_persistence_invalid");
  if (receipt?.credential_material_exported !== false || receipt?.consumer_credential_access !== false || receipt?.github_actions_credential_access !== false) fail("byte_ingress_credential_boundary_invalid");
  return value;
}

export async function executeCurrentIphoneTvcTestflightByteIngress({
  uploadRequest,
  signedIpa,
  fetchImpl = fetch,
  providerRoute = TVC_PROVIDER_ROUTE,
} = {}) {
  if (uploadRequest?.schema !== "stegverse.tvc.app-store-connect-provider-operation-request/v1") fail("upload_request_schema_invalid");
  if (uploadRequest?.provider_operation !== "UPLOAD_TESTFLIGHT_BUILD") fail("upload_request_operation_invalid");
  if (!(signedIpa instanceof ArrayBuffer)) fail("signed_ipa_bytes_invalid");
  if (signedIpa.byteLength !== uploadRequest?.artifact?.artifact_size) fail("signed_ipa_size_mismatch");
  const response = await fetchImpl(byteIngressRoute(providerRoute), {
    method: "POST",
    mode: "cors",
    cache: "no-store",
    credentials: "omit",
    redirect: "error",
    headers: {
      "content-type": "application/octet-stream",
      "accept": "application/json",
      "x-stegverse-provider-request": descriptorHeader(uploadRequest),
    },
    body: signedIpa,
  });
  if (!response.ok) {
    let detail = `http_${response.status}`;
    try { const body = await response.json(); if (typeof body?.detail === "string" && body.detail) detail = body.detail; } catch (_) {}
    fail(detail);
  }
  return validateResult(await response.json(), uploadRequest);
}

export { byteIngressRoute, descriptorHeader, validateResult };
