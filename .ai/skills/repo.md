# fit-docs-forge — Repo Map

## Structure
- `/agent` — Python package. All AI logic, file ops, promote scripts, and folder rewrites will live here.
- `/app` — placeholder for the Next.js preview + gate UI yet to be built.
- `/.ai` — agent scaffolding. Read `AGENT.md` before every session.
- `/FIT-Automate-Master-Blueprint-v3.md` — the master plan (7 phases). Agents consult this before proposing PRs.
- `/CHANGELOG.md` — running history of every merged change. Updated on every PR.
- `/.github` — CI workflows, Dependabot, PR template, issue template.

## Key concepts
- Library README = schema for that folder. Always read it before touching files there.
- Promote script: will validate gate fields, route drafts, and build compliant filenames when ready.
- Gate fields: a set of `gate_` frontmatter booleans that must all be true before promotion.
- Documentation gate: every PR must update CHANGELOG.md and keep README/`.ai/` files accurate.
- Vault path: `C:\Vaults\FIT-Vault\` (local Windows environment used by the agent).
- Fit-docs path: `C:\Dev\fit-docs\` (target repository where promoted drafts land).

## Key directories in fit-docs (the target repo, not this one)
- `docs/Operations/SOPs/` — published SOPs (named `📚 SOP NN — Title.md`)
- `docs/Operations/Procedures/` — published procedures (named `📋 PROC — System — Title.md`)
- `docs/Knowledge Base/` — published KB articles (named `📘 KB — Title.md`)
- Each library folder has a README that is the schema source (the 👮 file)

## Where env vars live
- `agent/.env` — API keys, the vault path override, and the fit-docs path override. Never commit this file; it's in `.gitignore`.
- `agent/.env.example` shows the expected keys.
- `python-dotenv` is used to load these values at runtime.
