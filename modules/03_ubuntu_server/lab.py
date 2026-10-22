#!/usr/bin/env python3
"""Module 03 lab — OpenUEM server installation and configuration.

Standard library only, fully offline, deterministic. Every fixture below is
simulated teaching data. No OpenUEM server, database or network is contacted,
and no wall-clock time or temporary path is printed.
"""

from __future__ import annotations

import datetime

PASS_LINE = "[PASS] All 6/6 exercises passed successfully."

# ---------------------------------------------------------------------------
# Exercise 1 fixtures — package catalogue mapped to component roles.
# ---------------------------------------------------------------------------
PACKAGE_ROLES = {
    "openuem-agent-worker": ("agent-report-worker", ()),
    "openuem-cert-manager": ("certificate-cli", ()),
    "openuem-cert-manager-worker": ("certificate-issuer-worker", ()),
    "openuem-console": ("console+auth-server", (1323, 1324)),
    "openuem-nats-service": ("nats-broker", (4433,)),
    "openuem-notification-worker": ("notification-worker", ()),
    "openuem-ocsp-responder": ("ocsp-responder", (8000,)),
    "openuem-server-updater": ("ini-generator-service", ()),
}

REQUESTED_PACKAGES = [
    "openuem-console",
    "openuem-nats-service",
    "openuem-agent-worker",
    "openuem-notification-worker",
    "openuem-cert-manager-worker",
    "openuem-ocsp-responder",
    "openuem-server-updater",
    "openuem-telemetry-sidecar",
]

# ---------------------------------------------------------------------------
# Exercise 2 fixtures — documented start order and the dependency pairs.
# ---------------------------------------------------------------------------
DOCUMENTED_ORDER = [
    "openuem-ocsp-responder",
    "openuem-nats-service",
    "openuem-server-updater",
    "openuem-agent-worker",
    "openuem-notification-worker",
    "openuem-cert-manager-worker",
    "openuem-console",
]

DEPENDENCIES = [
    ("openuem-ocsp-responder", "openuem-console"),
    ("openuem-nats-service", "openuem-agent-worker"),
    ("openuem-nats-service", "openuem-notification-worker"),
    ("openuem-server-updater", "openuem-agent-worker"),
    ("openuem-server-updater", "openuem-notification-worker"),
    ("openuem-server-updater", "openuem-cert-manager-worker"),
    ("openuem-server-updater", "openuem-console"),
]

PROPOSED_ORDER = [
    "openuem-console",
    "openuem-nats-service",
    "openuem-ocsp-responder",
    "openuem-server-updater",
    "openuem-agent-worker",
    "openuem-notification-worker",
    "openuem-cert-manager-worker",
]

# ---------------------------------------------------------------------------
# Exercise 3 fixtures — openuem.ini content and a deliberately broken copy.
# ---------------------------------------------------------------------------
INI_FIXTURE = """CACert = /etc/openuem-server/certificates/ca/ca.cer
CAKey = /etc/openuem-server/certificates/ca/ca.key
NATSCert = /etc/openuem-server/certificates/nats/nats.cer

[Console]
hostname = console.openuem.example
port = 1323
authport = 1324
reverseproxyserver = caddy.openuem.example
reverseproxyauthport = 443
domain = openuem.example

[JWT]
Key = 4f1c9a2b7d6e40518c3a9b2f7e6d5c41
"""

REQUIRED_INI = [
    ("Console", "hostname"),
    ("Console", "port"),
    ("Console", "authport"),
    ("JWT", "Key"),
]

INT_KEYS = ("port", "authport", "reverseproxyauthport")

# ---------------------------------------------------------------------------
# Exercise 4 fixtures — issue dates and validity windows.
# ---------------------------------------------------------------------------
YEARS_VALID_CASES = [
    (datetime.date(2026, 3, 15), 2),
    (datetime.date(2024, 2, 29), 1),
    (datetime.date(2026, 3, 15), 0),
]

# ---------------------------------------------------------------------------
# Exercise 5 and 6 fixtures — the inbound port plan of one server.
# ---------------------------------------------------------------------------
PORT_PLAN = [
    ("caddy", "https", 443, "tcp"),
    ("openuem-console", "console", 1323, "tcp"),
    ("openuem-console", "auth", 1324, "tcp"),
    ("openuem-nats-service", "nats", 4433, "tcp"),
    ("openuem-ocsp-responder", "ocsp", 8000, "tcp"),
]

EXTRA_LISTENERS = [
    ("probe-agent", "http", 1323, "tcp"),
    ("metrics-relay", "dns", 4433, "udp"),
]


# ---------------------------------------------------------------------------
# Helpers (names deliberately avoid the `exercise_N_` prefix).
# ---------------------------------------------------------------------------
def _parse_ini(text: str) -> dict:
    """Split an ini-style text into {section: {key: value}}.

    Keys that appear before any section header land in the "(global)" bucket,
    which is how a hand-edited openuem.ini usually starts.
    """
    sections: dict = {"(global)": {}}
    current = "(global)"
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current = line[1:-1].strip()
            sections.setdefault(current, {})
            continue
        if "=" in line:
            key, value = line.split("=", 1)
            sections[current][key.strip()] = value.strip()
    return sections


