import initWasm, * as wasmModule from "./stegos_current_iphone_ipa_signer.js";

const EXPECTED_WASM_SHA256 = "699dc3054788d779ba7920e332c661ef7eac001156f93ab7b1fe1b64ee5a4b93";
const EXPECTED_WASM_BYTES = 2277815;
const DEFAULT_WASM_URL = new URL("./stegos_current_iphone_ipa_signer_bg.wasm", import.meta.url).toString();

function fail(reason) {
  throw new Error(`current_iphone_wasm_materializer:${reason}`);
}

function hex(bytes) {
  return Array.from(bytes, (value) => value.toString(16).padStart(2, "0")).join("");
}

async function sha256(bytes) {
  return hex(new Uint8Array(await crypto.subtle.digest("SHA-256", bytes)));
}

export async function loadValidatedCurrentIphoneWasmModule({
  fetchImpl = fetch,
  wasmUrl = DEFAULT_WASM_URL,
} = {}) {
  const response = await fetchImpl(wasmUrl, {
    method: "GET",
    credentials: "omit",
    cache: "no-store",
  });
  if (!response || response.ok !== true) fail("wasm_fetch_failed");

  const bytes = await response.arrayBuffer();
  if (bytes.byteLength !== EXPECTED_WASM_BYTES) fail("wasm_size_mismatch");
  if (await sha256(bytes) !== EXPECTED_WASM_SHA256) fail("wasm_sha256_mismatch");

  await initWasm({ module_or_path: bytes });
  if (typeof wasmModule.StegOsSigningSession !== "function") {
    fail("signing_session_constructor_missing_after_init");
  }
  return wasmModule;
}

export const CURRENT_IPHONE_WASM_STATIC_EVIDENCE = Object.freeze({
  schema: "stegos.current-iphone-wasm-static-evidence.v1",
  wasm_sha256: EXPECTED_WASM_SHA256,
  wasm_bytes: EXPECTED_WASM_BYTES,
  source_workflow_run: 34394101439,
  source_artifact_id: 10120870613,
  artifact_authority_effect: "NONE_STATIC_SOURCE_ONLY",
  credential_authority: "TV/TVC",
  github_actions_runtime_authority: false,
});
