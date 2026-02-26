# fit-doc-forge — Repo Map

## Structure
- `/agent` — Python package. All AI logic, file ops, promote scripts, and folder rewrites will live here.
- `/app` — placeholder for the Next.js preview + gate UI yet to be built.
- `/.ai` — agent scaffolding. Read `AGENT.md` before every session.
- `/FIT-Automate-Master-Blueprint-v3.md` — the plan that agents consult before proposing PRs.

## Key concepts
- Reader-first: a library README is the schema for that folder. Always read it before editing files there.
- Promote script: will validate gate fields, route drafts, and build compliant filenames when ready.
- Gate fields: a set of `gate_` frontmatter booleans that must all be true before promotion.
- Vault path: `C:\Vaults\FIT-Vault\` (local Windows environment used by the agent).
- Fit-docs path: `C:\Dev\fit-docs\` (target repository where promoted drafts land).

## Where env vars live
- `agent/.env` — API keys, the vault path override, and the fit-docs path override. Never commit this file; it’s included in `.gitignore`.
- `agent/.env.example` shows the expected keys.
- `python-dotenv` is used to load these values at runtime.
