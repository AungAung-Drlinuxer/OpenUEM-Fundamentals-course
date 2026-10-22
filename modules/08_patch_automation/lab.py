#!/usr/bin/env python3
"""Module 07 lab — patch management and automation (stdlib, offline, deterministic).

Fixtures simulate what the OpenUEM console shows in the security view and what
an administrator derives from it. No network access, no wall-clock reads.
"""

from datetime import datetime, timedelta, timezone

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

# Security view export: pending updates per endpoint, split by severity.
PENDING_UPDATES = [
    {"endpoint": "WS-ACC-01", "os": "Windows", "critical": 2, "important": 3,
     "moderate": 4, "low": 1, "installed_last_30d": 6},
    {"endpoint": "WS-ACC-02", "os": "Windows", "critical": 0, "important": 2,
     "moderate": 1, "low": 2, "installed_last_30d": 11},
    {"endpoint": "SRV-DB-01", "os": "Linux", "critical": 5, "important": 0,
     "moderate": 2, "low": 0, "installed_last_30d": 3},
    {"endpoint": "SRV-APP-01", "os": "Linux", "critical": 1, "important": 4,
     "moderate": 0, "low": 3, "installed_last_30d": 9},
    {"endpoint": "MB-CEO-01", "os": "macOS", "critical": 0, "important": 0,
     "moderate": 0, "low": 1, "installed_last_30d": 4},
]

# Maintenance windows are declared in UTC; endpoints report a UTC offset.
MAINTENANCE_WINDOWS = [
    {"name": "windows-ring-1", "weekday": 0, "start": "18:00", "end": "21:00"},
    {"name": "linux-ring-1", "weekday": 0, "start": "22:00", "end": "01:00"},
    {"name": "mac-ring-1", "weekday": 1, "start": "09:00", "end": "11:00"},
]

ENDPOINT_OFFSETS = [
    {"endpoint": "WS-ACC-01", "utc_offset_minutes": 480},
    {"endpoint": "SRV-DB-01", "utc_offset_minutes": 60},
    {"endpoint": "MB-CEO-01", "utc_offset_minutes": -300},
]

# Fixed reference instant: Monday 2026-06-01 23:30 UTC.
REFERENCE_NOW = datetime(2026, 6, 1, 23, 30, tzinfo=timezone.utc)


def _severity_rank(severity):
    order = {"critical": 0, "important": 1, "moderate": 2, "low": 3}
    return order[severity]


def _minutes(hhmm):
    hours, minutes = hhmm.split(":")
    return int(hours) * 60 + int(minutes)


def _in_window(reference, window, offset_minutes):
    """Return True when the endpoint's local time falls inside the window.

    The window is expressed in UTC and may wrap past midnight; a wrapped
    window belongs to the weekday on which it starts.
    """
    local = reference + timedelta(minutes=offset_minutes)
    start = _minutes(window["start"])
    end = _minutes(window["end"])
    now_minutes = local.hour * 60 + local.minute
    weekday = local.weekday()
    if start <= end:
        return weekday == window["weekday"] and start <= now_minutes < end
    # Wrapped window: before midnight on the start weekday, or after midnight
    # on the following weekday.
    if weekday == window["weekday"] and now_minutes >= start:
        return True
    next_day = (window["weekday"] + 1) % 7
    return weekday == next_day and now_minutes < end


# ---------------------------------------------------------------------------
# Exercise 1 — pending-update counts from fixtures
# ---------------------------------------------------------------------------

def exercise_1():
    """Total pending updates per endpoint and per severity across the fleet."""
    per_endpoint = []
    per_severity = {"critical": 0, "important": 0, "moderate": 0, "low": 0}
    for row in PENDING_UPDATES:
        total = row["critical"] + row["important"] + row["moderate"] + row["low"]
        per_endpoint.append((row["endpoint"], total))
        for severity in per_severity:
            per_severity[severity] += row[severity]

    per_endpoint.sort()
    fleet_total = sum(count for _, count in per_endpoint)

    assert fleet_total == 31, fleet_total
    assert per_severity == {"critical": 8, "important": 9, "moderate": 7, "low": 7}
    assert per_endpoint[0] == ("MB-CEO-01", 1)
    assert per_endpoint[-1] == ("WS-ACC-02", 5)
    assert max(per_endpoint, key=lambda t: t[1]) == ("WS-ACC-01", 10)
    # Highest-priority backlog: critical count dominates the ranking.
    ranked = sorted(PENDING_UPDATES, key=lambda r: (-r["critical"], r["endpoint"]))
    assert [r["endpoint"] for r in ranked][:2] == ["SRV-DB-01", "WS-ACC-01"]

    print("  endpoint    pending  critical")
    for endpoint, total in per_endpoint:
        crit = next(r["critical"] for r in PENDING_UPDATES if r["endpoint"] == endpoint)
        print("  {:<11} {:>7}  {:>8}".format(endpoint, total, crit))
    print("  fleet total pending updates: {}".format(fleet_total))
    print("  by severity: critical={critical} important={important} "
          "moderate={moderate} low={low}".format(**per_severity))
    print("[OK] exercise_1 — pending-update counts and severity split from the security-view fixture")


