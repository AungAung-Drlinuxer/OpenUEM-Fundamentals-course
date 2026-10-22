# Module 08 — Answers

The output shown in these answers is the actual stdout of `lab.py`. The fixtures are demonstration data and are not measurements from the console.

## Solution 1 — Analysing the pending-update list

The total for each endpoint is obtained by adding the four severities. The fleet total is obtained by adding those numbers. The important point is to sort the list before showing it. Using `sorted()` on a tuple sorts stably by name.

```python
total = row["critical"] + row["important"] + row["moderate"] + row["low"]
per_endpoint.append((row["endpoint"], total))
per_endpoint.sort()
```

When choosing the endpoint with the largest critical count, the name has to be included as the second key. Otherwise the order of two endpoints with the same count can change.

```python
ranked = sorted(PENDING_UPDATES, key=lambda r: (-r["critical"], r["endpoint"]))
```

The result —

```text
  endpoint    pending  critical
  MB-CEO-01         1         0
  SRV-APP-01        8         1
  SRV-DB-01         7         5
  WS-ACC-01        10         2
  WS-ACC-02         5         0
  fleet total pending updates: 31
  by severity: critical=8 important=9 moderate=7 low=7
[OK] exercise_1 — pending-update counts and severity split from the security-view fixture
```

How to read it — `SRV-DB-01` has only 7 pending, but 5 of them are critical. So it is first in the priority list. `WS-ACC-01` has 10 pending, but only 2 critical. This difference shows that "largest count" and "largest risk" are not the same thing.

## Solution 2 — Calculating maintenance-window availability

Converting the window to minutes and comparing is the simplest approach. In a midnight-spanning window the start and end swap order. So the condition is split into two cases.

```python
def _in_window(reference, window, offset_minutes):
    local = reference + timedelta(minutes=offset_minutes)
    start, end = _minutes(window["start"]), _minutes(window["end"])
    now_minutes = local.hour * 60 + local.minute
    if start <= end:
        return local.weekday() == window["weekday"] and start <= now_minutes < end
    if local.weekday() == window["weekday"] and now_minutes >= start:
        return True
    next_day = (window["weekday"] + 1) % 7
    return local.weekday() == next_day and now_minutes < end
```

There are three key points. First, calculate the local time using the offset. Second, for a midnight-spanning window, check the next day as a continuation. Third, treat the start time as inside.

The result —

```text
  endpoint    local-time    eligible-windows
  MB-CEO-01   Mon 18:30     windows-ring-1
  SRV-DB-01   Tue 00:30     linux-ring-1
  WS-ACC-01   Tue 07:30     (none)
  reference instant: Mon 2026-06-01 23:30 UTC
[OK] exercise_2 — maintenance-window eligibility resolved through UTC offsets
```

How to read it — `MB-CEO-01` has a −05:00 offset. 23:30 UTC is 18:30 at that endpoint. `windows-ring-1` runs from 18:00 to 21:00, so the time falls inside. `SRV-DB-01` is +01:00, so its local time is Tuesday 00:30. `linux-ring-1` runs from Monday 22:00 to Tuesday 01:00, so the time falls inside. `WS-ACC-01` is +08:00, so its local time is 07:30. No window matches.

This result shows that a patch wave cannot be done at a single instant. Each site's local time has to be examined.

## Solution 3 — Ordering patch waves by criticality

The wave is derived directly from severity. The window duration is decided by the reboot requirement. In the sort, placing `not p["reboot"]` as the second key makes the patches that need a reboot arrive first.

```python
plan.sort(key=lambda p: (p["wave"], not p["reboot"],
                         _severity_rank(p["severity"]), p["id"]))
```

The window required for a wave is the largest duration among the patches in that wave. A window is not needed per patch. The whole wave is done in one pass.

```python
wave_minutes[item["wave"]] = max(wave_minutes.get(item["wave"], 0),
                                 item["window_minutes"])
```

The result —

```text
  wave  patch        severity   reboot  window(min)
  1     KB5034441    critical   yes      90
  1     libssl3      critical   no       30
  2     openssl      important  yes      90
  2     KB5034123    important  no       30
  3     KB5031539    moderate   no       30
  3     firefox-esr  moderate   no       30
  3     curl         low        no       30
  3     tzdata       low        no       30
  wave sizes: wave1=2, wave2=2, wave3=4
[OK] exercise_3 — criticality-driven patch wave plan with reboot-aware windows
```

