#!/usr/bin/env python3
"""Module 08 — reporting and troubleshooting drills.

Pure standard library, fully offline, deterministic. Each exercise models one
operational task: report filtering, dashboard prioritisation, layered
connectivity evaluation, log classification, MTTR metrics, alert rule matching.
"""

from datetime import datetime

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

AGENTS = [
    {"name": "ws-001", "site": "yangon", "platform": "windows", "state": "Enabled",
     "hours": 2, "antivirus": "enabled"},
    {"name": "ws-002", "site": "yangon", "platform": "windows", "state": "Disabled",
     "hours": 30, "antivirus": "disabled"},
    {"name": "lnx-003", "site": "yangon", "platform": "linux", "state": "Enabled",
     "hours": 1, "antivirus": "enabled"},
    {"name": "mac-004", "site": "mandalay", "platform": "macos", "state": "Enabled",
     "hours": 5, "antivirus": "enabled"},
    {"name": "ws-005", "site": "mandalay", "platform": "windows",
     "state": "Waiting for admission", "hours": 0, "antivirus": "enabled"},
    {"name": "lnx-006", "site": "yangon", "platform": "linux", "state": "Enabled",
     "hours": 80, "antivirus": "enabled"},
]

SOFTWARE = [
    {"name": "7-Zip", "publisher": "Igor Pavlov", "installs": 4},
    {"name": "Firefox", "publisher": "Mozilla", "installs": 5},
    {"name": "VLC", "publisher": "VideoLAN", "installs": 3},
    {"name": "WinGet", "publisher": "Microsoft", "installs": 2},
]

DASHBOARD = {
    "red": [
        {"key": "agents_not_reporting", "count": 4, "severity": "critical"},
        {"key": "antivirus_disabled", "count": 7, "severity": "high"},
        {"key": "pending_updates", "count": 23, "severity": "medium"},
        {"key": "agent_app_updates", "count": 11, "severity": "low"},
    ],
    "green": {"users": 42, "apps": 96, "tags": 6},
    "blue": {"console": "ok", "nats": "ok", "workers": "degraded",
             "ocsp": "ok", "postgres": "ok"},
}

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
REFRESH_SECONDS = 300

LAYERS = [
    "endpoint->nats:4433",
    "nats->agent-worker",
    "agent-worker->postgres:5432",
    "console:1323/1324",
    "console->ocsp:8000",
]

SCENARIOS = [
    ("healthy", 0),
    ("nats_down", 1),
    ("db_down", 3),
    ("ocsp_down", 5),
]

LOG_LINES = [
    ("agent", "level=error msg=cannot load ca.cer from certificates folder"),
    ("agent", "level=error msg=x509 certificate has expired"),
    ("nats", "level=error msg=connection refused 192.168.1.43:4433"),
    ("console", "level=warn msg=jwt signature mismatch for session 8812"),
    ("worker", "level=error msg=postgres: password authentication failed for user test"),
    ("agent", "level=error msg=lookup nats.openuem.example: no such host"),
    ("agent", "level=error msg=sftp upload of inventory failed on port 2022"),
    ("ocsp", "level=info msg=ocsp responder returned good"),
    ("agent", "level=info msg=agent report sent ok"),
    ("console", "level=error msg=token expired, user must reauthenticate"),
    ("agent", "level=error msg=time skew 420s detected during TLS handshake"),
]

LOG_ORDER = ["certificate", "dns", "auth", "database", "nats", "sftp", "other"]

LOG_KEYWORDS = {
    "certificate": ("certificate", "x509", "tls", "ca.cer"),
    "dns": ("no such host", "dns", "lookup"),
    "auth": ("jwt", "token", "401"),
    "database": ("postgres", "sql", "database"),
    "nats": ("nats", "4433"),
    "sftp": ("sftp", "2022"),
}

INCIDENTS = [
    ("inc-01", "certificate", "ws-001", "2026-03-02T09:00:00", "2026-03-02T10:30:00"),
    ("inc-02", "certificate", "lnx-003", "2026-03-05T14:00:00", "2026-03-05T15:00:00"),
    ("inc-03", "nats", "ws-005", "2026-03-03T08:00:00", "2026-03-03T12:00:00"),
    ("inc-04", "database", "ws-001", "2026-03-04T11:00:00", "2026-03-04T11:20:00"),
    ("inc-05", "auth", "ws-002", "2026-03-06T09:00:00", "2026-03-06T11:00:00"),
    ("inc-06", "dns", "ws-005", "2026-03-07T10:00:00", "2026-03-07T10:45:00"),
]

