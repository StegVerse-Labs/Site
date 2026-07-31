const CANONICAL = Object.freeze({
  primary_version: "v1.1",
  primary_sha256: "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462",
  protocol: "HIL-PROTOCOL-v1.1",
  prompt: "HIL-PROMPT-v1.1",
  prompt_sha256: "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"
});

module.exports = function handler(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ error: "method_not_allowed" });
  }

  res.setHeader("Cache-Control", "no-store");
  return res.status(200).json({
    schema_version: "HIL-VERCEL-DIAGNOSTIC-v1",
    state: "DIAGNOSTIC",
    receiver_mode: "DIAGNOSTIC",
    durable_submission: false,
    exact_byte_retrieval: false,
    publication_authorized: false,
    custody_backend: null,
    canonical: CANONICAL
  });
};