How to read it — in wave 1, `KB5034441` arrives before `libssl3` because it needs a reboot. The window for wave 1 is 90 minutes. Wave 3 has four patches, and because none of them needs a reboot 30 minutes is enough. Putting wave 3 last makes the low-risk patches wait.

## Solution 4 — Evaluating the validation matrix

Storing each check as a function lets the matrix be handled as data. If the names of the failed checks are stored, writing the report is easy.

```python
VALIDATION_RULES = [
    ("report_fresh", lambda row: row["last_report_minutes"] <= 90, "report within 90 min"),
    ("patch_applied", lambda row: row["pending_after"] == 0, "no pending update left"),
    ("service_healthy", lambda row: row["service"] == "running", "service running"),
    ("disk_headroom", lambda row: row["free_disk_gb"] >= 10, "at least 10 GB free"),
    ("reboot_settled", lambda row: row["uptime_hours"] <= 24, "uptime under 24 h"),
]

failed = [name for name, rule, _ in VALIDATION_RULES if not rule(row)]
```

The rollback condition is tied to a single check. A service that will not come up is damage the user feels. Low disk space can be fixed later. So the two measures are handled differently.

The result —

```text
  endpoint     passed/total  failed-checks
  SRV-APP-01    2/5          disk_headroom,patch_applied,service_healthy
  WS-ACC-01     5/5          (none)
  WS-ACC-02     4/5          report_fresh
  checks passed overall: 11/15
  rollback required: SRV-APP-01
[OK] exercise_4 — validation matrix scored per endpoint with rollback flag
```

How to read it — `WS-ACC-01` passes all five checks. On `WS-ACC-02` the report is 120 minutes old, so `report_fresh` fails. But the patch installation succeeded. On `SRV-APP-01` three checks fail. The service not coming up raises the rollback flag.

## Solution 5 — Calculating compliance percentage

The two measures have to be calculated separately. The fleet patch rate is a ratio of patch counts. Endpoint compliance is a ratio of endpoint counts.

```python
pct = round(row["installed"] * 100.0 / row["required"], 1)
compliant = pct >= COMPLIANCE_THRESHOLD_PCT and row["critical_pending"] == 0
fleet_pct = round(total_installed * 100.0 / total_required, 1)
endpoint_pct = round(compliant_count * 100.0 / len(rows), 1)
```

Using `round()` to one decimal place keeps the numbers consistent across the report. Without `round()` the display would show numbers such as 94.44444.

The result —

```text
  endpoint     patch-rate  critical-pending  compliant
  SRV-APP-01        83.3%                 2  no
  WS-ACC-02         90.0%                 1  no
  MB-CEO-01        100.0%                 0  yes
  SRV-DB-01        100.0%                 0  yes
  WS-ACC-01        100.0%                 0  yes
  fleet patch rate: 94.4% (68/72)
  endpoint compliance: 60.0% (3/5)
  exceptions: SRV-APP-01,WS-ACC-02
[OK] exercise_5 — compliance percentage with a separate exception list
```

How to read it — the fleet patch rate is 94.4 percent, but endpoint compliance is only 60.0 percent. The reason is that two of the five endpoints do not meet the criterion. This difference shows that both reports are needed.

## Solution 6 — Choosing the automation trigger

The trigger choice is written with three rules. The order matters. The work that is once-only for a single endpoint has to be checked first. Otherwise every job that has a desired state would land in profile.

```python
def _select_trigger(job):
    if job["scope"] == "single" and job["repeat"] == "one-off":
        return "deployment"
    if job["desired_state"]:
        return "profile"
    return "report"
```

The per-day count is obtained by dividing the minutes in a day. The profile check is every 30 minutes, so 48 times; the report is every 60 minutes, so 24 times.

```python
per_day_profile = 24 * 60 // PROFILE_CHECK_MINUTES
per_day_report = 24 * 60 // REPORT_INTERVAL_MINUTES
```

The result —

```text
  trigger     jobs
  deployment  fix-one-endpoint-service,remove-legacy-package
  profile     enforce-baseline-registry,install-critical-updates
  report      collect-patch-state,daily-inventory-sweep
  profile checks per day: 48 (every 30 min)
  agent reports per day: 24 (every 60 min)
[OK] exercise_6 — automation trigger selected per job shape

==============================================================
[PASS] All 6/6 exercises passed successfully.
```

How to read it — `install-critical-updates` lands in profile because it is a desired-state job. `fix-one-endpoint-service` lands in deployment because it is once-only for a single endpoint. `collect-patch-state` relies on the report because it is only collecting state. The profile check runs 48 times a day, so it is the faster lever for repetitive work.
