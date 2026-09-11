import { validateKvBoundEphemeralProjectionContext } from "./kv-bound-ephemeral-projection-context.js";

export async function loadKvProjectionContextFromFile(file) {
  if (!file || typeof file.text !== "function") {
    throw new Error("kv_projection_file_required");
  }
  if (file.size > 32768) {
    throw new Error("kv_projection_file_too_large");
  }
  let parsed;
  try {
    parsed = JSON.parse(await file.text());
  } catch (_) {
    throw new Error("kv_projection_file_invalid_json");
  }
  return validateKvBoundEphemeralProjectionContext(parsed);
}
