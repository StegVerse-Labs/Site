"use strict";

/*
 * Bounded recovery shim for the existing root-scoped Universal InTr runtime.
 * It does not create another service worker, transport, authority, or execution plane.
 * It only permits replacement of the canonical installation receipt when the resident
 * slot is already occupied by a row that fails the canonical installation validator.
 */
(function(){
  var priorPersistPortable = persistPortable;

  function isCanonicalInstallationPayload(payload){
    var files = payload && Array.isArray(payload.files) ? payload.files : [];
    return payload && payload.canonical_path === "_System" && files.length === 1 && files[0] && files[0].name === "installation.receipt.json";
  }

  function sameCanonicalFile(existing,candidate){
    return !!existing &&
      existing.key === candidate.key &&
      existing.directory_id === candidate.directory_id &&
      existing.canonical_path === candidate.canonical_path &&
      existing.name === candidate.name &&
      existing.media_type === candidate.media_type &&
      existing.size_bytes === candidate.size_bytes &&
      existing.sha256 === candidate.sha256 &&
      existing.content_base64 === candidate.content_base64 &&
      existing.credential_material_present === false &&
      existing.provider_operation_authorized === false &&
      existing.authority_effect === "NONE";
  }

  persistPortable = function(req){
    var payload = req && req.portable_payload;
    if(!isCanonicalInstallationPayload(payload)) return priorPersistPortable(req);

    require(payload.schema === "stegverse.kv.portable-direct-source-inline-payload/v1", "portable_payload_invalid");
    require(payload.credential_requirement === "NONE" && payload.authority_effect === "NONE", "portable_payload_authority_invalid");

    var file = payload.files[0];
    require(typeof file.content_base64 === "string", "portable_file_content_missing");
    var bytes = base64ToBytes(file.content_base64);

    return shaUriBytes(bytes).then(function(actual){
      require(actual === file.sha256, "portable_file_sha256_mismatch");
      var key = "_System/installation.receipt.json";
      var candidate = {
        key:key,
        directory_id:payload.directory_id,
        canonical_path:payload.canonical_path,
        name:file.name,
        media_type:file.media_type || "application/json",
        size_bytes:bytes.length,
        sha256:actual,
        content_base64:file.content_base64,
        admitted_at:new Date().toISOString(),
        credential_material_present:false,
        provider_operation_authorized:false,
        authority_effect:"NONE"
      };

      return validateInstallationReceiptRow(candidate).then(function(){
        return get(FILES,key).then(function(existing){
          if(!existing) return putOnce(FILES,key,candidate).then(function(){return {state:"KV_MATERIALIZED_LOCAL",count:1,recovery_mode:"CANONICAL_INSTALLATION_RECEIPT_FIRST_ADMISSION"};});
          if(sameCanonicalFile(existing,candidate)) return {state:"KV_MATERIALIZED_LOCAL",count:1,recovery_mode:"CANONICAL_INSTALLATION_RECEIPT_IDEMPOTENT_REUSE"};

          return validateInstallationReceiptRow(existing).then(function(){
            throw new Error("write_once_collision:"+FILES);
          }).catch(function(error){
            if(String(error && error.message || error) === "write_once_collision:"+FILES) throw error;
            return shaUri(existing).then(function(priorHash){
              candidate.recovery_mode = "REPLACE_INVALID_CANONICAL_INSTALLATION_RECEIPT";
              candidate.replaced_invalid_row_sha256 = priorHash;
              return put(FILES,candidate).then(function(){
                return {state:"KV_MATERIALIZED_LOCAL",count:1,recovery_mode:candidate.recovery_mode,replaced_invalid_row_sha256:priorHash};
              });
            });
          });
        });
      });
    });
  };
}());
