function fail(reason) {
  throw new Error(`current_iphone_wasm_signer:${reason}`);
}

function toArrayBuffer(bytes) {
  if (bytes instanceof ArrayBuffer) return bytes;
  if (ArrayBuffer.isView(bytes)) {
    return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
  }
  fail("wasm_bytes_invalid");
}

function toUint8Array(bytes, label) {
  if (bytes instanceof ArrayBuffer) return new Uint8Array(bytes);
  if (ArrayBuffer.isView(bytes)) return new Uint8Array(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  fail(`${label}_invalid`);
}

function profileBytes(profiles, role) {
  const value = profiles?.[role]?.mobileprovision_bytes;
  return toUint8Array(value, `profile_${role}_bytes`);
}

export function createCurrentIphoneWasmSigningEngine(wasmModule) {
  const Session = wasmModule?.StegOsSigningSession;
  if (typeof Session !== "function") fail("wasm_session_constructor_missing");

  const sessions = new Map();

  function lookup(handle) {
    const session = sessions.get(handle);
    if (!session) fail("key_handle_unknown");
    return session;
  }

  return Object.freeze({
    referenceImplementationImported: false,

    async generateEphemeralKeyAndCsr(options = {}) {
      if (options.extractable !== false || options.persistence !== false) {
        fail("ephemeral_key_policy_invalid");
      }
      const session = new Session();
      const handle = crypto.randomUUID();
      try {
        const csr = session.csr_der("StegOS Current iPhone Signing");
        const csrBytes = toArrayBuffer(csr);
        if (csrBytes.byteLength === 0) fail("csr_empty");
        sessions.set(handle, session);
        return { keyHandle: handle, csrBytes };
      } catch (error) {
        try { session.destroy(); } catch (_) {}
        throw error;
      }
    },

    async signIpa({ unsignedIpa, keyHandle, certificateBytes, profiles, bundleIds, sharedAppGroup }) {
      if (!Array.isArray(bundleIds) || bundleIds.length !== 3) fail("bundle_ids_invalid");
      if (sharedAppGroup !== "group.org.stegverse.stegosmobile") fail("app_group_invalid");
      const session = lookup(keyHandle);
      session.bind_certificate(toUint8Array(certificateBytes, "certificate_bytes"));
      const signed = session.sign_ipa(
        toUint8Array(unsignedIpa, "unsigned_ipa"),
        profileBytes(profiles, "app"),
        profileBytes(profiles, "control"),
        profileBytes(profiles, "broadcast"),
      );
      return toArrayBuffer(signed);
    },

    async verifySignedIpa({ signedIpa, keyHandle, bundleIds, sharedAppGroup }) {
      if (!Array.isArray(bundleIds) || bundleIds.length !== 3) fail("verify_bundle_ids_invalid");
      if (sharedAppGroup !== "group.org.stegverse.stegosmobile") fail("verify_app_group_invalid");
      const session = lookup(keyHandle);
      const verified = session.verify_ipa(toUint8Array(signedIpa, "signed_ipa"));
      if (verified !== true) fail("wasm_signed_ipa_verification_failed");
      return {
        codesign_structure_verified: true,
        entitlements_verified: true,
      };
    },

    async destroyEphemeralKey(keyHandle) {
      const session = lookup(keyHandle);
      sessions.delete(keyHandle);
      session.destroy();
      if (session.is_destroyed() !== true) fail("key_destroy_failed");
    },
  });
}
