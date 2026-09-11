const TVC_PROVIDER_ROUTE = "https://tvc.stegverse.org/v1/provider-operation";
const PROVIDER_SCHEMA = "stegverse.tvc.app-store-connect-provider-operation-request/v1";
const PROVIDER_RESULT_SCHEMA = "stegverse.tvc.app-store-connect-provider-operation-result/v1";
const APP_RESOLUTION_SCHEMA = "stegverse.tvc.app-store-connect-app-resource-resolution/v1";
const INTR_PROFILE = Object.freeze({
  profile_id: "external-provider-operation",
  request_class: "EXTERNAL_PROVIDER_OPERATION",
  payload_schema: "stegverse.external-provider.operation-request/v1",
  operation: "REQUEST_PROVIDER_OPERATION",
  source: Object.freeze({ boundary: "STEGOS_ECOSYSTEM", subsystem: "LLMAdapter:ProviderOperationClient" }),
  destination: Object.freeze({ boundary: "STEGOS_ECOSYSTEM", subsystem: "TVC:ProviderOperationBroker" }),
  authority_effect: "NONE_TRANSPORT_ONLY",
});
const BUNDLES = Object.freeze({
  app: "org.stegverse.stegosmobile",
  control: "org.stegverse.stegosmobile.capture",
  broadcast: "org.stegverse.stegosmobile.capture.broadcast",
});
const APP_GROUP = "group.org.stegverse.stegosmobile";