RULES = [
    {"name": "agent_silent", "metric": "hours_since_report", "op": ">",
     "threshold": 24, "for_samples": 2, "severity": "critical"},
    {"name": "pending_updates_high", "metric": "pending_updates", "op": ">=",
     "threshold": 10, "for_samples": 1, "severity": "high"},
    {"name": "disk_low", "metric": "free_disk_percent", "op": "<",
     "threshold": 10, "for_samples": 2, "severity": "high"},
]

SAMPLES = {
    "AP-1": {"hours_since_report": [12, 26, 30]},
    "AP-2": {"hours_since_report": [12, 26]},
    "AP-3": {"pending_updates": [4, 12]},
    "AP-4": {"free_disk_percent": [8, 6]},
    "AP-5": {"free_disk_percent": [5, 14]},
    "AP-6": {"pending_updates": [2]},
}


# --------------------------------------------------------------------------
# Exercise 1 — report row filtering
# --------------------------------------------------------------------------

def exercise_1():
    """Filter rows per view and keep the filter definition with the result."""
    filters = {
        "agents": {"site": "yangon", "state": "Enabled"},
        "computers": {"platform": ("windows", "linux"), "max_hours": 24,
                      "exclude_state": "Waiting for admission"},
        "security": {"antivirus": "disabled"},
        "software": {"min_installs": 3},
    }

    def agents_view(f):
        rows = [a for a in AGENTS if a["site"] == f["site"] and a["state"] == f["state"]]
        return sorted(rows, key=lambda a: a["name"])

    def computers_view(f):
        rows = [a for a in AGENTS
                if a["platform"] in f["platform"]
                and a["hours"] <= f["max_hours"]
                and a["state"] != f["exclude_state"]]
        return sorted(rows, key=lambda a: a["name"])

    def security_view(f):
        rows = [a for a in AGENTS if a["antivirus"] == f["antivirus"]]
        return sorted(rows, key=lambda a: a["name"])

    def software_view(f):
        rows = [s for s in SOFTWARE if s["installs"] >= f["min_installs"]]
        return sorted(rows, key=lambda s: s["name"])

    views = {
        "agents": (agents_view, filters["agents"], "site:yangon,state:Enabled", len(AGENTS)),
        "computers": (computers_view, filters["computers"],
                      "platform:windows|linux,max_hours:24", len(AGENTS)),
        "security": (security_view, filters["security"], "antivirus:disabled", len(AGENTS)),
        "software": (software_view, filters["software"], "min_installs:3", len(SOFTWARE)),
    }

    results = {}
    for view, (fn, spec, label, total) in views.items():
        rows = fn(spec)
        results[view] = (rows, label, total)
        print(f"[report] {view:<9} filter={label:<30} "
              f"rows={len(rows)}/{total} -> {', '.join(r['name'] for r in rows)}")

    # The exported row set is exactly what the filter selects, in sort order.
    assert [a["name"] for a in results["agents"][0]] == ["lnx-003", "lnx-006", "ws-001"]
    assert [a["name"] for a in results["computers"][0]] == ["lnx-003", "ws-001"]
    assert [a["name"] for a in results["security"][0]] == ["ws-002"]
    assert [s["name"] for s in results["software"][0]] == ["7-Zip", "Firefox", "VLC"]
    # A waiting agent reports but is not manageable and never reaches charts.
    assert "ws-005" not in [a["name"] for a in results["computers"][0]]
    # The filter definition travels with the result.
    assert filters["agents"] == {"site": "yangon", "state": "Enabled"}

    print("[OK] exercise_1 — report rows filtered and filter state preserved")


# --------------------------------------------------------------------------
# Exercise 2 — dashboard alert prioritisation
# --------------------------------------------------------------------------

