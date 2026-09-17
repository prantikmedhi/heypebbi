# Project-local Claude support

This directory contains original Pebbi-specific instructions. It does not install or change global skills, provider configuration, credentials or permission settings.

- `/build-pebbi` is an explicitly invoked skill that loads the complete build contract.
- `pebbi-native`, `pebbi-visual`, `pebbi-services`, and `pebbi-verification` are domain procedures.
- Specialist agent files in `agents/` reference those skills and use `model: inherit`. They do not force a paid Anthropic model or imply a runtime dependency.
- No unsafe auto-approval setting, hook or project secret file is included. Existing user/admin permissions continue to govern tools.

Other coding agents should read [AGENTS.md](../AGENTS.md), [the build prompt](../docs/agents/BUILD-PROMPT.md) and the same skill Markdown directly if they do not discover this directory automatically. Project skill formats are documented by [Claude](https://code.claude.com/docs/en/skills); use the installed client's supported behavior rather than assuming a feature exists.
