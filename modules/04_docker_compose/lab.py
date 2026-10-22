#!/usr/bin/env python3
"""Module 04 lab — Docker/Podman deployment checks, offline and deterministic."""

ENV = {
    "DATABASE_DB_NAME": "openuem",
    "DATABASE_PORT": "5432",
    "DATABASE_USER": "openuem",
    "DATABASE_PASSWORD": "db-secret",
    "OPENUEM_DATABASE_URL": "postgres://openuem:db-secret@openuem-db:5432/openuem",
    "OPENUEM_ORGNAME": "Example Org",
    "OPENUEM_COUNTRY": "MM",
    "OPENUEM_DOMAIN": "openuem.example",
    "CONSOLE_HOST": "console.openuem.example",
    "CONSOLE_PORT": "1323",
    "CONSOLE_AUTH_PORT": "1324",
    "CONSOLE_JWT_KEY": "",
    "NATS_HOST": "nats.openuem.example",
    "NATS_PORT": "4433",
    "OPENUEM_NATS_SERVERS": "nats.openuem.example:4433",
    "OCSP_URL": "http://ocsp.openuem.example:8000",
    "OCSP_HOST": "ocsp.openuem.example",
    "OCSP_PORT": "8000",
}

REQUIRED = (
    "DATABASE_DB_NAME", "DATABASE_PORT", "DATABASE_USER", "DATABASE_PASSWORD",
    "OPENUEM_DATABASE_URL", "OPENUEM_ORGNAME", "OPENUEM_COUNTRY", "OPENUEM_DOMAIN",
    "CONSOLE_HOST", "CONSOLE_PORT", "CONSOLE_AUTH_PORT", "CONSOLE_JWT_KEY",
    "NATS_HOST", "NATS_PORT", "OPENUEM_NATS_SERVERS", "OCSP_URL", "OCSP_HOST",
    "OCSP_PORT",
)

DEPENDENCIES = {
    "openuem-db": [],
    "nats": ["openuem-db"],
    "ocsp": ["openuem-db"],
    "cert-manager": ["openuem-db"],
    "agent-worker": ["openuem-db", "nats"],
    "console": ["openuem-db", "nats", "agent-worker"],
}

PROXY_CASES = [
    {"REVERSE_PROXY_HOST": "", "REVERSE_PROXY_CONSOLE_PORT": "", "REVERSE_PROXY_AUTH_PORT": ""},
    {"REVERSE_PROXY_HOST": "console.openuem.example",
     "REVERSE_PROXY_CONSOLE_PORT": "443", "REVERSE_PROXY_AUTH_PORT": "4443"},
    {"REVERSE_PROXY_HOST": "console.openuem.example",
     "REVERSE_PROXY_CONSOLE_PORT": "443", "REVERSE_PROXY_AUTH_PORT": ""},
]

TEARDOWN = {
    "docker compose stop": "containers stopped, data kept",
    "docker compose down": "containers removed, data kept",
    "docker compose down -v": "containers and volumes removed, data lost",
}


def exercise_1():
    """Validate required .env keys before the stack starts."""
    missing = [k for k in REQUIRED if not ENV.get(k)]
    assert missing == ["CONSOLE_JWT_KEY"], missing
    print(f"[OK] exercise_1 — env: {len(REQUIRED) - len(missing)}/{len(REQUIRED)} "
          f"required keys set; missing={','.join(missing)}")


def exercise_2():
    """Apply the JWT key policy: 32+ characters, never the shipped default."""
    candidates = ["averylongsecret", "", "9f2c41ab7d3e58c0a6b1f4d92e7c0a38"]
    verdicts = []
    for key in candidates:
        if not key:
            verdicts.append("empty")
        elif key == "averylongsecret":
            verdicts.append("default")
        elif len(key) < 32:
            verdicts.append("too-short")
        else:
            verdicts.append("ok")
    assert verdicts == ["default", "empty", "ok"], verdicts
    print("[OK] exercise_2 — jwt key policy: " + ",".join(verdicts)
          + f"; accepted_length={len(candidates[-1])}")


def exercise_3():
    """Build one hosts entry for every OpenUEM name in the lab."""
    ip = "192.168.1.43"
    names = [ENV["NATS_HOST"], ENV["OCSP_HOST"], ENV["CONSOLE_HOST"], ENV["NATS_HOST"]]
    unique = sorted(set(names))
    entry = f"{ip}  " + "  ".join(unique)
    assert unique == ["console.openuem.example", "nats.openuem.example",
                      "ocsp.openuem.example"], unique
    assert entry.startswith("192.168.1.43") and "127.0.0.1" not in entry
    print(f"[OK] exercise_3 — hosts entry: {entry}")


def exercise_4():
    """Validate reverse proxy settings: host and both ports move together."""
    def valid(case):
        host = case["REVERSE_PROXY_HOST"]
        console_port = case["REVERSE_PROXY_CONSOLE_PORT"]
        auth_port = case["REVERSE_PROXY_AUTH_PORT"]
        if not host:
            return not console_port and not auth_port
        return bool(console_port) and bool(auth_port)

    results = [valid(case) for case in PROXY_CASES]
    assert results == [True, True, False], results
    print("[OK] exercise_4 — reverse proxy: no-proxy=ok, full=ok, "
          "host-without-auth-port=invalid")


def exercise_5():
    """Derive a startup order from the service dependency graph."""
    order = []
    pending = dict(DEPENDENCIES)
    while pending:
        ready = sorted(name for name, deps in pending.items()
                       if all(d in order for d in deps))
        assert ready, f"dependency cycle among {sorted(pending)}"
        order.extend(ready)
        for name in ready:
            del pending[name]
    assert order[0] == "openuem-db", order
    assert order.index("nats") < order.index("agent-worker") < order.index("console")
    print("[OK] exercise_5 — startup order: " + " -> ".join(order))


def exercise_6():
    """Classify teardown commands by whether they destroy data."""
    lossless = sorted(cmd for cmd, effect in TEARDOWN.items() if "lost" not in effect)
    destructive = sorted(cmd for cmd, effect in TEARDOWN.items() if "lost" in effect)
    assert lossless == ["docker compose down", "docker compose stop"], lossless
    assert destructive == ["docker compose down -v"], destructive
    print("[OK] exercise_6 — teardown: data-safe=" + " | ".join(lossless)
          + "; data-loss=" + " | ".join(destructive))


def main():
    exercise_1()
    exercise_2()
    exercise_3()
    exercise_4()
    exercise_5()
    exercise_6()
    print("[PASS] All 6/6 exercises passed successfully.")


if __name__ == "__main__":
    main()
