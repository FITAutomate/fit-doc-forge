# Validation + Evidence Format

## Python gate (run from `/agent`)
pip install -e ".[dev]"
ruff check .
pytest

Expected evidence in PR:
- ruff: "All checks passed." or diff count of 0
- pytest: "X passed in Xs" — no failures, no errors

## Next.js gate (run from `/app`)
npm ci
npm run lint
npm run build

Expected evidence in PR:
- lint: exit 0, no errors
- build: "✓ Compiled successfully" or equivalent

## Manual validation (John's gate)
- John pulls the branch locally
- Runs both gates himself
- Tests the specific feature, confirms against acceptance criteria
- Only John merges — never auto-merge
