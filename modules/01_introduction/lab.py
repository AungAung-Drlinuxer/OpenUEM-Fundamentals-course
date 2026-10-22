#!/usr/bin/env python3
"""Module 01 lab — OpenUEM concepts, checked offline and deterministically.

Every exercise asserts the concept it teaches. Output is stable across runs:
no randomness, no wall-clock reads, no temporary paths.
"""

AGENTS = [
    {"name": "ws-001", "state": "Enabled", "platform": "Windows", "last_report_min": 12},
    {"name": "ws-002", "state": "Waiting for admission", "platform": "Windows", "last_report_min": 25},
    {"name": "srv-010", "state": "Enabled", "platform": "Linux", "last_report_min": 95},
    {"name": "mac-004", "state": "Disabled", "platform": "macOS", "last_report_min": 600},
    {"name": "ws-003", "state": "Enabled", "platform": "Windows", "last_report_min": 300},
]

COMPONENT_PORTS = {
    "console": 1323,
    "console-auth": 1324,
    "nats": 4433,
    "ocsp-responder": 8000,
    "agent-sftp": 2022,
    "agent-vnc-proxy": 1443,
    "postgresql": 5432,
}

CAPABILITIES = {
    "package-deploy": {"Windows", "Linux", "macOS"},
    "registry-key": {"Windows"},
    "powershell-script": {"Windows"},
    "shell-script": {"Linux", "macOS"},
    "msi-package": {"Windows"},
    "bitlocker-status": {"Windows"},
    "remote-assistance": {"Windows", "Linux", "macOS"},
    "wol": {"Windows", "Linux"},
}

ALLOWED_TRANSITIONS = {
    "Waiting for admission": {"Enabled", "Removed"},
    "Enabled": {"Disabled", "Removed"},
    "Disabled": {"Enabled", "Removed"},
    "Removed": set(),
}

PORT_PLAN = [
    ("console", 1323),
    ("console-auth", 1324),
    ("nats", 4433),
    ("ocsp-responder", 8000),
    ("agent-sftp", 2022),
    ("agent-vnc-proxy", 1443),
    ("postgresql", 5432),
    ("console-old", 1323),
]

INCIDENTS = [
    {"id": "INC-104", "severity": "low", "age_min": 400},
    {"id": "INC-101", "severity": "critical", "age_min": 15},
    {"id": "INC-103", "severity": "high", "age_min": 30},
    {"id": "INC-102", "severity": "critical", "age_min": 5},
]


def exercise_1():
    """Validate lifecycle transitions against the allowed map."""
    requested = [
        ("Waiting for admission", "Enabled"),
        ("Waiting for admission", "Disabled"),
        ("Enabled", "Disabled"),
        ("Disabled", "Enabled"),
        ("Removed", "Enabled"),
    ]
    invalid = [f"{src}->{dst}" for src, dst in requested
               if dst not in ALLOWED_TRANSITIONS[src]]
    assert invalid == ["Waiting for admission->Disabled", "Removed->Enabled"], invalid
    print(f"[OK] exercise_1 — lifecycle: {len(requested) - len(invalid)}/{len(requested)} "
          f"transitions valid; rejected={','.join(invalid)}")


def exercise_2():
    """Look up the default port of each server component."""
    expected = {
        "console": 1323, "console-auth": 1324, "nats": 4433,
        "ocsp-responder": 8000, "agent-sftp": 2022,
        "agent-vnc-proxy": 1443, "postgresql": 5432,
    }
    assert COMPONENT_PORTS == expected
    print("[OK] exercise_2 — component ports: "
          + ", ".join(f"{k}={v}" for k, v in sorted(COMPONENT_PORTS.items())))


def exercise_3():
    """Classify agents by report freshness (fresh <=60, late <=240, stale >240)."""
    def bucket(minutes):
        if minutes <= 60:
            return "fresh"
        if minutes <= 240:
            return "late"
        return "stale"

    counts = {"fresh": 0, "late": 0, "stale": 0}
    for agent in AGENTS:
        counts[bucket(agent["last_report_min"])] += 1
    assert counts == {"fresh": 2, "late": 1, "stale": 2}, counts
    stale = sorted(a["name"] for a in AGENTS if bucket(a["last_report_min"]) == "stale")
    print(f"[OK] exercise_3 — freshness: fresh={counts['fresh']} late={counts['late']} "
          f"stale={counts['stale']}; stale={','.join(stale)}")


def exercise_4():
    """Answer capability questions from the platform matrix."""
    def supported(feature, platform):
        return platform in CAPABILITIES[feature]

    assert supported("registry-key", "Windows")
    assert not supported("registry-key", "Linux")
    assert supported("shell-script", "macOS")
    assert not supported("msi-package", "Linux")
    windows_only = sorted(feature for feature, platforms in CAPABILITIES.items()
                          if platforms == {"Windows"})
    print("[OK] exercise_4 — capability matrix: windows-only="
          + ",".join(windows_only)
          + f"; shell-script on macOS={supported('shell-script', 'macOS')}")


def exercise_5():
    """Detect duplicate ports in a proposed lab port plan."""
    seen = {}
    conflicts = []
    for service, port in PORT_PLAN:
        if port in seen:
            conflicts.append((port, seen[port], service))
        else:
            seen[port] = service
    assert conflicts == [(1323, "console", "console-old")], conflicts
    port, first, second = conflicts[0]
    print(f"[OK] exercise_5 — port conflict: {port} used by {first} and {second}; "
          f"unique_ports={len(seen)}")


def exercise_6():
    """Order incidents for triage: severity first, then age (oldest first)."""
    weight = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    ordered = sorted(INCIDENTS, key=lambda i: (weight[i["severity"]], -i["age_min"]))
    ids = [i["id"] for i in ordered]
    assert ids == ["INC-101", "INC-102", "INC-103", "INC-104"], ids
    print("[OK] exercise_6 — triage order: " + " > ".join(ids))


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
