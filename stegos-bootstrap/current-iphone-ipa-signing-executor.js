const CONTRACT_PATH = "/contracts/current-iphone-ipa-signing-executor.v1.json";
const REQUIRED_BUNDLES = Object.freeze([
  "org.stegverse.stegosmobile",
  "org.stegverse.stegosmobile.capture",
  "org.stegverse.stegosmobile.capture.broadcast",
]);
const REQUIRED_APP_GROUP = "group.org.stegverse.stegosmobile";
const APP_RESOLUTION_SCHEMA = "stegverse.tvc.app-store-connect-app-resource-resolution/v1";

function fail(reason) {
  throw new Error(`current_iphone_ipa_signer:${reason}`);
}

function hex(bytes) {
  return Array.from(new Uint8Array(bytes), (b) => b.toString(16).padStart(2, "0")).join("");
}

async function sha256Bytes(bytes) {
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return `sha256:${hex(digest)}`;
}

async function sha256Json(value) {
  const bytes = new TextEncoder().encode(JSON.stringify(value));
  return sha256Bytes(bytes.buffer);
}

function exactKeys(value, required) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return false;
  const actual = Object.keys(value).sort();
  return JSON.stringify(actual) === JSON.stringify([...required].sort());
}

function validateContract(contract) {
  if (contract?.schema !== "stegverse.stegos.current-iphone-ipa-signing-executor-contract/v1") fail("contract_schema_invalid");
  if (contract?.goal_task_id !== "STEG-BROWSER-EPHEMERAL-RUNTIME-BINDING-001") fail("task_invalid");
  if (contract?.cosv_id !== "40000100100000") fail("cosv_invalid");
  if (contract?.execution_surface !== "CURRENT_USER_IPHONE") fail("surface_invalid");
  if (contract?.executor_class !== "SAME_DEVICE_BROWSER_WASM_IPA_SIGNER") fail("executor_class_invalid");
  if (contract?.external_machine_required !== false) fail("external_machine_forbidden");
  if (contract?.second_user_operated_machine_allowed !== false) fail("second_machine_forbidden");
  if (contract?.github_actions_execution_allowed !== false) fail("github_execution_forbidden");
  if (contract?.credential_authority !== "TV/TVC") fail("credential_authority_invalid");
  if (contract?.app_store_connect_credential_custody !== "SKAP_SEALED_TV_TVC_OWNED") fail("credential_custody_invalid");
  if (contract?.canonical_app_bundle_id !== REQUIRED_BUNDLES[0]) fail("canonical_app_bundle_invalid");
  const key = contract?.signing_private_key;
  if (key?.origin !== "CURRENT_IPHONE_EPHEMERAL_SESSION") fail("signing_key_origin_invalid");
  for (const field of ["persistence_allowed", "repository_export_allowed", "network_export_allowed", "artifact_export_allowed", "retention_after_terminal_state_allowed"]) {
    if (key?.[field] !== false) fail(`signing_key_${field}_must_be_false`);
  }
  if (JSON.stringify(contract?.required_bundle_ids) !== JSON.stringify(REQUIRED_BUNDLES)) fail("bundle_ids_invalid");
  if (contract?.required_shared_app_group !== REQUIRED_APP_GROUP) fail("app_group_invalid");
  return contract;
}

async function loadContract(fetchImpl = fetch) {
  const response = await fetchImpl(CONTRACT_PATH, { cache: "no-store", credentials: "same-origin" });
  if (!response.ok) fail("contract_unavailable");
  return validateContract(await response.json());
}

async function verifyUnsignedInput(request) {
  if (!exactKeys(request, ["unsignedIpa", "unsignedIpaSha256", "sourceCommit", "buildNumber", "tvcAppResourceClient", "tvcProvisioningClient", "signingEngine"])) fail("request_shape_invalid");
  if (!(request.unsignedIpa instanceof ArrayBuffer)) fail("unsigned_ipa_bytes_invalid");
  if (!/^sha256:[0-9a-f]{64}$/.test(request.unsignedIpaSha256)) fail("unsigned_ipa_commitment_invalid");
  if (!request.sourceCommit || !request.buildNumber) fail("request_binding_missing");
  if (typeof request.tvcAppResourceClient !== "function") fail("tvc_app_resource_client_missing");
  const actual = await sha256Bytes(request.unsignedIpa);
  if (actual !== request.unsignedIpaSha256) fail("unsigned_ipa_hash_mismatch");
  return actual;
}

