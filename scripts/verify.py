"""Verify the registered-source catalog without network access or credentials."""
import ipaddress
import json
from pathlib import Path
import re
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
    if not isinstance(catalog, dict) or set(catalog) != {"schemaVersion", "sources"} or catalog["schemaVersion"] != "1":
        raise ValueError("catalog shape/version")
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


if __name__ == "__main__":
    catalog = json.loads((ROOT / "catalog.json").read_text(), object_pairs_hook=unique_object)
    print(f"Verified {verify(catalog)} registered source URLs; 0 executable policies.")
