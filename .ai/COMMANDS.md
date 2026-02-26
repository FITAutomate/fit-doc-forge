# Commands reference for fit-doc-forge

## Python gate (`agent/`)
```
cd agent
pip install -e ".[dev]"
ruff check .
pytest
```

## Next.js gate (`app/`)
```
cd app
npm ci
npm run lint
npm run build
```

## Full validation (run both terminals before any PR)
```
# Terminal 1:
cd agent && pip install -e ".[dev]" && ruff check . && pytest
# Terminal 2:
cd app && npm ci && npm run lint && npm run build
```
