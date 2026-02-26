# CHANGELOG Format Rules

## File
`CHANGELOG.md` at the repo root. Updated on every PR.

## Structure
```
# Changelog

## [Unreleased]
### Added / Changed / Fixed / Removed / Deprecated
- Entry here

## YYYY-MM-DD
### Added / Changed / Fixed / Removed / Deprecated
- Entry here
```

## When to write an entry
Every PR adds at least one line under `[Unreleased]`. No exceptions.

## Which section to use
| Section | Use when... |
|---|---|
| Added | A new file, feature, skill, template, or dependency is introduced |
| Changed | An existing file or behavior is modified (not a bug fix) |
| Fixed | A bug, typo, or misconfiguration is corrected |
| Removed | A file, feature, or dependency is deleted |
| Deprecated | Something still works but is scheduled for removal |

## Format rules
- Start each line with a dash and a space: `- `
- Lead with *what* changed, not *why* (the PR description covers why)
- Include the file or area affected when it's not obvious
- Keep entries to one line; if you need detail, link to the PR
- Do not include commit hashes in changelog entries (they belong in git log, not here)

## Rolling a release
When John cuts a release or closes a phase:
1. Move everything under `[Unreleased]` into a new `## YYYY-MM-DD` section
2. Leave `[Unreleased]` empty and ready for the next round