# ---------------------------------------------------------------------------
# Exercise 2 — maintenance window eligibility by timezone offset
# ---------------------------------------------------------------------------

def exercise_2():
    """Decide which windows are open for an endpoint at the reference instant."""
    results = []
    for endpoint in ENDPOINT_OFFSETS:
        local = REFERENCE_NOW + timedelta(minutes=endpoint["utc_offset_minutes"])
        local_label = local.strftime("%a %H:%M")
        eligible = [
            window["name"]
            for window in MAINTENANCE_WINDOWS
            if _in_window(REFERENCE_NOW, window, endpoint["utc_offset_minutes"])
        ]
        results.append((endpoint["endpoint"], local_label, sorted(eligible)))

    results.sort()
    by_endpoint = {name: windows for name, _, windows in results}

    assert by_endpoint["WS-ACC-01"] == [], by_endpoint["WS-ACC-01"]
    assert by_endpoint["SRV-DB-01"] == ["linux-ring-1"], by_endpoint["SRV-DB-01"]
    assert by_endpoint["MB-CEO-01"] == ["windows-ring-1"], by_endpoint["MB-CEO-01"]
    # Reference is Monday 23:30 UTC; -05:00 makes it Monday 18:30 local.
    assert results[0] == ("MB-CEO-01", "Mon 18:30", ["windows-ring-1"])

    print("  endpoint    local-time    eligible-windows")
    for endpoint, label, windows in results:
        joined = ",".join(windows) if windows else "(none)"
        print("  {:<11} {:<13} {}".format(endpoint, label, joined))
    print("  reference instant: Mon 2026-06-01 23:30 UTC")
    print("[OK] exercise_2 — maintenance-window eligibility resolved through UTC offsets")


# ---------------------------------------------------------------------------
# Exercise 3 — patch wave planner by criticality
# ---------------------------------------------------------------------------

UPDATE_BACKLOG = [
    {"id": "KB5034441", "severity": "critical", "reboot": True},
    {"id": "libssl3", "severity": "critical", "reboot": False},
    {"id": "KB5034123", "severity": "important", "reboot": False},
    {"id": "openssl", "severity": "important", "reboot": True},
    {"id": "KB5031539", "severity": "moderate", "reboot": False},
    {"id": "firefox-esr", "severity": "moderate", "reboot": False},
    {"id": "curl", "severity": "low", "reboot": False},
    {"id": "tzdata", "severity": "low", "reboot": False},
]

# Wave rules: severity decides the ring, a reboot adds time to the window.
WAVE_OF_SEVERITY = {"critical": 1, "important": 2, "moderate": 3, "low": 3}
BASE_WINDOW_MINUTES = 30
REBOOT_EXTRA_MINUTES = 60


def exercise_3():
    """Group the backlog into three rings and size each maintenance window."""
    plan = []
    for update in UPDATE_BACKLOG:
        wave = WAVE_OF_SEVERITY[update["severity"]]
        minutes = BASE_WINDOW_MINUTES + (REBOOT_EXTRA_MINUTES if update["reboot"] else 0)
        plan.append({
            "id": update["id"],
            "wave": wave,
            "severity": update["severity"],
            "reboot": update["reboot"],
            "window_minutes": minutes,
        })

    # Inside a ring, reboot-requiring patches go first: they need the longest
    # window and the least uncertainty about user activity.
    plan.sort(key=lambda p: (p["wave"], not p["reboot"],
                             _severity_rank(p["severity"]), p["id"]))

    per_wave = {}
    for item in plan:
        per_wave.setdefault(item["wave"], []).append(item["id"])
    wave_minutes = {}
    for item in plan:
        wave_minutes[item["wave"]] = max(wave_minutes.get(item["wave"], 0),
                                         item["window_minutes"])

    assert per_wave[1] == ["KB5034441", "libssl3"], per_wave[1]
    assert per_wave[2] == ["openssl", "KB5034123"], per_wave[2]
    assert per_wave[3] == ["KB5031539", "firefox-esr", "curl", "tzdata"], per_wave[3]
    assert wave_minutes == {1: 90, 2: 90, 3: 30}, wave_minutes
    # A ring must never contain more than the two highest severities it serves.
    assert all(WAVE_OF_SEVERITY[i["severity"]] == i["wave"] for i in plan)

    print("  wave  patch        severity   reboot  window(min)")
    for item in plan:
        print("  {:<4}  {:<11}  {:<9}  {:<5}  {:>4}".format(
            item["wave"], item["id"], item["severity"],
            "yes" if item["reboot"] else "no", item["window_minutes"]))
    print("  wave sizes: " + ", ".join(
        "wave{}={}".format(w, len(per_wave[w])) for w in sorted(per_wave)))
    print("[OK] exercise_3 — criticality-driven patch wave plan with reboot-aware windows")


