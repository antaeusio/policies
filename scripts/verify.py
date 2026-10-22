"""Verify source registrations and immutable candidate artifacts offline."""
import argparse
from datetime import date, datetime
import hashlib
import ipaddress
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import parse_qsl, urlsplit


ROOT = Path(__file__).resolve().parents[1]
FIELDS = {"id", "organization", "title", "url", "category", "status",
          "current_version", "discovery", "scope_notes"}
CATEGORIES = {"commerce", "payments", "developer", "community", "ai",
              "hosting", "advertising"}


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON key")
        value[key] = item
    return value


def public_url(raw):
    if not isinstance(raw, str) or len(raw.encode()) > 2048 or not raw.isascii():
        raise ValueError("URL shape")
    if any(c.isspace() or ord(c) < 32 for c in raw) or "\\" in raw:
        raise ValueError("URL ambiguity")
    parts = urlsplit(raw)
    host = parts.hostname or ""
    if (parts.scheme != "https" or parts.port not in (None, 443)
            or parts.username is not None or parts.password is not None
            or parts.fragment or host.endswith(".") or "." not in host):
        raise ValueError("public HTTPS source required")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise ValueError("IP literal")
    if not re.fullmatch(r"[a-z0-9.-]+", host) or not re.search(r"\.[a-z]{2,}$", host):
        raise ValueError("hostname")
    if any(not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", p)
           for p in host.split(".")):
        raise ValueError("hostname label")
    if host.rsplit(".", 1)[1] in {"local", "internal", "localhost", "test", "invalid", "example"}:
        raise ValueError("reserved hostname")
    for name, _ in parse_qsl(parts.query, keep_blank_values=True):
        name = name.lower()
        if (name in {"sig", "sas", "googleaccessid", "password", "passwd", "pwd"} or name.startswith(("x-amz-", "x-goog-"))
                or any(x in name for x in ("token", "key", "auth", "signature", "credential", "secret", "session"))):
            raise ValueError("private or signed source URL")
    # This validates catalog syntax only; connection-safe retrieval is separate.
    return raw


def verify(catalog):
    if not isinstance(catalog, dict):
        raise ValueError("catalog shape/version")
    version = catalog.get("schemaVersion")
    fields = {"schemaVersion", "sources"} if version == "1" else {"schemaVersion", "sources", "versions"}
    if version not in {"1", "2"} or set(catalog) != fields:
        raise ValueError("catalog shape/version")
    if version == "2" and not isinstance(catalog["versions"], list):
        raise ValueError("versions")
    sources = catalog["sources"]
    if not isinstance(sources, list) or not sources:
        raise ValueError("sources")
    ids, urls = set(), set()
    for source in sources:
        if not isinstance(source, dict) or set(source) != FIELDS:
            raise ValueError("source fields")
        sid = source["id"]
        if not isinstance(sid, str) or not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", sid) or sid in ids:
            raise ValueError("source identity")
        url = public_url(source["url"])
        if url in urls:
            raise ValueError("duplicate source URL")
        ids.add(sid)
        urls.add(url)
        if source["status"] != "registered" or source["current_version"] is not None:
            raise ValueError("registration cannot assert an executable version")
        if source["category"] not in CATEGORIES:
            raise ValueError("category")
        for field in ("organization", "title", "scope_notes"):
            text = source[field]
            if not isinstance(text, str) or not text.strip() or len(text.encode()) > 1000:
                raise ValueError("source description")
        discovery = source["discovery"]
        if (not isinstance(discovery, dict) or set(discovery) != {"date", "result"}
                or not isinstance(discovery["date"], str)
                or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", discovery["date"])
                or discovery["result"] not in {"readable", "unavailable", "pending"}):
            raise ValueError("discovery metadata")
    return len(sources)


FILES = {"policy.json", "provenance.json", "coverage.json", "cases.json", "fixtures.json", "README.md"}
HASH = re.compile(r"sha256:[0-9a-f]{64}")
IDENTIFIER = re.compile(r"[a-z][a-z0-9-]{0,63}")
VERSION = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\.[1-9][0-9]{0,5}")


def load_json(path):
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 1024 * 1024:
        raise ValueError("bounded regular JSON file required")
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("non-finite number")))


