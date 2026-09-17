# Pebbi for Claude Code

@AGENTS.md

**Documentation only until the owner explicitly resumes implementation.** Current scope is local BYOK Azure onboarding, not the older full managed-service app.

Read [the current feature](docs/product/LOCAL-AZURE-ONBOARDING.md), [CONTRACT.md](docs/CONTRACT.md) and [the index](docs/README.md). A later explicit `/build-pebbi` invocation loads [BUILD-PROMPT.md](docs/agents/BUILD-PROMPT.md) for this bounded feature only.

No backend, Supabase, Render, Vercel, Pebbi account, Stripe or mandatory locked model. Keys stay in macOS Keychain; actual Azure inference is remote. Do not modify the user's global Claude/LiteLLM/Azure configuration.

Specialist agents inherit the development model and normal permissions. Their deployment-related names are compatibility names, not permission to create servers. No project credential file, unsafe auto-approval or security bypass is included.
