# Antaeus policy library

Public source URLs and reusable [Antaeus](https://github.com/antaeusio/antaeus)
policy versions, with explicit provenance, coverage and review status.

The initial [catalog](catalog.json) registers **24 official policy URLs** across
commerce, payments, community platforms, AI and hosting. These links are an
import queue: **no executable policy versions are published yet**. Registered
sources must not be used as if their policies have been generated or reviewed.
A reachable overview page can still require linked documents or account facts.

| State | Meaning |
| --- | --- |
| `registered` | Source URL is recorded; `current_version` is null. |
| Generated candidate | A future immutable artifact with source identity and coverage; awaiting review. |
| Reviewed version | A maintainer has approved the specific version and its test evidence. |
| Withdrawn | Unavailable for new checks; historical copies may remain public. |

## Planned version layout

```text
policies/<source-id>/versions/<version-id>/
  policy.yaml
  provenance.json
  coverage.json
  cases.json
  README.md
```

Portable policy files use the released Antaeus contract and default to review
when permission cannot be established. Sidecars describe the exact source and
generation identity, coverage, omitted clauses and required application facts.
Versions are immutable. A new source revision needs a new policy version and
cannot inherit a previous review status.

A generated rule set is an independent interpretation of the selected source,
not an official policy, platform endorsement or proof of overall compliance.
Check the current source and related policies before using it for enforcement.
Text-only checks cannot establish every product, transaction or account fact.

## Contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md). To verify the registered catalog locally:

```sh
python3 scripts/verify.py
```

Verification needs Python 3.14 and no credential, provider call or hosted account.
Artifact reuse commands and regression cases will accompany each usable version.

## Attribution and removal

Source organizations retain rights in their policy text and marks. This library
links to source pages; it does not republish full source documents. Apache-2.0
covers this project's original code and metadata, not third-party materials.
Report corrections or removal requests through [an issue](https://github.com/antaeusio/policies/issues).
For sensitive reports, use the [security reporting route](https://github.com/antaeusio/antaeus/security/policy);
do not post secrets or personal information in public issues.