def exact(value, fields):
    if not isinstance(value, dict) or set(value) != set(fields.split()):
        raise ValueError("sidecar fields")


def bounded_text(value, maximum=4096):
    return isinstance(value, str) and bool(value.strip()) and len(value.encode("utf-8")) <= maximum


def verify_browser_observation(observation):
    exact(observation, "method selector element_index matched_elements text_property normalization text_sha256 text_bytes http_response_sha256 response_linkage authentication")
    if (observation["method"] != "browser-dom"
            or observation["text_property"] != "innerText" or observation["normalization"] != "none"
            or observation["authentication"] != "public-no-sign-in"
            or observation["http_response_sha256"] is not None
            or observation["response_linkage"] != "not-established"
            or not bounded_text(observation["selector"], 1000)):
        raise ValueError("browser observation assertion")
    count, index, size = [observation[k] for k in ["matched_elements", "element_index", "text_bytes"]]
    if (type(count) is not int or not 1 <= count <= 256
            or type(index) is not int or not 0 <= index < count
            or type(size) is not int or not 1 <= size <= 1024 * 1024
            or not isinstance(observation["text_sha256"], str)
            or not re.fullmatch(r"[0-9a-f]{64}", observation["text_sha256"])):
        raise ValueError("browser observation identity")


def digest(value):
    # Policy and input identities here contain only ASCII keys and string values.
    # This restricted JSON domain has the same serialization as RFC 8785; general
    # numbers/Unicode keys require the released CLI, never this helper.
    def check(item):
        if isinstance(item, str):
            item.encode("utf-8")
        elif isinstance(item, list):
            for child in item:
                check(child)
        elif isinstance(item, dict) and all(isinstance(k, str) and k.isascii() for k in item):
            for child in item.values():
                check(child)
        else:
            raise ValueError("unsupported canonical identity value")
    check(value)
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def version_path(root, source_id, version_id):
    if not isinstance(source_id, str) or not IDENTIFIER.fullmatch(source_id):
        raise ValueError("version source identity")
    if not isinstance(version_id, str) or not VERSION.fullmatch(version_id):
        raise ValueError("version identity")
    folder = root / "policies" / source_id / "versions" / version_id
    if any(p.is_symlink() for p in [folder, *folder.parents] if p != root.parent):
        raise ValueError("symlink version path")
    return folder


