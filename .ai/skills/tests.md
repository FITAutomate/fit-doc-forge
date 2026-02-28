# Validation + Evidence Format

## Python gate (run from `/agent`)
```bash
pip install -e ".[dev]"
ruff check .
pytest
```

Expected evidence in PR:
- `ruff check`: no errors
- `pytest`: all tests pass

## Next.js gate (run from `/app`)
```bash
npm ci
npm run lint
npm run build
```

Expected evidence in PR:
- `npm run lint`: pass
- `npm run build`: pass

## Documentation parity gate (every PR)

Before opening or merging any PR:

### CHANGELOG
- [ ] New `[Unreleased]` entry added (Added/Changed/Fixed/Removed)

### README
- [ ] Updated if phase status, workflow, structure, or run commands changed

### .ai docs
- [ ] `.ai/COMMANDS.md` updated when script behavior/flags/env usage changed
- [ ] `.ai/AGENT.md` updated when process rules or documentation gate changed
- [ ] `.ai/skills/repo.md` updated when repo map/key concepts changed

### Env alignment
- [ ] `agent/.env.example` updated when env keys/default strategy changed
- [ ] `.ai/COMMANDS.md` env block matches `.env.example`
- [ ] Airtable field mapping policy (`AIRTABLE_USE_FIELD_IDS`) is consistent across docs

### Safety workflow alignment
- [ ] If promote/rollback/audit behavior changed, both `README.md` and `.ai/COMMANDS.md` were updated in the same PR