def exercise_2():
    """Rank red-section items; green and blue never enter the alert queue."""
    red = DASHBOARD["red"]
    ranked = sorted(red, key=lambda i: (SEVERITY_ORDER[i["severity"]],
                                       -i["count"], i["key"]))
    green = DASHBOARD["green"]
    blue = DASHBOARD["blue"]
    degraded = sorted(k for k, v in blue.items() if v != "ok")

    print(f"[dashboard] refresh={REFRESH_SECONDS}s max_data_age={REFRESH_SECONDS}s")
    for pos, item in enumerate(ranked, 1):
        print(f"[dashboard] red  priority {pos}: {item['key']:<22} "
              f"count={item['count']:<3} severity={item['severity']}")
    print(f"[dashboard] green users={green['users']} apps={green['apps']} tags={green['tags']}")
    print("[dashboard] blue  " + " ".join(f"{k}={blue[k]}" for k in sorted(blue)))
    print(f"[dashboard] blue_degraded={','.join(degraded) if degraded else 'none'}")

    assert [i["key"] for i in ranked] == [
        "agents_not_reporting", "antivirus_disabled",
        "pending_updates", "agent_app_updates",
    ]
    assert sum(i["count"] for i in ranked) == 45
    assert all(i["severity"] in SEVERITY_ORDER for i in ranked)
    assert not any(i["key"] in green for i in ranked)
    assert degraded == ["workers"]
    # A five-minute refresh means every number can be five minutes old.
    assert REFRESH_SECONDS == 5 * 60

    print("[OK] exercise_2 — dashboard items ranked; green and blue kept out")


# --------------------------------------------------------------------------
# Exercise 3 — layered connectivity evaluation
# --------------------------------------------------------------------------

def exercise_3():
    """Walk the layers in order and stop at the first failing layer."""

    def evaluate(failing_layer):
        states = []
        blocked = False
        for index, layer in enumerate(LAYERS, 1):
            if blocked:
                states.append((layer, "not tested"))
            elif index == failing_layer:
                states.append((layer, "fail"))
                blocked = True
            else:
                states.append((layer, "ok"))
        first = LAYERS[failing_layer - 1] if failing_layer else "none"
        verdict = f"blocked_at_layer_{failing_layer}" if failing_layer else "healthy"
        return states, first, verdict

    results = {}
    for name, failing in SCENARIOS:
        states, first, verdict = evaluate(failing)
        results[name] = (states, first, verdict)
        print(f"[diag] scenario={name:<10} first_failure={first:<26} verdict={verdict}")
        print("[diag]   " + " ".join(f"{layer}={state}" for layer, state in states))

    healthy = results["healthy"][0]
    assert [s for _, s in healthy] == ["ok"] * 5
    assert results["healthy"][1] == "none"

    for name, failing in [("nats_down", 1), ("db_down", 3), ("ocsp_down", 5)]:
        states, first, verdict = results[name]
        assert first == LAYERS[failing - 1]
        assert states[failing - 1][1] == "fail"
        assert all(s == "ok" for _, s in states[:failing - 1])
        assert all(s == "not tested" for _, s in states[failing:])
        assert sum(1 for _, s in states if s == "not tested") == 5 - failing
        assert verdict == f"blocked_at_layer_{failing}"
    # No downstream layer may ever be reported healthy after a failure.
    assert not any(s == "ok" for _, s in results["nats_down"][0][1:])

    print("[OK] exercise_3 — layers evaluated in order with downstream skipped")


# --------------------------------------------------------------------------
# Exercise 4 — log classification
# --------------------------------------------------------------------------

def exercise_4():
    """Assign every log line to exactly one category by keyword precedence."""

    def classify(line):
        text = line.lower()
        for category in LOG_ORDER:
            for keyword in LOG_KEYWORDS.get(category, ()):
                if keyword in text:
                    return category
        return "other"

    counts = {category: 0 for category in LOG_ORDER}
    classified = []
    for source, line in LOG_LINES:
        category = classify(line)
        classified.append((source, line, category))
        counts[category] += 1

    print(f"[logs] classified={len(classified)}")
    print("[logs] " + " ".join(f"{k}={counts[k]}" for k in sorted(counts)))
    print("[logs] triage_order=" + ",".join(LOG_ORDER))

    assert counts == {"certificate": 3, "dns": 1, "auth": 2, "database": 1,
                      "nats": 1, "sftp": 1, "other": 2}
    assert sum(counts.values()) == len(LOG_LINES) == 11
    assert all(c in LOG_ORDER for _, _, c in classified)
    # A DNS failure that mentions the NATS host is still a DNS failure.
    assert classified[5][2] == "dns"
    # Clock skew surfaces through TLS, so it lands in the certificate bucket.
    assert classified[10][2] == "certificate"
    assert set(counts) == set(LOG_ORDER)

    print("[OK] exercise_4 — log lines classified by keyword precedence")


