#!/usr/bin/env python3
"""Module 02 lab — PostgreSQL preparation checks, offline and deterministic."""

ENV_TEMPLATE = {
    "DATABASE_DB_NAME": "openuem",
    "DATABASE_PORT": "5432",
    "DATABASE_USER": "openuem_app",
    "DATABASE_PASSWORD": "change-this-dbpassword",
    "OPENUEM_DATABASE_URL": "postgres://openuem_app:change-this-dbpassword@openuem-db:5432/openuem",
    "OPENUEM_DOMAIN": "openuem.example",
    "CONSOLE_HOST": "console.openuem.example",
}

REQUIRED_ENV = (
    "DATABASE_DB_NAME",
    "DATABASE_PORT",
    "DATABASE_USER",
    "DATABASE_PASSWORD",
    "OPENUEM_DATABASE_URL",
)

RESERVED = {
    " ": "%20", "/": "%2F", ":": "%3A", "@": "%40",
    "=": "%3D", "?": "%3F", "#": "%23", "&": "%26",
}

HBA_RULES = [
    {"type": "local", "database": "all", "user": "all", "address": "", "method": "peer"},
    {"type": "host", "database": "all", "user": "all", "address": "127.0.0.1/32", "method": "scram-sha-256"},
    {"type": "host", "database": "all", "user": "all", "address": "::1/128", "method": "scram-sha-256"},
]

ERRORS = [
    "FATAL:  password authentication failed for user \"openuem_app\"",
    "FATAL:  no pg_hba.conf entry for host \"10.0.0.5\", user \"openuem_app\", database \"openuem\"",
    "could not connect to server: Connection refused",
    "FATAL:  database \"openuem\" does not exist",
]

ACL = "openuem_app=UC/openuem_app,postgres=CTc/postgres"


def exercise_1():
    """Report which required .env keys are missing."""
    env = dict(ENV_TEMPLATE)
    del env["DATABASE_PASSWORD"]
    del env["OPENUEM_DATABASE_URL"]
    missing = [k for k in REQUIRED_ENV if not env.get(k)]
    assert missing == ["DATABASE_PASSWORD", "OPENUEM_DATABASE_URL"], missing
    print(f"[OK] exercise_1 — env validation: {len(REQUIRED_ENV) - len(missing)}/"
          f"{len(REQUIRED_ENV)} required keys present; missing={','.join(missing)}")


def exercise_2():
    """Percent-encode a password and assemble the connection URI."""
    password = "te=st@lab"
    encoded = "".join(RESERVED.get(ch, ch) for ch in password)
    assert encoded == "te%3Dst%40lab", encoded
    uri = f"postgres://openuem_app:{encoded}@localhost:5432/openuem"
    assert uri == "postgres://openuem_app:te%3Dst%40lab@localhost:5432/openuem", uri
    print(f"[OK] exercise_2 — uri encoding: {password} -> {encoded}; "
          f"host=localhost port=5432 db=openuem")


def exercise_3():
    """Resolve the authentication method for a TCP connection."""
    def method_for(host_type, address):
        for rule in HBA_RULES:
            if rule["type"] != host_type:
                continue
            if host_type == "local":
                return rule["method"]
            if rule["address"] == address:
                return rule["method"]
        return "reject"

    assert method_for("host", "127.0.0.1/32") == "scram-sha-256"
    assert method_for("host", "10.0.0.5/32") == "reject"
    assert method_for("local", "") == "peer"
    print("[OK] exercise_3 — pg_hba: 127.0.0.1/32=scram-sha-256, "
          "10.0.0.5/32=reject, local=peer")


def exercise_4():
    """Classify connection errors by their root cause."""
    def classify(message):
        if "password authentication failed" in message:
            return "credentials"
        if "no pg_hba.conf entry" in message:
            return "hba-rule"
        if "Connection refused" in message:
            return "service-or-port"
        if "does not exist" in message:
            return "wrong-database"
        return "unknown"

    causes = [classify(e) for e in ERRORS]
    assert causes == ["credentials", "hba-rule", "service-or-port", "wrong-database"], causes
    print("[OK] exercise_4 — error causes: " + ",".join(causes))


def exercise_5():
    """Decide whether a role may create tables in schema public."""
    def privileges(acl, role):
        for entry in acl.split(","):
            name, _, rights = entry.partition("=")
            if name == role:
                return rights.split("/")[0]
        return ""

    rights = privileges(ACL, "openuem_app")
    other = privileges(ACL, "readonly_user")
    assert "C" in rights and "U" in rights
    assert not other
    print(f"[OK] exercise_5 — schema privileges: openuem_app={rights} "
          f"create={'C' in rights}; readonly_user=none")


def exercise_6():
    """Validate the order of a backup and restore runbook."""
    steps = [
        ("stop OpenUEM services", 1),
        ("pg_dump -Fc openuem", 2),
        ("createdb openuem_restore", 3),
        ("pg_restore -d openuem_restore", 4),
        ("start OpenUEM services", 5),
    ]
    ordered = [name for name, _ in sorted(steps, key=lambda s: s[1])]
    assert ordered[0].startswith("stop")
    assert ordered[-1].startswith("start")
    assert ordered.index("pg_dump -Fc openuem") < ordered.index("pg_restore -d openuem_restore")
    print("[OK] exercise_6 — runbook order: " + " -> ".join(ordered))


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