function validateAppResourceResolution(value) {
  if (value?.schema !== APP_RESOLUTION_SCHEMA) fail("app_resource_resolution_schema_invalid");
  if (value?.state !== "APP_RESOURCE_ID_RESOLVED") fail("app_resource_resolution_state_invalid");
  if (value?.provider !== "APPLE_APP_STORE_CONNECT") fail("app_resource_provider_invalid");
  if (value?.bundle_id !== REQUIRED_BUNDLES[0]) fail("app_resource_bundle_invalid");
  if (value?.provider_operation !== "RESOLVE_APP_RESOURCE_ID") fail("app_resource_operation_invalid");
  if (value?.credential_authority !== "TV/TVC") fail("app_resource_credential_authority_invalid");
  if (value?.credential_material_exported !== false) fail("app_resource_credential_export_detected");
  if (value?.github_actions_credential_access !== false) fail("app_resource_github_credential_access_invalid");
  if (value?.consumer_credential_access !== false) fail("app_resource_consumer_credential_access_invalid");
  if (value?.authority_effect !== "NONE_RESOURCE_DISCOVERY_ONLY") fail("app_resource_authority_effect_invalid");
  if (typeof value?.app_store_connect_app_id !== "string" || !value.app_store_connect_app_id.trim()) fail("app_resource_id_invalid");
  if (typeof value?.provider_result_commitment !== "string" || !/^sha256:[0-9a-f]{64}$/.test(value.provider_result_commitment)) fail("app_resource_commitment_invalid");
  return value;
}

function validateTvcProvisioningResult(value) {
  if (value?.credential_authority !== "TV/TVC") fail("tvc_credential_authority_invalid");
  if (value?.credential_custody !== "SKAP_SEALED_TV_TVC_OWNED") fail("tvc_credential_custody_invalid");
  if (value?.credential_material_exported !== false) fail("tvc_credential_export_detected");
  if (value?.github_actions_credential_access !== false) fail("tvc_github_credential_access_invalid");
  if (value?.consumer_credential_access !== false) fail("tvc_consumer_credential_access_invalid");
  const profiles = value?.profiles;
  if (!profiles || !exactKeys(profiles, ["app", "control", "broadcast"])) fail("tvc_profiles_shape_invalid");
  for (const role of ["app", "control", "broadcast"]) {
    const p = profiles[role];
    if (p?.bundle_id !== REQUIRED_BUNDLES[["app", "control", "broadcast"].indexOf(role)]) fail(`profile_${role}_bundle_invalid`);
    if (p?.shared_app_group !== REQUIRED_APP_GROUP) fail(`profile_${role}_app_group_invalid`);
    if (!(p?.mobileprovision_bytes instanceof ArrayBuffer)) fail(`profile_${role}_bytes_invalid`);
  }
  if (!(value?.certificate_bytes instanceof ArrayBuffer)) fail("certificate_bytes_invalid");
  return value;
}

function validateSigningEngine(engine) {
  for (const method of ["generateEphemeralKeyAndCsr", "signIpa", "verifySignedIpa", "destroyEphemeralKey"]) {
    if (typeof engine?.[method] !== "function") fail(`signer_method_missing:${method}`);
  }
  if (engine?.referenceImplementationImported === true) fail("unverified_reference_signer_imported");
  return engine;
}

