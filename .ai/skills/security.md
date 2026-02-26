# Security Rules

- Never paste API keys, tokens, or passwords into code or PR descriptions.
- Vault path and fit-docs path are configuration values. Load them from `.env`, never hardcode them.
- `.env` is always listed in `.gitignore` and must never be committed.
- Log only filenames and status — do not log draft content.
- Airtable API key lives in `.env` as `AIRTABLE_API_KEY`.
- Anthropic/OpenAI keys live in `.env` as `ANTHROPIC_API_KEY` / `OPENAI_API_KEY`.
- If a secret is accidentally committed: stop, rotate the key, and clean up git history before proceeding.
