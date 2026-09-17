# Pebbi for Claude Code

@AGENTS.md

The current repository is documentation-only. Do not start implementation unless the user asks to build or explicitly invokes `/build-pebbi`.

For an authorized full build, use [the master build prompt](docs/agents/BUILD-PROMPT.md), [documentation index](docs/README.md), and [orchestration contract](docs/agents/ORCHESTRATION.md). Repository-local specialist agents and skills live in `.claude/agents` and `.claude/skills`.

Models used by a development assistant are separate from models shipped in Pebbi. `model: inherit` keeps project subagents on the developer's chosen working provider. This repository does not reconfigure Claude, LiteLLM, Azure, or a user's global skills. Claude Code through a non-Claude model gateway is third-party compatibility, not an Anthropic-supported route; use any functioning coding agent with the portable Markdown prompt if needed.

Do not load the entire documentation pack into every child. Give each its authoritative contracts, PB requirement IDs, owned files, verification targets and current blockers. The coordinator still owns integration and independent verification.

There is deliberately no project permission override, unsafe auto-approval hook or credential-bearing settings file. Project instructions are guidance, not a security boundary.