export async function executeCurrentIphoneIpaSigning(request, { fetchImpl = fetch } = {}) {
  const contract = await loadContract(fetchImpl);
  await verifyUnsignedInput(request);
  const appResolution = validateAppResourceResolution(await request.tvcAppResourceClient({
    provider: "APPLE_APP_STORE_CONNECT",
    providerOperation: "RESOLVE_APP_RESOURCE_ID",
    bundleId: REQUIRED_BUNDLES[0],
    credentialAuthority: "TV/TVC",
    credentialCustody: "SKAP_SEALED_TV_TVC_OWNED",
    authorityEffect: "NONE_RESOURCE_DISCOVERY_REQUEST_ONLY",
  }));
  const appResolutionCommitment = await sha256Json({
    schema: appResolution.schema,
    state: appResolution.state,
    provider: appResolution.provider,
    bundle_id: appResolution.bundle_id,
    app_store_connect_app_id: appResolution.app_store_connect_app_id,
    provider_operation: appResolution.provider_operation,
    provider_result_commitment: appResolution.provider_result_commitment,
    authority_effect: appResolution.authority_effect,
  });
  const engine = validateSigningEngine(request.signingEngine);
  let keyHandle = null;
  let destroyed = false;
  try {
    const keyAndCsr = await engine.generateEphemeralKeyAndCsr({ extractable: false, persistence: false });
    keyHandle = keyAndCsr?.keyHandle;
    if (!keyHandle) fail("ephemeral_key_missing");
    if (!(keyAndCsr?.csrBytes instanceof ArrayBuffer)) fail("csr_bytes_invalid");

    const provisioning = validateTvcProvisioningResult(await request.tvcProvisioningClient({
      csrBytes: keyAndCsr.csrBytes,
      bundleIds: REQUIRED_BUNDLES,
      sharedAppGroup: REQUIRED_APP_GROUP,
      sourceCommit: request.sourceCommit,
      buildNumber: request.buildNumber,
      appStoreConnectAppId: appResolution.app_store_connect_app_id,
      appStoreConnectAppResolutionCommitment: appResolutionCommitment,
    }));

    const certificateCommitment = await sha256Bytes(provisioning.certificate_bytes);
    const profileCommitments = {};
    for (const role of ["app", "control", "broadcast"]) {
      profileCommitments[role] = await sha256Bytes(provisioning.profiles[role].mobileprovision_bytes);
    }

    const signedIpa = await engine.signIpa({
      unsignedIpa: request.unsignedIpa,
      keyHandle,
      certificateBytes: provisioning.certificate_bytes,
      profiles: provisioning.profiles,
      bundleIds: REQUIRED_BUNDLES,
      sharedAppGroup: REQUIRED_APP_GROUP,
    });
    if (!(signedIpa instanceof ArrayBuffer)) fail("signed_ipa_bytes_invalid");

    const verification = await engine.verifySignedIpa({
      signedIpa,
      keyHandle,
      bundleIds: REQUIRED_BUNDLES,
      sharedAppGroup: REQUIRED_APP_GROUP,
    });
    if (verification?.codesign_structure_verified !== true) fail("codesign_structure_not_verified");
    if (verification?.entitlements_verified !== true) fail("entitlements_not_verified");
    const signedSha = await sha256Bytes(signedIpa);

    const tvcUploadInput = {
      app_store_connect_app_id: appResolution.app_store_connect_app_id,
      app_store_connect_app_resolution_commitment: appResolutionCommitment,
      artifact_sha256: signedSha,
      artifact_size: signedIpa.byteLength,
      platform: "IOS",
    };
    const tvcUploadRequestCommitment = await sha256Json(tvcUploadInput);

    await engine.destroyEphemeralKey(keyHandle);
    destroyed = true;
    keyHandle = null;

    return {
      schema: "stegverse.stegos.current-iphone-ipa-signing-receipt/v1",
      goal_task_id: contract.goal_task_id,
      cosv_id: contract.cosv_id,
      execution_surface: "CURRENT_USER_IPHONE",
      source_commit: request.sourceCommit,
      build_number: request.buildNumber,
      app_store_connect_app_id: appResolution.app_store_connect_app_id,
      app_store_connect_app_resolution_commitment: appResolutionCommitment,
      unsigned_ipa_sha256: request.unsignedIpaSha256,
      signed_ipa_sha256: signedSha,
      bundle_ids: REQUIRED_BUNDLES,
      shared_app_group: REQUIRED_APP_GROUP,
      certificate_commitment: certificateCommitment,
      profile_commitments: profileCommitments,
      codesign_structure_verified: true,
      entitlements_verified: true,
      private_key_destroyed: true,
      signedIpa,
      tvc_upload_input: tvcUploadInput,
      tvc_upload_request_commitment: tvcUploadRequestCommitment,
      authority_effect: "NONE_EVIDENCE_ONLY",
    };
  } finally {
    if (keyHandle && !destroyed) {
      try { await engine.destroyEphemeralKey(keyHandle); } catch (_) {}
    }
  }
}

export { loadContract, validateContract, validateAppResourceResolution, validateTvcProvisioningResult };