def _add_years(day: datetime.date, years: int) -> datetime.date:
    """Add a validity window in years, clamping 29 February to the 28th."""
    try:
        return day.replace(year=day.year + years)
    except ValueError:
        return day.replace(year=day.year + years, day=28)


def _order_violations(order: list, dependencies: list) -> list:
    """Return human-readable statements for every dependency the order breaks."""
    position = {name: index for index, name in enumerate(order)}
    violations = []
    for before, after in dependencies:
        if position[before] > position[after]:
            violations.append(f"{after} starts before {before}")
    return sorted(violations)


def _short(name: str) -> str:
    return name.replace("openuem-", "")


# ---------------------------------------------------------------------------
# Exercises
# ---------------------------------------------------------------------------
def exercise_1() -> None:
    """Map installed package names onto component roles and listening ports."""
    print("== Exercise 1 — package to role mapping ==")
    mapped, unmapped = [], []
    for name in sorted(REQUESTED_PACKAGES):
        if name in PACKAGE_ROLES:
            role, ports = PACKAGE_ROLES[name]
            port_text = ",".join(str(port) for port in ports) if ports else "-"
            mapped.append((name, role, port_text))
        else:
            unmapped.append(name)

    for name, role, port_text in mapped:
        print(f"  {name:<30}{role:<26}{port_text}")
    for name in unmapped:
        print(f"  {name:<30}{'UNKNOWN PACKAGE':<26}-")

    listeners = sorted(
        port for name in PACKAGE_ROLES for port in PACKAGE_ROLES[name][1]
    )
    print(f"  mapped={len(mapped)} unmapped={len(unmapped)}")
    print("  listener ports: " + ",".join(str(port) for port in listeners))

    assert len(mapped) == 7
    assert unmapped == ["openuem-telemetry-sidecar"]
    assert PACKAGE_ROLES["openuem-console"][1] == (1323, 1324)
    assert PACKAGE_ROLES["openuem-nats-service"][1] == (4433,)
    assert PACKAGE_ROLES["openuem-ocsp-responder"][1] == (8000,)
    assert listeners == [1323, 1324, 4433, 8000]
    print("[OK] exercise_1 — resolved 7 packages to roles and flagged 1 unknown package")


def exercise_2() -> None:
    """Validate a proposed start order against the documented dependency pairs."""
    print("== Exercise 2 — service start-order validation ==")
    print("  documented order: " + " -> ".join(_short(name) for name in DOCUMENTED_ORDER))
    documented = _order_violations(DOCUMENTED_ORDER, DEPENDENCIES)
    print(f"  documented order violations: {len(documented)}")

    print("  proposed order: " + ", ".join(_short(name) for name in PROPOSED_ORDER))
    proposed = _order_violations(PROPOSED_ORDER, DEPENDENCIES)
    print(f"  proposed order violations: {len(proposed)}")
    for line in proposed:
        print(f"    - {line}")

    assert documented == []
    assert len(proposed) == 2
    assert "openuem-console starts before openuem-server-updater" in proposed
    assert "openuem-console starts before openuem-ocsp-responder" in proposed
    # The documented order is a superset of every service the course names.
    assert set(DOCUMENTED_ORDER) == set(name for pair in DEPENDENCIES for name in pair)
    print(f"[OK] exercise_2 — documented order is valid and the proposed order breaks {len(proposed)} dependencies")


def exercise_3() -> None:
    """Parse the openuem.ini fixture into sections and validate required keys."""
    print("== Exercise 3 — openuem.ini section parsing ==")
    sections = _parse_ini(INI_FIXTURE)
    print("  sections: " + ", ".join(sorted(sections)))

    global_keys = sorted(sections["(global)"])
    print("  (global) keys: " + ", ".join(global_keys))

    console = sections["Console"]
    for key in INT_KEYS:
        if key in console:
            console[key] = int(console[key])
    print(
        "  Console: hostname={hostname} port={port} authport={authport} domain={domain}".format(
            **console
        )
    )
    print(
        "  Console reverse proxy: {server}:{port}".format(
            server=console["reverseproxyserver"], port=console["reverseproxyauthport"]
        )
    )

    jwt_key = sections["JWT"]["Key"]
    print(f"  JWT key length={len(jwt_key)}")

    missing = [
        f"{section}.{key}"
        for section, key in REQUIRED_INI
        if key not in sections.get(section, {})
    ]
    print("  missing required entries: " + (", ".join(missing) if missing else "none"))

    broken = INI_FIXTURE.replace("authport = 1324\n", "").replace(
        "Key = 4f1c9a2b7d6e40518c3a9b2f7e6d5c41\n", ""
    )
    broken_sections = _parse_ini(broken)
    broken_missing = sorted(
        f"{section}.{key}"
        for section, key in REQUIRED_INI
        if key not in broken_sections.get(section, {})
    )
    print("  broken fixture missing: " + ", ".join(broken_missing))

    assert sorted(sections) == ["(global)", "Console", "JWT"]
    assert global_keys == ["CACert", "CAKey", "NATSCert"]
    assert console["port"] == 1323 and console["authport"] == 1324
    assert console["reverseproxyauthport"] == 443
    assert len(jwt_key) == 32
    assert missing == []
    assert broken_missing == ["Console.authport", "JWT.Key"]
    print("[OK] exercise_3 — parsed 3 ini sections and detected 2 missing entries in the broken copy")


