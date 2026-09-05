"use strict";

(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.StegVerseVisualProjection = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  const SCHEMA = "stegverse.ecosystem_visual_projection/v1";
  const RENDERER_ROLE = "PROJECTION_ONLY";

  function fail(reason) { throw new Error("FAIL_CLOSED: " + reason); }
  function arr(value) { return Array.isArray(value) ? value : []; }
  function uniq(values) { return Array.from(new Set(values.filter(Boolean))).sort(); }
  function safeId(value) { return String(value || "").replace(/[^a-zA-Z0-9_.:-]/g, "_"); }

  function assertCanonicalEvent(event) {
    if (!event || typeof event !== "object") fail("canonical event must be an object");
    if (!event.event_id) fail("canonical event missing event_id");
    if (!event.event_type) fail("canonical event missing event_type");
  }

  function normalizeDisposition(event) {
    const raw = String(
      event.disposition ||
      (event.governed_projection && event.governed_projection.disposition) ||
      (event.governed_projection && event.governed_projection.state) ||
      ""
    ).toUpperCase();
    if (["ALLOW", "ADMITTED", "PASS"].includes(raw)) return "ADMITTED";
    if (["DENY", "BLOCK", "REJECT", "FAIL_CLOSED"].includes(raw)) return "DENIED";
    if (["DEFER", "PENDING", "QUARANTINE"].includes(raw)) return "DEFERRED";
    return raw || null;
  }

  function nodeForEvent(event) {
    return {
      id: "event:" + safeId(event.event_id),
      kind: event.event_type === "decision" ? "decision" : "event",
      label: String(
        (event.human_projection && (event.human_projection.title || event.human_projection.summary || event.human_projection.text)) ||
        event.event_type
      ),
      source_event_ids: [event.event_id],
      state: normalizeDisposition(event),
      refs: uniq([
        ...arr(event.evidence_refs), ...arr(event.policy_refs), ...arr(event.artifact_refs), ...arr(event.continuity_refs)
      ]),
      presentation: { emphasis: event.event_type === "decision" ? "decision" : "normal" }
    };
  }

  function edgeId(from, to, relation) { return "edge:" + safeId(from + ":" + relation + ":" + to); }

  function buildProjection(events, options) {
    options = options || {};
    if (!Array.isArray(events) || !events.length) fail("at least one canonical event is required");
    events.forEach(assertCanonicalEvent);

    const ids = events.map((event) => event.event_id);
    if (new Set(ids).size !== ids.length) fail("duplicate canonical event_id");
    const known = new Set(ids);
    const nodes = events.map(nodeForEvent);
    const edges = [];

    events.forEach((event) => {
      if (event.parent_event_id) {
        if (!known.has(event.parent_event_id)) fail("unresolved parent_event_id " + event.parent_event_id);
        const from = "event:" + safeId(event.parent_event_id);
        const to = "event:" + safeId(event.event_id);
        edges.push({ id: edgeId(from, to, "parent"), from, to, relation: "parent", source_event_ids: [event.parent_event_id, event.event_id] });
      }
      arr(event.relationships).forEach((relationship, index) => {
        if (!relationship || !relationship.target_event_id) fail("relationship target_event_id missing");
        if (!known.has(relationship.target_event_id)) fail("unresolved relationship target " + relationship.target_event_id);
        const from = "event:" + safeId(event.event_id);
        const to = "event:" + safeId(relationship.target_event_id);
        const relation = String(relationship.relation || "related");
        edges.push({ id: edgeId(from, to, relation + ":" + index), from, to, relation, source_event_ids: [event.event_id, relationship.target_event_id] });
      });
    });

    const evidenceRefs = uniq(events.flatMap((event) => arr(event.evidence_refs)));
    const policyRefs = uniq(events.flatMap((event) => arr(event.policy_refs)));
    const artifactRefs = uniq(events.flatMap((event) => arr(event.artifact_refs)));
    const continuityRefs = uniq(events.flatMap((event) => arr(event.continuity_refs)));

    const projection = {
      schema: SCHEMA,
      projection_id: String(options.projection_id || ("projection:" + ids.map(safeId).join("+"))),
      source_event_ids: ids.slice(),
      nodes,
      edges,
      presentation: {
        mode: options.mode || "auto",
        layout: options.layout || "governed-topology",
        focus_node_id: options.focus_event_id ? "event:" + safeId(options.focus_event_id) : null,
        animate: options.animate !== false
      },
      provider: {
        id: options.provider_id || "provider-neutral",
        capabilities: uniq(options.capabilities || ["2d", "3d", "interactive-selection", "bounded-refinement"])
      },
      provenance: {
        canonical_stream: String(options.canonical_stream || "ecosystem-chat:canonical-governed-event-stream"),
        generated_from_exact_events: true,
        evidence_refs: evidenceRefs,
        policy_refs: policyRefs,
        artifact_refs: artifactRefs,
        continuity_refs: continuityRefs
      },
      authority: {
        renderer_may_mutate_canonical_events: false,
        renderer_may_grant_admission: false,
        renderer_may_invent_evidence: false,
        renderer_role: RENDERER_ROLE
      }
    };

    validateProjection(projection);
    return projection;
  }

  function validateProjection(projection) {
    if (!projection || projection.schema !== SCHEMA) fail("unsupported projection schema");
    if (!projection.provenance || projection.provenance.generated_from_exact_events !== true) fail("projection provenance missing");
    if (!projection.authority) fail("authority boundary missing");
    if (projection.authority.renderer_may_mutate_canonical_events !== false) fail("renderer canonical mutation authority prohibited");
    if (projection.authority.renderer_may_grant_admission !== false) fail("renderer admission authority prohibited");
    if (projection.authority.renderer_may_invent_evidence !== false) fail("renderer evidence invention prohibited");
    if (projection.authority.renderer_role !== RENDERER_ROLE) fail("renderer role must be PROJECTION_ONLY");

    const sourceIds = new Set(arr(projection.source_event_ids));
    const nodeIds = new Set();
    arr(projection.nodes).forEach((node) => {
      if (!node.id) fail("node id missing");
      if (nodeIds.has(node.id)) fail("duplicate node id " + node.id);
      nodeIds.add(node.id);
      if (!arr(node.source_event_ids).length) fail("node source_event_ids missing");
      arr(node.source_event_ids).forEach((id) => { if (!sourceIds.has(id)) fail("node references unknown source event " + id); });
    });
    const edgeIds = new Set();
    arr(projection.edges).forEach((edge) => {
      if (!edge.id || edgeIds.has(edge.id)) fail("edge id missing or duplicate");
      edgeIds.add(edge.id);
      if (!nodeIds.has(edge.from) || !nodeIds.has(edge.to)) fail("edge endpoint unresolved");
      arr(edge.source_event_ids).forEach((id) => { if (!sourceIds.has(id)) fail("edge references unknown source event " + id); });
    });
    return true;
  }

  function siteFlowCapabilityDescriptor() {
    return {
      provider_id: "ai-siteflow-compatible",
      provider_type: "visual-projection-renderer",
      runtime_hints: ["nextjs", "webgl", "realtime-3d"],
      capabilities: ["2d", "3d", "interactive-selection", "bounded-refinement", "animation", "topology"],
      authority: RENDERER_ROLE,
      endpoint: null,
      credential_ref: null,
      integration_state: "CAPABILITY_DESCRIPTOR_ONLY"
    };
  }

  return { SCHEMA, buildProjection, validateProjection, siteFlowCapabilityDescriptor };
});
