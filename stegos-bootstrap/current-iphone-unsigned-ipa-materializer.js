const IPA_URL = new URL("./StegOSMobile-unsigned-device.ipa", import.meta.url).toString();
const MANIFEST_URL = new URL("./StegOSMobile-unsigned-device-manifest.json", import.meta.url).toString();
const EXPECTED_SOURCE_COMMIT = "32115e32d701e783af2c2659a900e4bc90460fd2";
const EXPECTED_IPA_SHA256 = "sha256:557d559082bdefca5fcc69c86f342d8cc035c2d803d154de5ed45b5677f80c35";
const EXPECTED_IPA_BYTES = 389564;
const EXPECTED_BUILD_NUMBER = "1";

function fail(reason) { throw new Error(`current_iphone_unsigned_ipa_materializer:${reason}`); }
function hex(bytes) { return Array.from(bytes, (value) => value.toString(16).padStart(2, "0")).join(""); }
async function digest(bytes) { return `sha256:${hex(new Uint8Array(await crypto.subtle.digest("SHA-256", bytes)))}`; }

function validateManifest(value) {
  if (value?.schema !== "stegos.mobile-unsigned-device-package-evidence/v1") fail("manifest_schema_invalid");
  if (value?.source_commit !== EXPECTED_SOURCE_COMMIT) fail("source_commit_mismatch");
  if (value?.ipa_sha256 !== EXPECTED_IPA_SHA256) fail("manifest_ipa_sha256_mismatch");
  if (value?.execution_target !== "CURRENT_USER_IPHONE") fail("execution_target_invalid");
  if (value?.iphoneos_build !== true) fail("iphoneos_build_required");
  if (value?.signed !== false) fail("unsigned_package_required");
  if (value?.canonical_stegbrowser_resident_embedded !== true) fail("retained_node_source_missing");
  if (value?.next_required_boundary !== "TV_TVC_APPLE_SIGNING_AND_PROVISIONING") fail("next_boundary_invalid");
  return value;
}

export async function loadValidatedCurrentIphoneUnsignedIpa({ fetchImpl = fetch } = {}) {
  const [manifestResponse, ipaResponse] = await Promise.all([
    fetchImpl(MANIFEST_URL, { method: "GET", credentials: "omit", cache: "no-store" }),
    fetchImpl(IPA_URL, { method: "GET", credentials: "omit", cache: "no-store" }),
  ]);
  if (!manifestResponse?.ok) fail("manifest_fetch_failed");
  if (!ipaResponse?.ok) fail("ipa_fetch_failed");
  const manifest = validateManifest(await manifestResponse.json());
  const unsignedIpa = await ipaResponse.arrayBuffer();
  if (unsignedIpa.byteLength !== EXPECTED_IPA_BYTES) fail("ipa_size_mismatch");
  if (await digest(unsignedIpa) !== EXPECTED_IPA_SHA256) fail("ipa_sha256_mismatch");
  return Object.freeze({
    unsignedIpa,
    unsignedIpaSha256: EXPECTED_IPA_SHA256,
    sourceCommit: EXPECTED_SOURCE_COMMIT,
    buildNumber: EXPECTED_BUILD_NUMBER,
    manifest,
  });
}

export const CURRENT_IPHONE_UNSIGNED_IPA_STATIC_EVIDENCE = Object.freeze({
  schema: "stegos.current-iphone-unsigned-ipa-static-evidence/v1",
  source_commit: EXPECTED_SOURCE_COMMIT,
  workflow_run: 34390689816,
  artifact_id: 10119511850,
  ipa_sha256: EXPECTED_IPA_SHA256,
  ipa_bytes: EXPECTED_IPA_BYTES,
  build_number: EXPECTED_BUILD_NUMBER,
  authority_effect: "NONE_STATIC_SOURCE_ONLY",
  github_actions_runtime_authority: false,
  credential_authority: "TV/TVC",
});