def exercise_4() -> None:
    """Turn a --years-valid window into an expiry date and a term length."""
    print("== Exercise 4 — certificate expiry from --years-valid ==")
    accepted, rejected = [], []
    for issued, years in YEARS_VALID_CASES:
        if years < 1:
            rejected.append((issued, years))
            print(f"  issued={issued.isoformat()} years={years} rejected (window must be >= 1 year)")
            continue
        expiry = _add_years(issued, years)
        term = (expiry - issued).days
        note = " leap_day_clamped=yes" if issued.month == 2 and issued.day == 29 else ""
        accepted.append((issued, years, expiry, term))
        print(f"  issued={issued.isoformat()} years={years} expires={expiry.isoformat()} term_days={term}{note}")

    print(f"  accepted={len(accepted)} rejected={len(rejected)}")

    assert len(accepted) == 2 and len(rejected) == 1
    assert accepted[0][2] == datetime.date(2028, 3, 15)
    assert accepted[0][3] == 731
    assert accepted[1][2] == datetime.date(2025, 2, 28)
    assert accepted[1][3] == 365
    # A longer window always expires later.
    assert _add_years(datetime.date(2026, 3, 15), 3) > _add_years(datetime.date(2026, 3, 15), 2)
    print("[OK] exercise_4 — computed 2 expiry dates and rejected 1 invalid window")


def exercise_5() -> None:
    """Detect duplicate port/protocol pairs across console, auth, NATS and OCSP."""
    print("== Exercise 5 — port conflict detection ==")
    listeners = PORT_PLAN + EXTRA_LISTENERS
    print(f"  plan entries: {len(PORT_PLAN)} extra listeners: {len(EXTRA_LISTENERS)}")

    buckets: dict = {}
    for component, role, port, proto in listeners:
        buckets.setdefault((port, proto), []).append(f"{component}({role})")

    conflicts = {key: owners for key, owners in buckets.items() if len(owners) > 1}
    print(f"  conflicts ({len(conflicts)}):")
    for port, proto in sorted(conflicts):
        print(f"    {port}/{proto} -> " + ", ".join(sorted(conflicts[(port, proto)])))

    shared_number = sorted(
        port for (port, proto) in buckets if proto == "udp" and (port, "tcp") in buckets
    )
    print(
        "  same number, other protocol (no conflict): "
        + ", ".join(f"{port}/udp vs {port}/tcp" for port in shared_number)
    )

    privileged = sorted({port for _, _, port, _ in listeners if port < 1024})
    print("  privileged ports (<1024): " + ",".join(str(port) for port in privileged))

    assert len(PORT_PLAN) == 5
    assert len(conflicts) == 1
    assert (1323, "tcp") in conflicts
    assert sorted(conflicts[(1323, "tcp")]) == ["openuem-console(console)", "probe-agent(http)"]
    assert shared_number == [4433]
    assert privileged == [443]
    print("[OK] exercise_5 — found 1 real conflict and ignored 1 same-number/different-protocol pair")


def exercise_6() -> None:
    """Generate an ordered firewall rule set from the inbound port plan."""
    print("== Exercise 6 — firewall rules from the port plan ==")
    rules = sorted(
        (port, proto, f"ufw allow {port}/{proto} comment '{component} {role}'")
        for component, role, port, proto in PORT_PLAN
    )
    print("  ufw default deny incoming")
    for _, _, line in rules:
        print(f"  {line}")

    again = sorted(
        (port, proto, f"ufw allow {port}/{proto} comment '{component} {role}'")
        for component, role, port, proto in PORT_PLAN
    )
    ports = [port for port, _, _ in rules]
    print(f"  rules={len(rules)} lowest_port={ports[0]} highest_port={ports[-1]}")

    assert rules == again, "regenerating the rule set must be idempotent"
    assert ports == sorted([443, 1323, 1324, 4433, 8000])
    assert all("comment" in line for _, _, line in rules)
    # Every listening port in the plan is covered exactly once.
    assert len({port for port, _, _ in rules}) == len(PORT_PLAN)
    print("[OK] exercise_6 — generated 5 idempotent firewall rules covering every planned port")


def main() -> None:
    exercises = (
        exercise_1,
        exercise_2,
        exercise_3,
        exercise_4,
        exercise_5,
        exercise_6,
    )
    for index, exercise in enumerate(exercises):
        if index:
            print()
        exercise()
    print()
    print(PASS_LINE)


if __name__ == "__main__":
    main()