def verify_version(entry, sources, root):
    exact(entry, "source_id version_id policy_digest state files cli_version case_count semantic_evaluation")
    sid, vid = entry["source_id"], entry["version_id"]
    if sid not in sources:
        raise ValueError("unregistered version source")
    folder = version_path(root, sid, vid)
    if (entry["state"] != "candidate" or entry["semantic_evaluation"] != "not_evaluated"
            or entry["cli_version"] != "0.7.0"):
        raise ValueError("unqualified publication/review assertion")
    if not isinstance(entry["files"], dict) or set(entry["files"]) != FILES:
        raise ValueError("version manifest files")
    if not folder.is_dir() or {p.name for p in folder.iterdir()} != FILES:
        raise ValueError("unexpected or missing version file")
    for name, expected in entry["files"].items():
        path = folder / name
        if (not isinstance(expected, str) or not HASH.fullmatch(expected) or path.is_symlink()
                or not path.is_file() or path.stat().st_size > 1024 * 1024
                or "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest() != expected):
            raise ValueError("immutable file identity")
    policy, provenance, coverage, suite, fixtures = [load_json(folder / name) for name in
        ["policy.json", "provenance.json", "coverage.json", "cases.json", "fixtures.json"]]
    pd = entry["policy_digest"]
    if not isinstance(pd, str) or not HASH.fullmatch(pd) or digest(policy) != pd:
        raise ValueError("policy identity")
    exact(policy, "apiVersion kind metadata spec")
    if policy["apiVersion"] != "policy.antaeus.io/v0alpha1" or policy["kind"] != "Policy":
        raise ValueError("portable policy contract")
    if policy["spec"].get("defaultOutcome") != "review":
        raise ValueError("candidate must default to review")
    rules = policy["spec"]["rules"]
    rule_ids = [r["id"] for r in rules]
    if not rules or len(set(rule_ids)) != len(rule_ids):
        raise ValueError("unique nonempty rules")
    for rule in rules:
        exact(rule, "id when outcome")
        if not IDENTIFIER.fullmatch(rule["id"]) or not rule["when"].strip() or rule["outcome"] not in {"allow", "review", "deny"}:
            raise ValueError("rule shape")
    provenance_fields = "schema_version source_id version_id source_url final_url language region retrieved_at source_effective_date source_snapshot_retained authoring policy_digest cli_version scope semantic_evaluation"
    if (not isinstance(provenance, dict) or not isinstance(provenance.get("schema_version"), str)
            or provenance["schema_version"] not in {"1", "2"}):
        raise ValueError("provenance format")
    if provenance["schema_version"] == "1":
        exact(provenance, provenance_fields + " response_sha256 extracted_text_sha256 extractor")
    else:
        exact(provenance, provenance_fields + " observation")
        verify_browser_observation(provenance["observation"])
    exact(coverage, "schema_version source_id version_id policy_digest input_fields clauses case_clauses dependencies limitations")
    if coverage["schema_version"] != "1":
        raise ValueError("coverage format")
    for sidecar in [provenance, coverage]:
        if (sidecar["source_id"] != sid
                or sidecar["version_id"] != vid or sidecar["policy_digest"] != pd):
            raise ValueError("sidecar identity")
    if (provenance["source_url"] != sources[sid]["url"] or not public_url(provenance["final_url"])
            or provenance["source_snapshot_retained"] is not False or provenance["cli_version"] != "0.7.0"
            or provenance["semantic_evaluation"] != "not_evaluated"):
        raise ValueError("provenance assertion")
    exact(provenance["authoring"], "method tool model revision")
    if provenance["authoring"]["method"] != "authored-candidate":
        raise ValueError("unqualified generation assertion")
    for key in ["language", "region", "scope"] + (["extractor"] if provenance["schema_version"] == "1" else []):
        if not bounded_text(provenance[key]):
            raise ValueError("provenance text identity")
    for key in ["tool", "model", "revision"]:
        if not bounded_text(provenance["authoring"][key]):
            raise ValueError("authoring text identity")
    observed = provenance["retrieved_at"]
    effective = provenance["source_effective_date"]
    try:
        if not isinstance(observed, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T.+", observed):
            raise ValueError()
        parsed = datetime.fromisoformat(observed)
        if parsed.utcoffset() is None:
            raise ValueError()
        if effective is not None:
            if not isinstance(effective, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", effective):
                raise ValueError()
            date.fromisoformat(effective)
    except ValueError:
        raise ValueError("provenance observation/effective date") from None
    for key in (["response_sha256", "extracted_text_sha256"] if provenance["schema_version"] == "1" else []):
        if not isinstance(provenance[key], str) or not re.fullmatch(r"[0-9a-f]{64}", provenance[key]):
            raise ValueError("source digest")
    if coverage["input_fields"] != ["text"] or not coverage["limitations"]:
        raise ValueError("text-only scope required")
    clause_ids, converted = set(), set()
    for clause in coverage["clauses"]:
        exact(clause, "id status rule_ids reason")
        cid, refs = clause["id"], clause["rule_ids"]
        if (not isinstance(cid, str) or not cid or cid in clause_ids or not isinstance(refs, list)
                or len(set(refs)) != len(refs) or not set(refs) <= set(rule_ids) or not clause["reason"].strip()
                or clause["status"] not in {"converted", "needs_context", "not_convertible", "out_of_scope"}
                or bool(refs) != (clause["status"] == "converted")):
            raise ValueError("clause coverage")
        clause_ids.add(cid)
        converted.update(refs)
    if converted != set(rule_ids):
        raise ValueError("unmapped rule")
    for dependency in coverage["dependencies"]:
        exact(dependency, "url status")
        public_url(dependency["url"])
        if dependency["status"] != "unresolved":
            raise ValueError("unverified dependency")
    identity = {"name": sid, "version": vid}
    if (suite.get("apiVersion") != "regression.antaeus.io/v0alpha1" or suite.get("kind") != "RegressionSuite"
            or fixtures.get("apiVersion") != "fixture.antaeus.io/v0alpha1" or fixtures.get("kind") != "FixtureSet"
            or suite["metadata"] != identity or fixtures["metadata"] != identity or suite["fixtureSet"] != identity
            or suite["policy"] != {"name": policy["metadata"]["name"], "digest": pd}):
        raise ValueError("suite and fixture identity")
    if type(entry["case_count"]) is not int or not 1 <= entry["case_count"] <= 256:
        raise ValueError("case count")
    if len(suite["cases"]) != entry["case_count"] or len(fixtures["cases"]) != entry["case_count"]:
        raise ValueError("case count mismatch")
    fixture_cases = {c["name"]: c for c in fixtures["cases"]}
    if len(fixture_cases) != len(fixtures["cases"]):
        raise ValueError("duplicate fixture case")
    names = set()
    for case in suite["cases"]:
        name = case["name"]
        if name in names or case["fixtureCase"] != name or name not in fixture_cases:
            raise ValueError("suite case identity")
        names.add(name)
        exact(case["input"], "text")
        if not isinstance(case["input"]["text"], str) or not case["input"]["text"].strip():
            raise ValueError("case text")
        fixture = fixture_cases[name]
        if (fixture["policyName"] != policy["metadata"]["name"] or fixture["policyDigest"] != pd
                or fixture["inputDigest"] != digest(case["input"])
                or [r["ruleId"] for r in fixture["ruleResults"]] != rule_ids):
            raise ValueError("fixture binding")
    expected_coverage = names - {"engine-provider-failure", "engine-deny-over-uncertainty"}
    if not isinstance(coverage["case_clauses"], dict) or set(coverage["case_clauses"]) != expected_coverage:
        raise ValueError("case coverage identity")
    for refs in coverage["case_clauses"].values():
        if not isinstance(refs, list) or not refs or not set(refs) <= clause_ids:
            raise ValueError("case coverage references")
    return folder


def verify_repository(root=ROOT, cli=None, base_ref=None):
    root = Path(root).resolve()
    catalog = load_json(root / "catalog.json")
    count = verify(catalog)
    sources = {s["id"]: s for s in catalog["sources"]}
    versions, seen = catalog.get("versions", []), set()
    folders = []
    for entry in versions:
        key = (entry["source_id"], entry["version_id"])
        if key in seen:
            raise ValueError("duplicate version")
        seen.add(key)
        folders.append(verify_version(entry, sources, root))
    actual = {p.relative_to(root).as_posix() for p in (root / "policies").glob("*/versions/*")}
    if actual != {p.relative_to(root).as_posix() for p in folders}:
        raise ValueError("unindexed version")
    if base_ref:
        old = json.loads(subprocess.check_output(["git", "show", base_ref + ":catalog.json"], cwd=root),
                         object_pairs_hook=unique_object)
        indexed = {(v["source_id"], v["version_id"]): v for v in versions}
        for previous in old.get("versions", []):
            current = indexed.get((previous["source_id"], previous["version_id"]))
            if current is None or current["files"] != previous["files"] or current["policy_digest"] != previous["policy_digest"]:
                raise ValueError("published version altered or removed")
    if cli:
        version = subprocess.check_output([str(cli), "version"], text=True, timeout=10).strip()
        if not version.startswith("antaeus v0.7.0 ("):
            raise ValueError("released CLI v0.7.0 required")
        for folder, entry in zip(folders, versions):
            identity = json.loads(subprocess.check_output([str(cli), "validate", str(folder / "policy.json")], timeout=30))
            if identity["digest"] != entry["policy_digest"]:
                raise ValueError("CLI policy digest mismatch")
            result = json.loads(subprocess.check_output([str(cli), "test", "--policy", str(folder / "policy.json"),
                "--suite", str(folder / "cases.json"), "--fixture-set", str(folder / "fixtures.json")], timeout=30))
            if result.get("passed") is not True or len(result.get("results", [])) != entry["case_count"]:
                raise ValueError("CLI regression failed")
    return count, len(versions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli", help="Explicit path to released Antaeus v0.7.0 CLI; runs offline fixture tests")
    parser.add_argument("--base-ref", help="Trusted local Git ref whose published versions must remain unchanged")
    args = parser.parse_args()
    sources, versions = verify_repository(cli=args.cli, base_ref=args.base_ref)
    print(f"Verified {sources} registered source URLs; {versions} candidate artifacts; 0 recommended/servable versions.")
