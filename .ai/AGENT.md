# fit-docs-forge Agent Rules

Apply these rules for every agent session in this repo.

- Small PR discipline: one concern per PR, draft first, validate before ready-for-review.
- Never commit secrets or credentials.
- Always run both validation gates (Python + Next.js) before marking a PR ready.
- README-as-schema rule (critical): before touching any library folder, read that folder README and treat it as the source of truth.
- Reference the exact blueprint phase in every issue and PR.
- Agent drop zone for new drafts: `C:\Vaults\FIT-Vault\00-INBOX\_agent-drop\`.
- Defaults for new drafts: all `gate_` frontmatter fields start as `false`.
- Do not invent SLAs, prices, or numeric commitments.

## Documentation Parity Gate (required on every PR)

1. Update `CHANGELOG.md` under `[Unreleased]`.
2. Update `README.md` if phase status, workflow, commands, or structure changed.
3. Update `.ai/COMMANDS.md` when script behavior, CLI flags, or env usage changed.
4. Update `agent/.env.example` when env keys/default strategy changed.
5. If Airtable mapping strategy changes, `COMMANDS.md` and `.env.example` must match exactly.
6. If safety flows change (promote/rollback/audit), `README.md` and `.ai/COMMANDS.md` must both be updated in the same PR.
7. Validate PR template checklist is still accurate; update it when gates/process rules change.

See `.ai/skills/tests.md` for detailed validation + evidence format.
