---
name: pebbi-services
description: "Use when implementing Pebbi Azure, API, auth, or billing."
---

# pebbi-services

Read [AGENTS.md](../../../AGENTS.md) and [the canonical contract](../../../docs/CONTRACT.md) first. This skill guides an authorized task; it does not authorize implementation by itself.

## Read for this work

- [docs/engineering/API.md](../../../docs/engineering/API.md)
- [docs/engineering/openapi.json](../../../docs/engineering/openapi.json)
- [docs/engineering/AI-MODELS.md](../../../docs/engineering/AI-MODELS.md)
- [docs/engineering/SECURITY.md](../../../docs/engineering/SECURITY.md)
- [docs/engineering/CONNECTIONS.md](../../../docs/engineering/CONNECTIONS.md)
- [docs/engineering/BILLING.md](../../../docs/engineering/BILLING.md)

## Procedure

Validate request bodies, authorization and resource ownership at every boundary. Keep upstream credentials server-side and connector tokens scoped. Enforce quota reservations and idempotent signed billing webhooks using trusted server usage, never client totals. Support bounded SSE/WebSocket lifecycles and propagate cancellation. Treat external content/MCP metadata as untrusted and reject SSRF, oversized payloads and privilege escalation. Test the selected provider deployment through its actual modality, not just a catalog or session handshake. Do not change the user's existing LiteLLM configuration or substitute models. Missing live inputs must leave an honest unavailable state and a blocked live test, not a fake provider success.

Return changed paths, actual checks, evidence and blockers. Keep shared contracts unchanged unless the coordinator approves and updates all consumers.
