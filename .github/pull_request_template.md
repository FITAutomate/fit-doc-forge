## What this PR does
<!-- One sentence. -->

## Blueprint reference
<!-- Phase N - Step name from FIT-Automate-Master-Blueprint-v3.md -->

## Linked issue
<!-- Closes #NN -->

## Changes
- 

## Validation evidence
### Python gate
```
# paste: pip install + ruff + pytest output
```

### Next.js gate
```
# paste: npm ci + lint + build output
```

## README-as-schema compliance
<!-- If this PR touches library content: which README(s) were read and what rules were applied -->
<!-- If not applicable: N/A -->

## Documentation parity checklist
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] `README.md` updated if phase/status/workflow changed
- [ ] `.ai/COMMANDS.md` updated if commands/flags/env changed
- [ ] `agent/.env.example` updated if env keys/default strategy changed
- [ ] Promote/rollback/audit doc updates are reflected in both README and COMMANDS when applicable

## Review checklist
- [ ] Logic matches blueprint intent
- [ ] No invented data or SLAs
- [ ] Both validation gates shown above pass
- [ ] Ready to test locally