# --------------------------------------------------------------------------
# Exercise 5 — MTTR and recurrence metrics
# --------------------------------------------------------------------------

def exercise_5():
    """Compute per-cause MTTR, the longest incident and recurrence per endpoint."""

    def minutes(opened, closed):
        fmt = "%Y-%m-%dT%H:%M:%S"
        delta = datetime.strptime(closed, fmt) - datetime.strptime(opened, fmt)
        return int(delta.total_seconds() // 60)

    durations = []
    for ident, cause, endpoint, opened, closed in INCIDENTS:
        durations.append((ident, cause, endpoint, minutes(opened, closed)))

    by_cause = {}
    for _, cause, _, span in durations:
        by_cause.setdefault(cause, []).append(span)
    mttr = {cause: sum(v) / len(v) for cause, v in by_cause.items()}

    recurrence = {}
    for _, _, endpoint, _ in durations:
        recurrence[endpoint] = recurrence.get(endpoint, 0) + 1
    recurring = sorted(e for e, n in recurrence.items() if n >= 2)

    overall = sum(d[3] for d in durations) / len(durations)
    longest = max(durations, key=lambda d: (d[3], d[0]))

    print(f"[mttr] overall={overall:.1f} min over {len(durations)} incidents")
    print("[mttr] " + " ".join(f"{c}={mttr[c]:.1f}" for c in sorted(mttr)))
    print(f"[mttr] longest={longest[0]} cause={longest[1]} duration={longest[3]} min")
    print("[mttr] recurrence>=2: " + ", ".join(recurring))

    assert mttr == {"auth": 120.0, "certificate": 75.0, "database": 20.0,
                    "dns": 45.0, "nats": 240.0}
    assert round(overall, 1) == 95.8
    assert longest[0] == "inc-03" and longest[3] == 240
    assert recurrence == {"ws-001": 2, "ws-002": 1, "lnx-003": 1, "ws-005": 2}
    assert recurring == ["ws-001", "ws-005"]
    # Every incident closes after it opens.
    assert all(d[3] > 0 for d in durations)

    print("[OK] exercise_5 — MTTR, longest incident and recurrence computed")


# --------------------------------------------------------------------------
# Exercise 6 — alert rule matching
# --------------------------------------------------------------------------

def exercise_6():
    """Fire a rule only when every sample in its window satisfies it."""
    compare = {">": lambda a, b: a > b, ">=": lambda a, b: a >= b,
               "<": lambda a, b: a < b}

    fired = []
    suppressed = {"duration": 0, "threshold": 0}
    pairs = 0
    for endpoint in sorted(SAMPLES):
        for rule in RULES:
            values = SAMPLES[endpoint].get(rule["metric"])
            if values is None:
                continue
            pairs += 1
            window = values[-rule["for_samples"]:]
            test = compare[rule["op"]]
            if len(window) == rule["for_samples"] and all(
                    test(v, rule["threshold"]) for v in window):
                fired.append((rule["severity"], rule["name"], endpoint, window[-1]))
            elif not test(values[-1], rule["threshold"]):
                suppressed["threshold"] += 1
            else:
                suppressed["duration"] += 1

    fired.sort(key=lambda a: (SEVERITY_ORDER[a[0]], a[2], a[1]))
    print(f"[alert] evaluated={pairs} pairs, fired={len(fired)}")
    for severity, name, endpoint, value in fired:
        print(f"[alert] {severity:<8} {name:<21} {endpoint} value={value}")
    print(f"[alert] suppressed duration={suppressed['duration']} "
          f"threshold={suppressed['threshold']}")

    assert pairs == 6
    assert [(s, n, e) for s, n, e, _ in fired] == [
        ("critical", "agent_silent", "AP-1"),
        ("high", "pending_updates_high", "AP-3"),
        ("high", "disk_low", "AP-4"),
    ]
    assert fired[0][3] == 30
    assert suppressed == {"duration": 1, "threshold": 2}
    # One passing sample is not enough when a rule asks for two.
    assert all(e != "AP-2" for _, _, e, _ in fired)

    print("[OK] exercise_6 — alert rules matched with for_samples windows")


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
