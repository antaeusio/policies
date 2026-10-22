# Policy catalog and candidate version format

Catalog format `1` contains source registrations only. Format `2` adds a
top-level `versions` array and preserves registration fields and meanings.
Source entries remain `registered` with `current_version: null`; a downloadable
candidate is not a recommended or currently servable version.

Each version entry has `source_id`, `version_id`, `policy_digest`, `state`,
`files`, `cli_version`, `case_count` and `semantic_evaluation`. Paths are derived
as `policies/<source_id>/versions/<version_id>/`; no artifact can supply an
arbitrary filesystem path. IDs use lowercase kebab case. Version IDs use
`YYYY-MM-DD.N`, with a positive integer suffix.

This first format admits only `state: candidate`,
`semantic_evaluation: not_evaluated` and released CLI `0.7.0`. Promotion,
withdrawal and trusted service indexing require subsequent reviewed changes;
none can be asserted by setting a boolean or changing a catalog pointer today.
The separate review/catalog state must not alter historical version bytes.

`files` names the exact six immutable files and their raw-byte `sha256:` digests:
`policy.json`, `provenance.json`, `coverage.json`, `cases.json`, `fixtures.json`
and `README.md`. JSON files reject duplicate keys and non-finite numbers.
Version files must be regular, bounded files, without symlink traversal.
Every on-disk version must be indexed exactly once. Use `--base-ref` to compare
existing version identities with a trusted Git base; updating a manifest cannot
legitimize changes to a previously published version.

The policy, RegressionSuite and FixtureSet follow the released Antaeus
contracts. Repository metadata is separate. Provenance sidecar format `1`
records exact source/final URL, language, observed region/date, source hashes,
extractor, source-retention statement, authored identity, policy digest, CLI
version, scope and semantic status. It describes direct-response extraction.
Published format-1 files stay immutable.

Provenance sidecar format `2` records a **manual public browser observation**.
It retains the same identity/date/language/region/authoring/scope fields and
replaces `response_sha256`, `extracted_text_sha256` and `extractor` with exactly
one `observation` object:

| Field | Required value or meaning |
| --- | --- |
| `method` | `browser-dom` |
| `selector` | Bounded CSS selector, recorded as data; never executed by verification. |
| `element_index` | Zero-based selected match, less than `matched_elements`. |
| `matched_elements` | Observed count, from 1 through 256. |
| `text_property` | `innerText` |
| `normalization` | `none`; hash exactly the UTF-8 encoding of the observed string. |
| `text_sha256` | Lowercase 64-character digest, without a prefix. |
| `text_bytes` | Positive observed UTF-8 byte count, at most 1 MiB. |
| `http_response_sha256` | `null`; no response bytes are linked to this observation. |
| `response_linkage` | `not-established` |
| `authentication` | `public-no-sign-in`; observations requiring sign-in are not admitted. |

A browser can render policy clauses absent from an ordinary HTML fetch. The
browser observation must not borrow that other response's hash, claim a direct
extraction chain, or establish safe automated retrieval. Record the selector,
selected index, match count and exact method at observation time. Visible source
language and regional applicability still need review. Do not retain page text,
HTML, cookies, session identifiers or request headers in the sidecar. Separate
HTTP observations may be documented privately as separate observations.

Offline verification checks the metadata's shape and artifact bindings; it does
not retrieve the page or prove that an observation happened or remains current.
Format `2` still permits only authored, unqualified candidates. It does not
change catalog format `2`, coverage format `1`, portable contracts, semantic
status, recommendation, source freshness or service eligibility. Consumers
supporting only format `1` must refuse format `2` until explicitly updated.

Coverage sidecar format `1` identifies each
clause as converted, context-dependent, unsupported or outside scope, with
reasons, references to converted rules, case-to-clause references, unresolved
dependencies and limitations. Every rule needs a converted clause. Deferred
clauses have no invented rules.

`python3 scripts/verify.py` checks catalog and sidecar integrity without an
account or network. It checks the restricted string-only canonical identities
used here; it is not a general replacement for released contract validation.
`--cli /path/to/antaeus` additionally validates each artifact and runs its exact
offline fixtures with released v0.7.0. CI obtains checksum-pinned release bytes
and performs both checks. Neither check establishes meaning, semantic quality,
source freshness, publication rights or maintainer approval.
