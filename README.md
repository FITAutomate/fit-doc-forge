# fit-doc-forge

A bootstrap for the FIT documentation forge: the `/agent` Python layer handles schema-aware drafting and promotion while `/app` (future Next.js UI) previews drafts and gate status.

## Structure
- `.ai/`: session rules, validation commands, templates, and metadata that every contributor follows.
- `.github/`: CI, Dependabot, and issue templates tailored to this repo.
- `agent/`: Python package with a placeholder test suite and dependency settings.
- `app/`: placeholder directory reserved for the Next.js preview UI.

## Getting started
1. Create the repository on GitHub as `fit-doc-forge` and push this scaffold.
2. Install Python/dev dependencies from `agent/` before running the agent gate:
   ```bash
   cd agent
   pip install -e ".[dev]"
   ruff check .
   pytest
   ```
3. When the Next.js UI arrives, run the npm gate from `app/`:
   ```bash
   cd app
   npm ci
   npm run lint
   npm run build
   ```
4. Follow `.ai/AGENT.md` before editing any folder.
