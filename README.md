# fit-docs-forge

AI-powered documentation pipeline for FIT Automate. Agents read library READMEs as schemas, draft and validate documents through gate fields, and promote them into the published `fit-docs` repo via a promote script.

The full plan lives in [`FIT-Automate-Master-Blueprint-v3.md`](FIT-Automate-Master-Blueprint-v3.md).

## Structure
| Path | What | Status |
|---|---|---|
| `.ai/` | Agent rules, commands, config, templates, skills | Active |
| `.github/` | CI workflows, Dependabot, PR/issue templates | Active |
| `agent/` | Python package — AI logic, promote script, folder rewrites | Skeleton |
| `app/` | Next.js — preview UI, gate status, approve-to-promote | Placeholder |
| `FIT-Automate-Master-Blueprint-v3.md` | The master plan (7 phases) | Active |
| `CHANGELOG.md` | Running history of every merged change | Active |

## Validation gates
Every PR must pass both gates before merge.

### Python gate (`agent/`)
```bash
cd agent
pip install -e ".[dev]"
ruff check .
pytest
```

### Next.js gate (`app/`)
```bash
cd app
npm ci
npm run lint
npm run build
```

## Contributing
1. Read `.ai/AGENT.md` before every session.
2. One concern per PR, always draft first.
3. Reference the relevant blueprint phase in the PR description.
4. Update `CHANGELOG.md` and this README when your PR changes repo structure or adds features.
5. Both CI gates must pass before requesting review.
