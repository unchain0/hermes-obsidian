---
name: verify-gha
description: Verify GitHub Actions workflow changes by inspecting workflow syntax and running local checks (lint/test/build) in the repo.
---
- Launch: inspect .github/workflows/ for YAML syntax; run repo tests/build.
- Doctor: workflow YAML parses and `actionlint` or `yq` validates syntax.
- Drive: confirm changed workflow is syntactically valid; run `pip install -r requirements.txt` / `npm test` / `make test` as defined.
- Evidence: log output of syntax check + test results saved to .cursor/skills/verify-gha/evidence/
- Cleanup: none needed (read-only checks).
