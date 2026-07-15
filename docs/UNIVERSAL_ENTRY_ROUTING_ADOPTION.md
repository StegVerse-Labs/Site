# Site Universal Entry Routing Adoption

## Source of truth

`StegVerse-org/StegVerse-SDK/docs/UNIVERSAL_ENTRY_ROUTING_CONTRACT.md`

Schema:

`StegVerse-org/StegVerse-SDK/schemas/universal-entry-envelope.schema.v0.1.json`

## Site role

`ecosystem-chat.html` is an entry adapter. It is not the owner of routing semantics, capability authority, receipt authority, or execution authority.

Every accepted Site Chat input must be normalized into the SDK universal entry envelope before governed routing. The same route must be usable by SDK, API, portable node, StegTalk, agent, repository-ingest, external-actor, and partner-adapter entry points.

## Required lanes

```text
conversation
 ecosystem_query
 external_llm
 research
 solver
 governed_task
 execution
```

Site may present only lanes that the connected node capability registry marks operational or degraded. It must not present fixture-only capability as performed work.

## Current adoption state

```text
universal_envelope_schema: SDK_INSTALLED
site_manifest_binding: NOT_IMPLEMENTED
shared_router_transport: NOT_DEPLOYED
conversation_engine: PARTIAL_LOCAL_PRE_ROUTER
 ecosystem_query_engine: NOT_CONNECTED
 external_llm_engine: NOT_CONNECTED
 mixed_query_orchestration: NOT_CONNECTED
 governed_return_path: PREVIEW_ONLY
 provider_usage_receipt: NOT_CONNECTED
 master_records_custody: NOT_CONNECTED
 portable_node_release: BLOCKED
```

## Release gate

The public Site may remain a development preview. It must not claim that the portable Ecosystem Chat node is functionally complete until:

1. Site emits the universal envelope;
2. the shared router consumes it;
3. conversational, ecosystem-query, and external-LLM lanes perform their declared work;
4. mixed queries preserve source and lane provenance;
5. applicable routing, usage, retrieval, decision, execution, custody, and reconstruction receipts are emitted;
6. entry-point parity tests pass;
7. unavailable capabilities fail closed without being represented as completed.

## Boundary

A Site-local classification or hash is not an SDK intake receipt, routing receipt, proof receipt, execution receipt, custody receipt, or Master-Records installation.
