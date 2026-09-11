import { executeCurrentIphoneIpaSigning } from "./current-iphone-ipa-signing-executor.js";
import { createCurrentIphoneWasmSigningEngine } from "./current-iphone-wasm-signing-engine.js";
import { createCurrentIphoneTvcProviderClients } from "./current-iphone-tvc-provider-client.js";
import { loadValidatedCurrentIphoneWasmModule } from "./current-iphone-wasm-materializer.js";

function fail(reason) { throw new Error(`current_iphone_testflight_signing_action:${reason}`); }

export async function executeCurrentIphoneTestflightSigning({
  unsignedIpa,
  unsignedIpaSha256,
  sourceCommit,
  buildNumber,
  wasmModule,
  fetchImpl = fetch,
  tvcProviderRoute,
} = {}) {
  if (!(unsignedIpa instanceof ArrayBuffer)) fail("unsigned_ipa_required");
  if (!/^sha256:[0-9a-f]{64}$/.test(unsignedIpaSha256 || "")) fail("unsigned_ipa_sha256_invalid");
  if (typeof sourceCommit !== "string" || !sourceCommit) fail("source_commit_required");
  if ((typeof buildNumber !== "string" && typeof buildNumber !== "number") || String(buildNumber).length === 0) fail("build_number_required");

  const resolvedWasmModule = wasmModule || await loadValidatedCurrentIphoneWasmModule({ fetchImpl });
  if (!resolvedWasmModule || typeof resolvedWasmModule !== "object") fail("wasm_module_required");

  const signingEngine = createCurrentIphoneWasmSigningEngine(resolvedWasmModule);
  const clients = createCurrentIphoneTvcProviderClients({ fetchImpl, route: tvcProviderRoute });

  return executeCurrentIphoneIpaSigning({
    unsignedIpa,
    unsignedIpaSha256,
    sourceCommit,
    buildNumber: String(buildNumber),
    tvcAppResourceClient: clients.tvcAppResourceClient,
    tvcProvisioningClient: clients.tvcProvisioningClient,
    signingEngine,
  }, { fetchImpl });
}

export const CURRENT_IPHONE_TESTFLIGHT_SIGNING_ROUTE = "external-provider-operation -> TVC:ProviderOperationBroker -> https://tvc.stegverse.org/v1/provider-operation";
