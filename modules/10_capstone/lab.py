#!/usr/bin/env python3
"""Module 09 capstone lab — deterministic, standard library only.

The fixtures below restate the numbers used throughout the module for the
`openuem.example` deployment: 27 endpoints across two sites and three
platforms, three enrollment waves, one patch wave, and one certificate
incident. A change to the scenario breaks the lab instead of drifting.

Run: python3 modules/09_capstone/lab.py
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

# The whole scenario lives in one country, so one fixed offset is enough and
# no wall clock is ever read.
LAB_TZ = timezone(timedelta(hours=6, minutes=30))

PLATFORMS = ("linux", "macos", "windows")
TAG = {"linux": "LNX", "macos": "MAC", "windows": "WIN"}

WINDOW_START = datetime(2026, 3, 14, 1, 0, tzinfo=LAB_TZ)
WINDOW_END = datetime(2026, 3, 14, 5, 0, tzinfo=LAB_TZ)


def _endpoints() -> list[dict]:
    """Head office: 10 Windows + 5 Linux + 3 macOS. Branch: 5 + 3 + 1."""
    rows: list[dict] = []
    for site, prefix, counts in (
        ("head-office", "HO", {"windows": 10, "linux": 5, "macos": 3}),
        ("branch", "BR", {"windows": 5, "linux": 3, "macos": 1}),
    ):
        for platform in PLATFORMS:
            for index in range(1, counts[platform] + 1):
                rows.append({
                    "name": "%s-%s-%02d" % (TAG[platform], prefix, index),
                    "site": site,
                    "platform": platform,
                })
    return rows


def exercise_1() -> None:
    """Readiness checklist validation before the build window."""
    checks = (
        ("db-service", "eq", "active", "active"),
        ("db-name", "eq", "openuem", "openuem"),
        ("db-owner", "eq", "openuem_app", "openuem_app"),
        ("ca-cert-days-left", "ge", 365, 120),
        ("console-port-1323", "eq", "free", "free"),
        ("auth-port-1324", "eq", "free", "free"),
        ("nats-port-4433", "eq", "free", "free"),
        ("ocsp-port-8000", "eq", "free", "free"),
        ("hosts-override", "eq", "present", "present"),
        ("console-health", "eq", 200, 200),
        ("nats-handshake", "eq", "ok", "ok"),
        ("clock-skew-seconds", "le", 300, 42),
    )

    print("[exercise_1] Build readiness for the openuem.example deployment")
    print("  %-20s%-6s%-14s%-14s%s" % ("check", "rule", "expected", "actual", "verdict"))

    blocked = []
    for name, rule, expected, actual in checks:
        if rule == "eq":
            passed = actual == expected
        elif rule == "ge":
            passed = actual >= expected
        else:
            passed = actual <= expected
        if not passed:
            blocked.append(name)
        print("  %-20s%-6s%-14s%-14s%s" % (
            name, rule, expected, actual, "PASS" if passed else "FAIL"))

    gate = "NOT-READY" if blocked else "READY"
    print("[RESULT] %d/%d checks passed" % (len(checks) - len(blocked), len(checks)))
    print("[RESULT] blocking item(s): %s" % (", ".join(blocked) if blocked else "none"))
    print("[RESULT] build gate: %s" % gate)
    if blocked:
        print("[RESULT] action: renew the CA certificate and re-run the checklist")

    assert len(blocked) == 1, blocked
    assert blocked[0] == "ca-cert-days-left"
    print("[OK] exercise_1 — 11/12 readiness checks pass and the CA validity gap blocks the build")


def exercise_2() -> None:
    """Enrollment wave planning: pilot, head office, branch."""
    endpoints = _endpoints()
    pilot = [e for e in endpoints
             if e["site"] == "head-office" and e["name"].endswith("-01")]
    wave_1 = sorted(pilot, key=lambda e: e["platform"])

    taken = {e["name"] for e in wave_1}
    wave_2 = sorted(
        (e for e in endpoints if e["site"] == "head-office" and e["name"] not in taken),
        key=lambda e: e["name"],
    )
    taken |= {e["name"] for e in wave_2}
    wave_3 = sorted(
        (e for e in endpoints if e["site"] == "branch"),
        key=lambda e: e["name"],
    )

    plan = (
        ("wave 1", "pilot", wave_1),
        ("wave 2", "head-office", wave_2),
        ("wave 3", "branch", wave_3),
    )

    print("[exercise_2] Enrollment wave plan")
    print("  %-8s%-14s%-12s%s" % ("wave", "scope", "endpoints", "platforms"))
    for label, scope, members in plan:
        platforms = ",".join(sorted({e["platform"] for e in members}))
        print("  %-8s%-14s%-12s%s" % (label, scope, len(members), platforms))

    assigned = [e["name"] for _, _, members in plan for e in members]
    duplicates = len(assigned) - len(set(assigned))
    covered = len(set(assigned)) == len(endpoints)
    biggest = max(len(members) for _, _, members in plan)

    print("[RESULT] assigned %d/%d endpoints, duplicates %d"
          % (len(set(assigned)), len(endpoints), duplicates))
    print("[RESULT] wave size cap 20 respected: %s" % ("yes" if biggest <= 20 else "no"))
    accepted = covered and duplicates == 0 and biggest <= 20
    print("[RESULT] plan accepted: %s" % ("yes" if accepted else "no"))

    assert [len(m) for _, _, m in plan] == [3, 15, 9]
    assert covered, "an endpoint is missing from the plan"
    assert duplicates == 0, "an endpoint appears in two waves"
    assert all(len({e["platform"] for e in m}) == 3 for _, _, m in plan)
    print("[OK] exercise_2 — three waves of 3/15/9 cover all 27 endpoints and every wave spans three platforms")


def _evaluate_gate(now, reporting, targets, validation_failures, open_p1):
    """Return (decision, reasons, reporting rate) for one gate evaluation."""
    reasons = []
    if not (WINDOW_START <= now < WINDOW_END):
        reasons.append("outside-maintenance-window")
    rate = reporting / targets
    if rate < 0.90:
        reasons.append("reporting-rate-below-0.90")
    if validation_failures > 0:
        reasons.append("validation-failures-present")
    if open_p1:
        reasons.append("open-p1-incident")
    return ("GO" if not reasons else "HOLD"), reasons, rate


def exercise_3() -> None:
    """Rollout gate evaluation for the Saturday patch wave."""
    attempts = (
        ("first-attempt", datetime(2026, 3, 14, 1, 5, tzinfo=LAB_TZ), 24, 1, False),
        ("after-remediation", datetime(2026, 3, 14, 2, 40, tzinfo=LAB_TZ), 27, 0, False),
        ("late-evaluation", datetime(2026, 3, 14, 6, 15, tzinfo=LAB_TZ), 27, 0, False),
    )

    print("[exercise_3] Patch wave gate for the Saturday maintenance window")
    print("  window 2026-03-14 01:00-05:00 (+06:30), 27 targets")
    print("  %-18s%-8s%-11s%-8s%-11s%s"
          % ("attempt", "at", "reporting", "rate", "validation", "decision"))

    decisions = []
    for name, moment, reporting, failures, p1 in attempts:
        decision, reasons, rate = _evaluate_gate(moment, reporting, 27, failures, p1)
        decisions.append(decision)
        print("  %-18s%-8s%-11s%-8.3f%-11s%s" % (
            name, moment.strftime("%H:%M"), "%d/27" % reporting, rate, failures, decision))
        for reason in reasons:
            print("    reason: %s" % reason)

    print("[RESULT] decision sequence: %s" % " -> ".join(decisions))
    print("[RESULT] wave executed in-window after remediation: yes")

    assert decisions == ["HOLD", "GO", "HOLD"], decisions
    assert _evaluate_gate(attempts[1][1], 27, 27, 0, False)[1] == []
    print("[OK] exercise_3 — the gate holds on two blockers, opens after remediation, and closes outside the window")


def exercise_4() -> None:
    """Compliance evidence summary: software baseline plus patch level."""
    gaps = {
        "LNX-BR-02": ("software-baseline", "Flatpak browser package missing"),
        "MAC-HO-03": ("patch-level", "one pending update above the baseline"),
        "WIN-BR-04": ("software-baseline", "WinGet package removed by the user"),
    }
    endpoints = _endpoints()
    total = len(endpoints)

    def compliant(rows):
        return sum(1 for e in rows if e["name"] not in gaps)

    print("[exercise_4] Compliance evidence summary (software baseline + patch level)")
    print("  %-10s%-8s%-11s%s" % ("platform", "total", "compliant", "rate"))
    for platform in PLATFORMS:
        rows = [e for e in endpoints if e["platform"] == platform]
        good = compliant(rows)
        print("  %-10s%-8d%-11d%.1f%%" % (platform, len(rows), good, 100.0 * good / len(rows)))

    good_total = compliant(endpoints)
    overall = round(100.0 * good_total / total, 1)
    print("[RESULT] overall compliance: %d/%d = %.1f%%" % (good_total, total, overall))
    print("[RESULT] gap(s), sorted:")
    for name in sorted(gaps):
        kind, note = gaps[name]
        print("  %-12s%-20s%s" % (name, kind, note))

    assert overall == 88.9, overall
    assert sorted(gaps) == ["LNX-BR-02", "MAC-HO-03", "WIN-BR-04"]
    assert total == 27
    print("[OK] exercise_4 — 24 of 27 endpoints are compliant (88.9 percent of the fleet)")


def _signal_matches(expected, actual) -> bool:
    if isinstance(expected, str) and expected.startswith(">"):
        return actual > int(expected[1:])
    return expected == actual


def exercise_5() -> None:
    """Incident root-cause selection after the certificate rotation."""
    signals = {
        "console_https_200": True,
        "nats_port_4433_open": True,
        "ocsp_responder_200": True,
        "postgres_accepting": True,
        "dns_resolution_ok": True,
        "clock_skew_seconds": 3,
        "agents_reporting": 4,
        "agents_total": 27,
        "certificates_rotated": 23,
        "agent_log_unknown_authority": True,
    }

    candidates = (
        ("nats-service-down", {"nats_port_4433_open": False}),
        ("postgres-unavailable", {"postgres_accepting": False}),
        ("dns-resolution-failure", {"dns_resolution_ok": False}),
        ("endpoint-clock-skew", {"clock_skew_seconds": ">300"}),
        ("trust-anchor-mismatch", {
            "agent_log_unknown_authority": True,
            "nats_port_4433_open": True,
            "dns_resolution_ok": True,
            "certificates_rotated": ">0",
        }),
    )

    print("[exercise_5] Incident root cause after the certificate rotation")
    print("  rotated certificates: %d   endpoints reporting: %d/%d"
          % (signals["certificates_rotated"], signals["agents_reporting"], signals["agents_total"]))
    print("  signal                           observed")
    for key in sorted(signals):
        print("  %-32s%s" % (key, signals[key]))

    scored = []
    for name, expected in candidates:
        matched = sum(1 for k, v in expected.items() if _signal_matches(v, signals[k]))
        scored.append((name, matched, len(expected), matched / len(expected)))
    scored.sort(key=lambda row: (-row[3], row[0]))

    print("  %-24s%-9s%-10s%s" % ("candidate", "matched", "required", "score"))
    for name, matched, required, score in scored:
        print("  %-24s%-9d%-10d%.2f" % (name, matched, required, score))

    chosen = scored[0]
    print("[RESULT] selected root cause: %s (score %.2f)" % (chosen[0], chosen[3]))
    print("[RESULT] evidence: the agent log reports an unknown certificate authority while "
          "NATS, OCSP, DNS and PostgreSQL all answer")

    recovery = (
        "freeze the certificate rotation batch",
        "restore the previous CA certificate in openuem.ini and in the certificate tree",
        "re-issue agent certificates from the trusted CA",
        "openuem-ocsp-responder",
        "openuem-nats-service",
        "openuem-server-updater",
        "openuem-agent-worker",
        "openuem-notification-worker",
        "openuem-cert-manager-worker",
        "openuem-console",
        "force report on the affected endpoints",
        "confirm reporting rate returns to 27/27",
    )
    print("[RESULT] recovery plan")
    for index, step in enumerate(recovery, 1):
        print("  %2d. %s" % (index, step))

    canonical = (
        "openuem-ocsp-responder",
        "openuem-nats-service",
        "openuem-server-updater",
        "openuem-agent-worker",
        "openuem-notification-worker",
        "openuem-cert-manager-worker",
        "openuem-console",
    )
    restarted = tuple(step for step in recovery if step in canonical)

    assert chosen[0] == "trust-anchor-mismatch", chosen
    assert scored[1][3] < chosen[3], scored
    assert restarted == canonical, restarted
    print("[OK] exercise_5 — trust-anchor mismatch is the only candidate that fits the evidence")


def exercise_6() -> None:
    """Final scorecard across the six capstone domains."""
    domains = (
        ("build-readiness", 15, 80),
        ("enrollment-waves", 15, 100),
        ("software-baseline", 20, 90),
        ("patch-wave", 20, 85),
        ("incident-response", 20, 70),
        ("evidence-pack", 10, 95),
    )

    print("[exercise_6] Capstone scorecard")
    print("  %-20s%-9s%-8s%s" % ("domain", "weight", "score", "contribution"))
    weighted = 0
    for name, weight, score in domains:
        contribution = weight * score
        weighted += contribution
        print("  %-20s%-9s%-8d%.1f" % (name, "%d%%" % weight, score, contribution / 100.0))

    total_weight = sum(w for _, w, _ in domains)
    final = weighted / 100.0
    lowest = min(domains, key=lambda d: d[2])

    if final >= 90:
        verdict = "exceeds"
    elif final >= 75:
        verdict = "meets"
    elif final >= 60:
        verdict = "partially-meets"
    else:
        verdict = "below"

    passed = final >= 75 and lowest[2] >= 60
    print("[RESULT] weight total: %d%%" % total_weight)
    print("[RESULT] weighted score: %.1f / 100" % final)
    print("[RESULT] lowest domain: %s at %d" % (lowest[0], lowest[2]))
    print("[RESULT] verdict: %s" % verdict)
    print("[RESULT] capstone gate: %s" % ("PASS" if passed else "FAIL"))

    assert total_weight == 100
    assert final == 85.5, final
    assert verdict == "meets"
    assert passed
    print("[OK] exercise_6 — weighted 85.5 with every domain at or above the 60 floor")


def main() -> None:
    exercise_1()
    exercise_2()
    exercise_3()
    exercise_4()
    exercise_5()
    exercise_6()
    print()
    print("[PASS] All 6/6 exercises passed successfully.")


if __name__ == "__main__":
    main()
