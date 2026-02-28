# fit-docs-forge - Repo Map

## Structure
- `/agent` - Python package for automation logic, promote/rollback scripts, and vault tooling.
- `/app` - Next.js preview UI with draft browser, gate panel, and approve-to-promote action.
- `/.ai` - Agent guidance, commands, templates, and repo-specific guardrails.
- `/.github` - CI workflow, PR template, and issue templates.
- `/FIT-Automate-Master-Blueprint-v3.md` - Master phase plan.
- `/CHANGELOG.md` - Running merged-change history.

## Key concepts
- README-as-schema: every fit-docs library README is the source of truth for structure and formatting.
- Promote flow: validate gates -> write target -> strict build -> commit -> archive/update draft -> audit log.
- Rollback flow: resolve from audit log -> remove target -> strict build -> commit -> restore archived draft -> audit log.
- Documentation parity gate: keep CHANGELOG, README, `.ai/COMMANDS.md`, and `.env.example` synchronized.

## Paths and environment
- Vault root: `C:\Vaults\FIT-Vault\`
- fit-docs root: `D:\dev\github\fit-docs\docs`
- Runtime env file: `agent/.env` (never commit)
- Template env file: `agent/.env.example`

## fit-docs library targets
- `docs/Operations/SOPs/`
- `docs/Operations/Procedures/`
- `docs/Knowledge Base/`
- Each library contains a README schema file that must be read before edits.
