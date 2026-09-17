---
name: pebbi-verification
description: "Use when testing or reviewing complete Pebbi behavior."
---

# pebbi-verification

Read [AGENTS.md](../../../AGENTS.md) and [the canonical contract](../../../docs/CONTRACT.md) first. This skill guides an authorized task; it does not authorize implementation by itself.

## Read for this work

- [docs/quality/ACCEPTANCE.md](../../../docs/quality/ACCEPTANCE.md)
- [docs/quality/TESTING.md](../../../docs/quality/TESTING.md)
- [docs/quality/coverage.json](../../../docs/quality/coverage.json)
- [docs/operations/RELEASE.md](../../../docs/operations/RELEASE.md)
- [docs/operations/EXTERNAL-INPUTS.md](../../../docs/operations/EXTERNAL-INPUTS.md)

## Procedure

Independently verify every claimed result with real tool output and artifacts. Cover normal and negative cases for every assigned PB ID, including focus mistakes, races, duplicate side effects, quota exhaustion, permission revocation, network loss and restart. Separate contract/unit fixtures, live integrations and hardware checks. Test doubles are never production evidence. A static screenshot is not a working control; a build is not a successful runtime; an unsigned binary is not a notarized release. Review secret handling, auth, SSRF, executable content, local tool policy and update integrity. Report severity, evidence, reproduction and remaining release blockers without lowering requirements to make the suite green.

Return changed paths, actual checks, evidence and blockers. Keep shared contracts unchanged unless the coordinator approves and updates all consumers.
