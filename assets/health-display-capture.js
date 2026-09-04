(function () {
  "use strict";

  const SCHEMA = "steghealth.lab-import-bundle.v0.1";

  function isoNow() { return new Date().toISOString(); }
  function uid(prefix) {
    if (globalThis.crypto && crypto.randomUUID) return `${prefix}-${crypto.randomUUID()}`;
    return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  }

  async function sha256(text) {
    if (!globalThis.crypto || !crypto.subtle) return null;
    const bytes = new TextEncoder().encode(text);
    const digest = await crypto.subtle.digest("SHA-256", bytes);
    return "sha256:" + Array.from(new Uint8Array(digest)).map(b => b.toString(16).padStart(2, "0")).join("");
  }

  function normalizeWhitespace(value) {
    return String(value || "").replace(/\u00a0/g, " ").replace(/[ \t]+/g, " ").trim();
  }

  function parseNumber(value) {
    const cleaned = String(value || "").replace(/,/g, "").trim();
    if (!/^[-+]?\d+(?:\.\d+)?$/.test(cleaned)) return null;
    const parsed = Number(cleaned);
    return Number.isFinite(parsed) ? parsed : null;
  }

  function splitCandidateLine(line) {
    const tab = line.split(/\t+/).map(normalizeWhitespace).filter(Boolean);
    if (tab.length >= 2) return tab;
    const wide = line.split(/\s{2,}/).map(normalizeWhitespace).filter(Boolean);
    if (wide.length >= 2) return wide;
    return null;
  }

  function parseReference(text) {
    const value = normalizeWhitespace(text);
    let match = value.match(/^([-+]?\d+(?:\.\d+)?)\s*[-–]\s*([-+]?\d+(?:\.\d+)?)(?:\s+(.+))?$/);
    if (match) return { low: Number(match[1]), high: Number(match[2]), unit: normalizeWhitespace(match[3] || "") || null };
    return { low: null, high: null, unit: null };
  }

  function parseLabText(text) {
    const results = [];
    const lines = String(text || "").split(/\r?\n/).map(normalizeWhitespace).filter(Boolean);

    for (const line of lines) {
      const fields = splitCandidateLine(line);
      if (!fields || fields.length < 2) continue;

      const display = fields[0];
      let valueIndex = -1;
      let numericValue = null;
      for (let i = 1; i < fields.length; i += 1) {
        const maybe = parseNumber(fields[i].replace(/^[<>]=?\s*/, ""));
        if (maybe !== null) { valueIndex = i; numericValue = maybe; break; }
      }
      if (valueIndex < 0) continue;

      let unit = null;
      let referenceText = null;
      let flag = null;
      for (let i = valueIndex + 1; i < fields.length; i += 1) {
        const f = fields[i];
        if (/^(H|L|HH|LL|high|low|abnormal)$/i.test(f)) { flag = f; continue; }
        if (/[-–]/.test(f) && /\d/.test(f)) { referenceText = f; continue; }
        if (!unit && f.length <= 24) unit = f;
      }
      const ref = parseReference(referenceText || "");
      if (!unit && ref.unit) unit = ref.unit;

      results.push({
        result_id: uid("LABR"),
        display,
        code: null,
        code_system: null,
        value: numericValue,
        unit,
        reference_low: ref.low,
        reference_high: ref.high,
        reference_text: referenceText,
        flag,
        value_state: "unknown",
        source_state: "parsed_text",
        confidence: 0.72,
        source_fragment_ref: `display-line:${results.length + 1}`
      });
    }
    return results;
  }

  async function buildBundle({ text, displayName, sourceType, originalFilename }) {
    const sourceText = String(text || "");
    const results = parseLabText(sourceText);
    const contentHash = await sha256(sourceText);
    return {
      schema_version: SCHEMA,
      import_id: uid("LABIMPORT"),
      imported_at: isoNow(),
      source: {
        source_type: sourceType || "displayed_surface",
        display_name: displayName || "User-authorized displayed surface",
        provider_id: null,
        export_format: originalFilename ? (originalFilename.split(".").pop() || "unknown") : "text"
      },
      patient_match: {
        state: "unconfirmed",
        confidence: 0,
        matched_record_ref: null
      },
      panels: [{
        panel_id: uid("PANEL"),
        name: "Imported laboratory results",
        effective_at: null,
        ordering_provider: null,
        accession: null,
        specimen: null,
        fasting_state: "unknown",
        results
      }],
      provenance: {
        origin_ref: `displayed-surface://${uid("CAPTURE")}`,
        content_hash: contentHash,
        raw_preserved: true,
        original_filename: originalFilename || null,
        record_ref: null
      },
      normalization: {
        loinc_mapping_applied: false,
        unit_normalization_applied: false,
        duplicate_resolution_applied: false,
        notes: "First-pass displayed-surface parser. All parsed values require provenance-preserving review before promotion."
      }
    };
  }

  function downloadJson(value, filename) {
    const blob = new Blob([JSON.stringify(value, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 5000);
  }

  async function readFile(file) {
    if (!file) return "";
    if (file.type && !file.type.startsWith("text/") && !/\.(txt|csv|json|xml)$/i.test(file.name)) {
      throw new Error("This first implementation directly reads text/CSV/JSON/XML. PDF/image extraction is the next adapter lane.");
    }
    return file.text();
  }

  function renderBundle(bundle, out, count) {
    out.textContent = JSON.stringify(bundle, null, 2);
    const n = bundle.panels[0].results.length;
    count.textContent = `${n} candidate result${n === 1 ? "" : "s"} parsed`;
  }

  async function init() {
    const text = document.querySelector("#capture-text");
    const file = document.querySelector("#capture-file");
    const parse = document.querySelector("#capture-parse");
    const save = document.querySelector("#capture-save");
    const out = document.querySelector("#capture-output");
    const count = document.querySelector("#capture-count");
    const native = document.querySelector("#capture-native");
    let lastBundle = null;

    if (!text || !file || !parse || !save || !out || !count) return;

    file.addEventListener("change", async () => {
      try {
        const selected = file.files && file.files[0];
        if (!selected) return;
        text.value = await readFile(selected);
        count.textContent = `Loaded ${selected.name}`;
      } catch (error) {
        count.textContent = error.message;
      }
    });

    parse.addEventListener("click", async () => {
      const selected = file.files && file.files[0];
      lastBundle = await buildBundle({
        text: text.value,
        displayName: selected ? selected.name : "User-authorized displayed content",
        sourceType: selected ? "portal_export" : "displayed_surface",
        originalFilename: selected ? selected.name : null
      });
      renderBundle(lastBundle, out, count);
      save.disabled = false;
    });

    save.addEventListener("click", () => {
      if (!lastBundle) return;
      downloadJson(lastBundle, `${lastBundle.import_id}.json`);
    });

    if (native) {
      native.addEventListener("click", () => {
        const payload = { action: "START_DISPLAYED_SURFACE_CAPTURE", schema: "stegverse.displayed-surface-capture-request.v0.1", requested_at: isoNow(), purpose: "LAB_IMPORT" };
        window.dispatchEvent(new CustomEvent("stegverse-native-capture-request", { detail: payload }));
        count.textContent = "Native capture requested. A future iOS host can bind this event to the system capture session; Safari alone cannot capture another app's screen.";
      });
    }
  }

  window.StegHealthDisplayedCapture = { parseLabText, buildBundle };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