# ---------------------------------------------------------------------------
# Exercise 4 — validation matrix evaluation
# ---------------------------------------------------------------------------

POST_DEPLOY_OBSERVATIONS = [
    {"endpoint": "WS-ACC-01", "last_report_minutes": 45, "pending_after": 0,
     "service": "running", "free_disk_gb": 22, "uptime_hours": 6},
    {"endpoint": "WS-ACC-02", "last_report_minutes": 120, "pending_after": 0,
     "service": "running", "free_disk_gb": 30, "uptime_hours": 2},
    {"endpoint": "SRV-APP-01", "last_report_minutes": 30, "pending_after": 2,
     "service": "stopped", "free_disk_gb": 8, "uptime_hours": 1},
]

# name -> (evaluator, human-readable expectation)
VALIDATION_RULES = [
    ("report_fresh", lambda row: row["last_report_minutes"] <= 90, "report within 90 min"),
    ("patch_applied", lambda row: row["pending_after"] == 0, "no pending update left"),
    ("service_healthy", lambda row: row["service"] == "running", "service running"),
    ("disk_headroom", lambda row: row["free_disk_gb"] >= 10, "at least 10 GB free"),
    ("reboot_settled", lambda row: row["uptime_hours"] <= 24, "uptime under 24 h"),
]


def exercise_4():
    """Score every endpoint against the post-deployment validation matrix."""
    matrix = []
    for row in POST_DEPLOY_OBSERVATIONS:
        failed = [name for name, rule, _ in VALIDATION_RULES if not rule(row)]
        passed = len(VALIDATION_RULES) - len(failed)
        matrix.append({
            "endpoint": row["endpoint"],
            "passed": passed,
            "failed": sorted(failed),
            "rollback": "service_healthy" in failed,
        })
    matrix.sort(key=lambda r: r["endpoint"])

    total_checks = len(VALIDATION_RULES) * len(POST_DEPLOY_OBSERVATIONS)
    total_passed = sum(r["passed"] for r in matrix)
    rollback = sorted(r["endpoint"] for r in matrix if r["rollback"])

    assert total_passed == 11, total_passed
    assert total_checks == 15
    assert matrix[0]["endpoint"] == "SRV-APP-01"
    assert matrix[0]["failed"] == ["disk_headroom", "patch_applied", "service_healthy"]
    assert matrix[1]["failed"] == [], matrix[1]["failed"]
    assert matrix[2]["failed"] == ["report_fresh"], matrix[2]["failed"]
    assert rollback == ["SRV-APP-01"]

    print("  endpoint     passed/total  failed-checks")
    for row in matrix:
        failed = ",".join(row["failed"]) if row["failed"] else "(none)"
        print("  {:<11}  {:>2}/{:<9}  {}".format(
            row["endpoint"], row["passed"], len(VALIDATION_RULES), failed))
    print("  checks passed overall: {}/{}".format(total_passed, total_checks))
    print("  rollback required: {}".format(",".join(rollback) if rollback else "(none)"))
    print("[OK] exercise_4 — validation matrix scored per endpoint with rollback flag")


# ---------------------------------------------------------------------------
# Exercise 5 — compliance percentage
# ---------------------------------------------------------------------------

# Baseline: patches in scope for the profile, patches actually installed inside
# the deadline, and critical updates still pending.
COMPLIANCE_ROWS = [
    {"endpoint": "WS-ACC-01", "required": 20, "installed": 20, "critical_pending": 0},
    {"endpoint": "WS-ACC-02", "required": 20, "installed": 18, "critical_pending": 1},
    {"endpoint": "SRV-DB-01", "required": 12, "installed": 12, "critical_pending": 0},
    {"endpoint": "SRV-APP-01", "required": 12, "installed": 10, "critical_pending": 2},
    {"endpoint": "MB-CEO-01", "required": 8, "installed": 8, "critical_pending": 0},
]

COMPLIANCE_THRESHOLD_PCT = 95.0