function fail(reason) { throw new Error(`current_iphone_tvc_provider_client:${reason}`); }
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
function randomId(prefix) { return `${prefix}-${crypto.randomUUID()}`; }
function arrayBufferToBase64(value) {
  if (!(value instanceof ArrayBuffer)) fail("array_buffer_required");
  const bytes = new Uint8Array(value);
  let binary = "";
  for (let i = 0; i < bytes.length; i += 1) binary += String.fromCharCode(bytes[i]);
  return btoa(binary);
}
function base64ToArrayBuffer(value, label) {
  if (typeof value !== "string" || !value) fail(`${label}_base64_invalid`);
  let binary;
  try { binary = atob(value); } catch (_) { fail(`${label}_base64_invalid`); }
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
  return bytes.buffer;
}
function assertSecretFreeHeaders(headers) {
  const forbidden = new Set(["authorization", "x-api-key", "x-admin-token", "x-github-token"]);
  for (const [name] of new Headers(headers || {})) {
    if (forbidden.has(name.toLowerCase())) fail(`protected_header_forbidden:${name.toLowerCase()}`);
  }
}
async function buildRequest(providerOperation, operationModel, steps, requestId = randomId("stegos-iphone-tvc")) {
  return {
    schema: PROVIDER_SCHEMA,
    provider: "APPLE_APP_STORE_CONNECT",
    credential_authority: "TV/TVC",
    credential_custody: "SKAP_SEALED_TV_TVC_OWNED",
    credential_material_export_allowed: false,
    github_actions_credential_access: false,
    consumer_credential_access: false,
    same_authenticated_session_required: true,
    request_id: requestId,
    provider_operation: providerOperation,
    operation_input_commitment: await commitment(operationModel),
    operation_model: operationModel,
    steps,
  };
}
function validateProviderResult(value, expectedOperation, expectedRequestId) {
  if (value?.schema !== PROVIDER_RESULT_SCHEMA) fail("provider_result_schema_invalid");
  if (value?.provider !== "APPLE_APP_STORE_CONNECT") fail("provider_result_provider_invalid");
  if (value?.provider_operation !== expectedOperation) fail("provider_result_operation_invalid");
  if (value?.request_id !== expectedRequestId) fail("provider_result_request_id_invalid");
  if (value?.credential_authority !== "TV/TVC") fail("provider_result_credential_authority_invalid");
  if (value?.credential_custody !== "SKAP_SEALED_TV_TVC_OWNED") fail("provider_result_credential_custody_invalid");
  if (value?.credential_material_exported !== false || value?.credential_material_logged !== false || value?.credential_material_retained !== false) fail("provider_result_credential_export_detected");
  if (value?.github_actions_credential_access !== false || value?.consumer_credential_access !== false) fail("provider_result_consumer_credential_access_detected");
  if (value?.same_authenticated_session_observed !== true) fail("provider_result_same_session_not_observed");
  if (!Array.isArray(value?.steps)) fail("provider_result_steps_invalid");
  if (!/^sha256:[0-9a-f]{64}$/.test(value?.result_commitment || "")) fail("provider_result_commitment_invalid");
  return value;
}
async function postProviderRequest(request, { fetchImpl = fetch, route = TVC_PROVIDER_ROUTE, headers = {} } = {}) {
  assertSecretFreeHeaders(headers);
  const response = await fetchImpl(route, {
    method: "POST",
    mode: "cors",
    cache: "no-store",
    credentials: "omit",
    redirect: "error",
    headers: { "content-type": "application/json", "accept": "application/json", ...headers },
    body: JSON.stringify(request),
  });
  if (!response.ok) fail(`provider_route_http_${response.status}`);
  return validateProviderResult(await response.json(), request.provider_operation, request.request_id);
}
function firstData(step, label) {
  const data = step?.body?.data;
  if (!data || Array.isArray(data) || typeof data !== "object") fail(`${label}_data_invalid`);
  return data;
}
function listData(step, label) {
  const data = step?.body?.data;
  if (!Array.isArray(data)) fail(`${label}_data_invalid`);
  return data;
}
async function resolveAppResource({ fetchImpl = fetch, route = TVC_PROVIDER_ROUTE } = {}) {
  const bundleId = BUNDLES.app;
  const model = { bundle_id: bundleId, discovery: "EXACT_CANONICAL_APP_RESOURCE" };
  const request = await buildRequest("RESOLVE_APP_RESOURCE_ID", model, [{
    method: "GET",
    path: `/v1/apps?filter%5BbundleId%5D=${encodeURIComponent(bundleId)}&limit=2`,
    body: null,
  }]);
  const result = await postProviderRequest(request, { fetchImpl, route });
  const apps = listData(result.steps[0], "app_resolution");
  if (apps.length !== 1 || apps[0]?.attributes?.bundleId !== bundleId || typeof apps[0]?.id !== "string" || !apps[0].id) fail("app_resource_resolution_not_unique");
  return {
    schema: APP_RESOLUTION_SCHEMA,
    state: "APP_RESOURCE_ID_RESOLVED",
    provider: "APPLE_APP_STORE_CONNECT",
    bundle_id: bundleId,
    app_store_connect_app_id: apps[0].id,
    provider_operation: "RESOLVE_APP_RESOURCE_ID",
    credential_authority: "TV/TVC",
    credential_material_exported: false,
    github_actions_credential_access: false,
    consumer_credential_access: false,
    provider_result_commitment: result.result_commitment,
    intr_profile: INTR_PROFILE.profile_id,
    authority_effect: "NONE_RESOURCE_DISCOVERY_ONLY",
  };
}
async function reconcileBundleIds(fetchOptions) {
  const roles = ["app", "control", "broadcast"];
  const inspect = await buildRequest("CREATE_AND_RECONCILE_PROVISIONING_RESOURCES", { bundle_ids: BUNDLES, phase: "INSPECT" }, roles.map((role) => ({
    method: "GET", path: `/v1/bundleIds?filter%5Bidentifier%5D=${encodeURIComponent(BUNDLES[role])}&limit=2`, body: null,
  })));
  let result = await postProviderRequest(inspect, fetchOptions);
  const ids = {};
  const missing = [];
  roles.forEach((role, index) => {
    const rows = listData(result.steps[index], `bundle_${role}`);
    if (rows.length === 1 && rows[0]?.attributes?.identifier === BUNDLES[role] && typeof rows[0]?.id === "string") ids[role] = rows[0].id;
    else if (rows.length === 0) missing.push(role);
    else fail(`bundle_${role}_resolution_ambiguous`);
  });
  if (missing.length) {
    const create = await buildRequest("CREATE_AND_RECONCILE_PROVISIONING_RESOURCES", { bundle_ids: BUNDLES, missing, phase: "CREATE_MISSING" }, missing.map((role) => ({
      method: "POST", path: "/v1/bundleIds", body: { data: { type: "bundleIds", attributes: { identifier: BUNDLES[role], name: `StegOS ${role}` } } },
    })));
    result = await postProviderRequest(create, fetchOptions);
    missing.forEach((role, index) => { const data = firstData(result.steps[index], `bundle_${role}_create`); if (typeof data.id !== "string" || !data.id) fail(`bundle_${role}_created_id_invalid`); ids[role] = data.id; });
  }
  return ids;
}
async function ensureAppGroupCapabilities(bundleResourceIds, fetchOptions) {
  const roles = ["app", "control", "broadcast"];
  const inspect = await buildRequest("CREATE_AND_RECONCILE_PROVISIONING_RESOURCES", { bundle_resource_ids: bundleResourceIds, app_group: APP_GROUP, phase: "CAPABILITY_INSPECT" }, roles.map((role) => ({
    method: "GET", path: `/v1/bundleIdCapabilities?filter%5BbundleId%5D=${encodeURIComponent(bundleResourceIds[role])}&limit=20`, body: null,
  })));
  const result = await postProviderRequest(inspect, fetchOptions);
  const missing = [];
  roles.forEach((role, index) => {
    const rows = listData(result.steps[index], `capability_${role}`);
    const hasAppGroups = rows.some((row) => row?.attributes?.capabilityType === "APP_GROUPS");
    if (!hasAppGroups) missing.push(role);
  });
  if (!missing.length) return;
  const enable = await buildRequest("ENABLE_APP_GROUP_CAPABILITY", { bundle_resource_ids: bundleResourceIds, app_group: APP_GROUP, missing }, missing.map((role) => ({
    method: "POST", path: "/v1/bundleIdCapabilities", body: { data: { type: "bundleIdCapabilities", attributes: { capabilityType: "APP_GROUPS" }, relationships: { bundleId: { data: { type: "bundleIds", id: bundleResourceIds[role] } } } } },
  })));
  await postProviderRequest(enable, fetchOptions);
}
async function createSigningCertificate(csrBytes, fetchOptions) {
  const csrContent = arrayBufferToBase64(csrBytes);
  const request = await buildRequest("CREATE_AND_RECONCILE_PROVISIONING_RESOURCES", { certificate_type: "IOS_DISTRIBUTION", csr_commitment: await commitment(csrContent), phase: "CERTIFICATE" }, [{
    method: "POST", path: "/v1/certificates", body: { data: { type: "certificates", attributes: { certificateType: "IOS_DISTRIBUTION", csrContent } } },
  }]);
  const result = await postProviderRequest(request, fetchOptions);
  const data = firstData(result.steps[0], "certificate");
  if (typeof data.id !== "string" || !data.id) fail("certificate_resource_id_invalid");
  return { id: data.id, bytes: base64ToArrayBuffer(data?.attributes?.certificateContent, "certificate_content") };
}
async function createProfiles(bundleResourceIds, certificateId, fetchOptions) {
  const roles = ["app", "control", "broadcast"];
  const request = await buildRequest("CREATE_AND_RECONCILE_PROVISIONING_RESOURCES", { bundle_resource_ids: bundleResourceIds, certificate_id: certificateId, profile_type: "IOS_APP_STORE", app_group: APP_GROUP, phase: "PROFILES" }, roles.map((role) => ({
    method: "POST", path: "/v1/profiles", body: { data: { type: "profiles", attributes: { name: `StegOS ephemeral ${role} ${crypto.randomUUID()}`, profileType: "IOS_APP_STORE" }, relationships: { bundleId: { data: { type: "bundleIds", id: bundleResourceIds[role] } }, certificates: { data: [{ type: "certificates", id: certificateId }] } } } },
  })));
  const result = await postProviderRequest(request, fetchOptions);
  const profiles = {};
  roles.forEach((role, index) => {
    const data = firstData(result.steps[index], `profile_${role}`);
    profiles[role] = { bundle_id: BUNDLES[role], shared_app_group: APP_GROUP, mobileprovision_bytes: base64ToArrayBuffer(data?.attributes?.profileContent, `profile_${role}_content`) };
  });
  return profiles;
}
async function provisionSigningMaterial({ csrBytes, bundleIds, sharedAppGroup }, fetchOptions) {
  if (!(csrBytes instanceof ArrayBuffer)) fail("csr_bytes_invalid");
  if (JSON.stringify(bundleIds) !== JSON.stringify([BUNDLES.app, BUNDLES.control, BUNDLES.broadcast])) fail("bundle_ids_invalid");
  if (sharedAppGroup !== APP_GROUP) fail("app_group_invalid");
  const bundleResourceIds = await reconcileBundleIds(fetchOptions);
  await ensureAppGroupCapabilities(bundleResourceIds, fetchOptions);
  const certificate = await createSigningCertificate(csrBytes, fetchOptions);
  const profiles = await createProfiles(bundleResourceIds, certificate.id, fetchOptions);
  return {
    credential_authority: "TV/TVC",
    credential_custody: "SKAP_SEALED_TV_TVC_OWNED",
    credential_material_exported: false,
    github_actions_credential_access: false,
    consumer_credential_access: false,
    certificate_bytes: certificate.bytes,
    profiles,
    intr_profile: INTR_PROFILE.profile_id,
  };
}

export function createCurrentIphoneTvcProviderClients({ fetchImpl = fetch, route = TVC_PROVIDER_ROUTE } = {}) {
  const fetchOptions = { fetchImpl, route };
  return Object.freeze({
    intrProfile: INTR_PROFILE,
    providerRoute: route,
    tvcAppResourceClient: () => resolveAppResource(fetchOptions),
    tvcProvisioningClient: (request) => provisionSigningMaterial(request, fetchOptions),
  });
}

export { TVC_PROVIDER_ROUTE, INTR_PROFILE, BUNDLES, APP_GROUP, buildRequest, postProviderRequest, validateProviderResult, resolveAppResource, provisionSigningMaterial };
