# Specialist ownership — local Azure onboarding

**Current operation: documentation only.** Do not dispatch implementation work until the owner resumes it. Current specification: [Local Azure onboarding](../product/LOCAL-AZURE-ONBOARDING.md); root conduct: [AGENTS.md](../../AGENTS.md).

For a later bounded implementation, use no more independent workstreams than needed:

| Role | Bounded responsibility |
| --- | --- |
| Native engineer | First-launch state, form model, atomic Keychain save/load/edit/reset and a minimal native shell |
| Experience designer | Existing Pebbi materials, accessible SecureField/form layout, validation and unavailable/error copy |
| Azure client reviewer | Endpoint/API-family/deployment semantics, local validation, direct-to-user-Azure trust boundary; no server |
| Verification reviewer | BYOK-001 through BYOK-012, secret isolation, denied/corrupt state recovery, real Mac evidence and truthful status |

Freeze the small local profile interface before parallel edits. Assign disjoint files and one owner to shared state. A reviewer should inspect changes independently, not simply repeat an implementer's result. Do not hand model prompts real API keys. A development subagent does not become an installed app dependency.

Legacy PB-001 through PB-040 allocation and managed-service implementation are no longer current. `.claude/agents/pebbi-service-engineer.md` remains a compatibility filename but now concerns direct Azure client boundaries only. No identity/billing/cloud-hosting work is in scope.
