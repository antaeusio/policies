# Antaeus policy library

Public source URLs and reusable [Antaeus](https://github.com/antaeusio/antaeus)
policy versions, with explicit provenance, coverage and review status.

The [catalog](catalog.json) registers **28 official policy URLs** across commerce,
payments, community platforms, AI and hosting. It indexes four downloadable
authored candidates:

- [eBay chance-listings text](policies/ebay-chance-listings/versions/2026-10-22.1/README.md): six rules, 26 offline fixture cases.
- [Amazon product listing text](policies/amazon-product-detail-rules/versions/2026-10-22.1/README.md): two selected demo rules, 24 offline fixture cases.
- [Facebook selected spam text](policies/meta-spam/versions/2026-10-22.1/README.md): six selected rules, 28 offline fixture cases.
- [X selected authenticity text](policies/x-authenticity/versions/2026-10-23.1/README.md): six selected rules, 28 offline fixture cases.

Semantic evaluation of these candidate suites is not qualified, and no version
is recommended or currently servable. Source registrations remain an import
queue. A reachable overview page can still require linked documents or account
facts. Offline fixtures verify bindings and reduction; they do not classify text.

The first live eBay study [stopped on a mismatched result](reports/ebay-chance-listings/2026-10-23-semantic-stop/README.md)
on 23 October 2026. Four of 24 planned content cases ran: three final outcomes
matched and a described mystery-box offer was incorrectly denied against its
frozen expectation. Twenty cases remain unrun. The candidate remains
unqualified; the dated report preserves the result without changing the
immutable artifact or its historical provenance.

| State | Meaning |
| --- | --- |
| `registered` | Source URL is recorded; `current_version` is null. |
| Generated candidate | A future immutable artifact with source identity and coverage; awaiting review. |
| Reviewed version | A maintainer has approved the specific version and its test evidence. |
| Withdrawn | Unavailable for new checks; historical copies may remain public. |

## Candidate version layout

```text
policies/<source-id>/versions/<version-id>/
  policy.json
  provenance.json
  coverage.json
  cases.json
  fixtures.json
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
To also validate artifacts and execute their synthetic cases, install the
[released v0.7.0 CLI](https://github.com/antaeusio/antaeus/releases/tag/v0.7.0) and run:

```sh
python3 scripts/verify.py --cli "$(command -v antaeus)"
```

[Catalog format and integrity rules](docs/catalog-format.md) describe candidate
identities, immutable files and the distinction between fixtures and semantic
evidence. CI verifies checksum-pinned CLI release bytes and unchanged history.

## Attribution and removal

Source organizations retain rights in their policy text and marks. This library
links to source pages; it does not republish full source documents. Apache-2.0
covers this project's original code and metadata, not third-party materials.
Report corrections or removal requests through [an issue](https://github.com/antaeusio/policies/issues).
For sensitive reports, use the [security reporting route](https://github.com/antaeusio/antaeus/security/policy);
do not post secrets or personal information in public issues.
