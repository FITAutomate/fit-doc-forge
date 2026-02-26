# Validation + Evidence Format

## Python gate (run from `/agent`)
```
pip install -e ".[dev]"
ruff check .
pytest
```

Expected evidence in PR:
- ruff: "All checks passed." or diff count of 0
- pytest: "X passed in Xs" — no failures, no errors

## Next.js gate (run from `/app`)
```
npm ci
npm run lint
npm run build
```

Expected evidence in PR:
- lint: exit 0, no errors
- build: exit 0 or "Compiled successfully"

## Documentation gate (every PR)
Before opening or merging any PR, confirm:

### CHANGELOG.md
- [ ] New entry added under `[Unreleased]` describing what changed
- [ ] Entry uses the correct section: Added, Changed, Fixed, Removed, Deprecated
- [ ] When a release is cut, `[Unreleased]` items move under a dated heading

### README.md
- [ ] If the PR adds, removes, or renames a top-level file or directory — README structure table is updated
- [ ] If the PR changes how validation works — README gate commands are updated
- [ ] If the PR changes contributing workflow — README contributing section is updated

### .ai/ files
- [ ] If agent rules change — `.ai/AGENT.md` is updated
- [ ] If validation commands change — `.ai/COMMANDS.md` is updated
- [ ] If repo structure changes — `.ai/skills/repo.md` is updated

## Manual validation (John's gate)
- John pulls the branch locally
- Runs both CI gates himself
- Confirms documentation gate: CHANGELOG entry exists, README is accurate
- Tests the specific feature, confirms against acceptance criteria
- Only John merges — never auto-merge
