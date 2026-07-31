const PRIMARY_SHA256 = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462";
const PROMPT_SHA256 = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c";
const SHA256 = /^[a-f0-9]{64}$/;

function bodyOf(req) {
  if (req.body && typeof req.body === "object") return req.body;
  if (typeof req.body === "string") return JSON.parse(req.body);
  return {};
}

module.exports = function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "method_not_allowed" });
  }

  res.setHeader("Cache-Control", "no-store");
  let body;
  try {
    body = bodyOf(req);
  } catch {
    return res.status(400).json({ valid: false, errors: ["invalid_json"] });
  }

  const errors = [];
  const required = ["source_object", "response_pdf", "provenance_manifest", "primary_sha256", "prompt_sha256", "response_sha256", "model", "provider", "publication_consent"];
  for (const field of required) if (body[field] === undefined || body[field] === null || body[field] === "") errors.push(`missing_${field}`);

  if (body.primary_sha256 && body.primary_sha256 !== PRIMARY_SHA256) errors.push("primary_sha256_mismatch");
  if (body.prompt_sha256 && body.prompt_sha256 !== PROMPT_SHA256) errors.push("prompt_sha256_mismatch");
  if (body.response_sha256 && !SHA256.test(body.response_sha256)) errors.push("invalid_response_sha256");
  if (body.publication_consent && !["WITHHELD", "PRIVATE_REVIEW_ONLY", "PUBLICATION_CONSENTED"].includes(body.publication_consent)) errors.push("unsupported_publication_consent");
  if (body.receipt_state && body.receipt_state !== "SOURCE_OBJECT_DECLARED") errors.push("premature_receipt_state");

  return res.status(errors.length ? 422 : 200).json({
    valid: errors.length === 0,
    errors,
    receiver_mode: "DIAGNOSTIC",
    durable_submission: false,
    exact_byte_retrieval: false,
    publication_authorized: false,
    accepted_for_custody: false,
    next_authority: errors.length ? null : "StegVerse-Labs/TVC commit-pinned intake",
    canonical: {
      primary_version: "v1.1",
      primary_sha256: PRIMARY_SHA256,
      protocol: "HIL-PROTOCOL-v1.1",
      prompt: "HIL-PROMPT-v1.1",
      prompt_sha256: PROMPT_SHA256
    }
  });
};
