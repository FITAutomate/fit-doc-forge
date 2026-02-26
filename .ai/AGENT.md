# fit-doc-forge Agent Rules

Apply these rules for every agent session in this repo:

- Small PR discipline: one concern per PR, always validate before opening, and prefer draft mode first.
- Never commit secrets or credentials.
- Always run both validation gates (agent and app) before marking a PR ready for review.
- **README-as-schema rule (CRITICAL):** before touching any library folder, read that folder’s README to capture naming conventions, metadata tables, required H2/H3 sections, and any other rules; treat the README as authoritative (it wins over archived YAML schemas).
- When proposing PRs, reference the relevant phase from `FIT-Automate-Master-Blueprint-v3.md`.
- Agent drop zone for new drafts: `C:\Vaults\FIT-Vault\00-INBOX\_agent-drop\`
- Defaults for new drafts: all `gate_` frontmatter fields start as `false`.
- Do not invent SLAs, prices, or numbers not explicitly provided in the blueprint.
- **Documentation gate (REQUIRED on every PR):**
  1. Add a CHANGELOG.md entry under `[Unreleased]` describing what changed (Added/Changed/Fixed/Removed)
  2. Update README.md if the PR changes repo structure, validation commands, or contributing workflow
  3. Update `.ai/` files if agent rules, commands, or repo map change
  4. See `.ai/skills/tests.md` for the full documentation gate checklist