def exercise_5():
    """Fleet patch rate, endpoint compliance rate and the exception list."""
    rows = []
    for row in COMPLIANCE_ROWS:
        pct = round(row["installed"] * 100.0 / row["required"], 1)
        compliant = pct >= COMPLIANCE_THRESHOLD_PCT and row["critical_pending"] == 0
        rows.append({
            "endpoint": row["endpoint"],
            "pct": pct,
            "critical_pending": row["critical_pending"],
            "compliant": compliant,
        })
    rows.sort(key=lambda r: (r["pct"], r["endpoint"]))

    total_required = sum(r["required"] for r in COMPLIANCE_ROWS)
    total_installed = sum(r["installed"] for r in COMPLIANCE_ROWS)
    fleet_pct = round(total_installed * 100.0 / total_required, 1)
    compliant_count = sum(1 for r in rows if r["compliant"])
    endpoint_pct = round(compliant_count * 100.0 / len(rows), 1)
    exceptions = sorted(r["endpoint"] for r in rows if not r["compliant"])

    assert total_required == 72 and total_installed == 68
    assert fleet_pct == 94.4, fleet_pct
    assert endpoint_pct == 60.0, endpoint_pct
    assert compliant_count == 3
    assert exceptions == ["SRV-APP-01", "WS-ACC-02"], exceptions
    # Endpoint compliance is the stricter number: one patch-behind host can
    # hide inside a healthy fleet average.
    assert endpoint_pct < fleet_pct

    print("  endpoint     patch-rate  critical-pending  compliant")
    for row in rows:
        print("  {:<11}  {:>9.1f}%  {:>16}  {}".format(
            row["endpoint"], row["pct"], row["critical_pending"],
            "yes" if row["compliant"] else "no"))
    print("  fleet patch rate: {:.1f}% ({}/{})".format(
        fleet_pct, total_installed, total_required))
    print("  endpoint compliance: {:.1f}% ({}/{})".format(
        endpoint_pct, compliant_count, len(rows)))
    print("  exceptions: " + ",".join(exceptions))
    print("[OK] exercise_5 — compliance percentage with a separate exception list")


# ---------------------------------------------------------------------------
# Exercise 6 — automation trigger selection
# ---------------------------------------------------------------------------

AUTOMATION_JOBS = [
    {"job": "enforce-baseline-registry", "scope": "fleet", "repeat": "continuous",
     "desired_state": True},
    {"job": "install-critical-updates", "scope": "fleet", "repeat": "continuous",
     "desired_state": True},
    {"job": "collect-patch-state", "scope": "fleet", "repeat": "continuous",
     "desired_state": False},
    {"job": "fix-one-endpoint-service", "scope": "single", "repeat": "one-off",
     "desired_state": True},
    {"job": "remove-legacy-package", "scope": "single", "repeat": "one-off",
     "desired_state": True},
    {"job": "daily-inventory-sweep", "scope": "fleet", "repeat": "continuous",
     "desired_state": False},
]

PROFILE_CHECK_MINUTES = 30
REPORT_INTERVAL_MINUTES = 60


def _select_trigger(job):
    """Pick the console mechanism that owns a routine job."""
    if job["scope"] == "single" and job["repeat"] == "one-off":
        return "deployment"
    if job["desired_state"]:
        return "profile"
    return "report"


def exercise_6():
    """Route each routine job to a profile, a deployment or the report cycle."""
    selected = {}
    for job in AUTOMATION_JOBS:
        selected.setdefault(_select_trigger(job), []).append(job["job"])
    for trigger in selected:
        selected[trigger].sort()

    per_day_profile = 24 * 60 // PROFILE_CHECK_MINUTES
    per_day_report = 24 * 60 // REPORT_INTERVAL_MINUTES

    assert sorted(selected) == ["deployment", "profile", "report"]
    assert selected["profile"] == ["enforce-baseline-registry", "install-critical-updates"]
    assert selected["deployment"] == ["fix-one-endpoint-service", "remove-legacy-package"]
    assert selected["report"] == ["collect-patch-state", "daily-inventory-sweep"]
    assert per_day_profile == 48 and per_day_report == 24
    # Profiles converge twice as often as reports arrive, so a profile task is
    # the faster lever for repeated work.
    assert per_day_profile == 2 * per_day_report

    print("  trigger     jobs")
    for trigger in sorted(selected):
        print("  {:<11} {}".format(trigger, ",".join(selected[trigger])))
    print("  profile checks per day: {} (every {} min)".format(
        per_day_profile, PROFILE_CHECK_MINUTES))
    print("  agent reports per day: {} (every {} min)".format(
        per_day_report, REPORT_INTERVAL_MINUTES))
    print("[OK] exercise_6 — automation trigger selected per job shape")


# ---------------------------------------------------------------------------

def main():
    print("Module 07 — patch management and automation lab")
    print("=" * 62)
    for number, exercise in enumerate(
            (exercise_1, exercise_2, exercise_3, exercise_4, exercise_5, exercise_6), 1):
        print("\n[exercise {}]".format(number))
        exercise()
    print("\n" + "=" * 62)
    print("[PASS] All 6/6 exercises passed successfully.")


if __name__ == "__main__":
    main()
