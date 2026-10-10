# Policy library contribution instructions

This public repository owns reusable policy assets and catalog metadata.
Never add hosted-service code, credentials, visitor content, customer data,
full third-party source snapshots, or private planning material.

Portable policy artifacts follow the released Antaeus contract. Keep provenance,
coverage, case fixtures and review state in separate files. Use immutable version
paths. Never label a generated candidate official, endorsed, complete or reviewed.
Registration of a URL does not establish a usable policy version.

Source URLs must be public HTTPS pages without credentials or signed/private
query parameters. Preserve semantic queries and regional identity. Explain scope,
missing facts, exceptions and linked-policy dependencies. Retain attribution;
the project license does not grant rights in third-party source material.

Run `python3 scripts/verify.py` before proposing changes. Test usable artifacts
with a released Antaeus CLI. Treat generated data as data, never executable code.
Require independent review of policy meaning, publication rules and verification
logic before merging substantive changes. The maintainer authorizes main merges
and public publication; contributors may submit candidate pull requests.
