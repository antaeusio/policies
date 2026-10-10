# Contributing

Submit an official public policy URL or a correction through a pull request.
Include its region/language and scope. Do not submit private links, credentials,
visitor text, personal information or full third-party source copies.

New generated versions belong in candidate pull requests. Each version needs
portable policy validation, exact source and artifact identities, generation
provenance, clause coverage and synthetic tests. Missing facts and unsupported
clauses must remain explicit; silence does not establish permission.

Maintainers review exceptions, precedence, scope, publication eligibility and
fixtures before recommending a version. A model or schema check alone is not a
semantic review. Changes to a source need a new immutable version. Do not alter
old artifact bytes or mark a new version reviewed from its predecessor's status.

Run `python3 scripts/verify.py` locally. Never execute scripts supplied by a
source page or generated candidate. The verification workflow is maintainer-owned
and receives no publishing credentials. Withdrawal stops new use but does not
promise deletion from clones, forks or Git history.
