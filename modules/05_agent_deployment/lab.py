#!/usr/bin/env python3
"""Module 04 — Agent deployment lab.

Standard library only, fully offline and deterministic: no random module, no
printed wall-clock time, no printed temporary paths. Fixtures mirror the agent
deployment facts taught in explanation.md.
"""

CERTS = ("ca.cer", "sftp.cer", "agent.cer", "agent.key")

# Where the agent reads its certificate material, per platform.
AGENT_DIRS = {
    "debian": "/etc/openuem-agent/certificates",
    "rpm": "/etc/openuem-agent",
    "windows": "C:\\Program Files\\OpenUEM Agent",
}

FLAG_ORDER = ("cacert", "cert", "key", "sftpcert", "tenantid", "siteid",
              "server", "sftp", "vnc")


# --------------------------------------------------------------------------
# exercise 1 — silent-install flag builder
# --------------------------------------------------------------------------

def _build_silent_args(params):
    """Return a /VERYSILENT argument line, or raise ValueError on bad input."""
    if not params.get("server"):
        raise ValueError("server=<domain:port> is required")
    tenant, site = params.get("tenantid"), params.get("siteid")
    if bool(tenant) != bool(site):
        raise ValueError("tenantid and siteid must be supplied together")
    tokens = ["/VERYSILENT"]
    for name in FLAG_ORDER:
        value = params.get(name)
        if value is not None:
            tokens.append("/%s=%s" % (name, value))
    return " ".join(tokens)


def exercise_1():
    full = {
        "cacert": "C:\\certs\\ca.cer",
        "cert": "C:\\certs\\agent.cer",
        "key": "C:\\certs\\agent.key",
        "sftpcert": "C:\\certs\\sftp.cer",
        "tenantid": "1",
        "siteid": "2",
        "server": "nats.openuem.example:4433",
        "sftp": "2022",
        "vnc": "1443",
    }
    line = _build_silent_args(full)
    assert line.startswith("/VERYSILENT ")
    assert line.count("/VERYSILENT") == 1
    assert line.index("/cacert=") < line.index("/cert=") < line.index("/key=")
    assert line.index("/key=") < line.index("/server=")
    assert "/sftp=2022" in line and "/vnc=1443" in line
    assert "/tenantid=1" in line and "/siteid=2" in line

    minimal = _build_silent_args({"server": "nats.openuem.example:4433"})
    assert minimal == "/VERYSILENT /server=nats.openuem.example:4433"
    assert "/sftp=" not in minimal

    try:
        _build_silent_args({"server": "nats.openuem.example:4433", "tenantid": "1"})
        raise AssertionError("tenant/site pairing rule was not enforced")
    except ValueError as exc:
        pairing = str(exc)
    assert "together" in pairing

    try:
        _build_silent_args({"sftp": "2022"})
        raise AssertionError("missing server was not rejected")
    except ValueError as exc:
        no_server = str(exc)
    assert "server" in no_server

    print("full     : " + line)
    print("minimal  : " + minimal)
    print("pairing  : " + pairing)
    print("no-server: " + no_server)
    print("[OK] exercise_1 — silent-install builder orders flags and enforces the tenant/site pair")


# --------------------------------------------------------------------------
# exercise 2 — certificate file check per platform
# --------------------------------------------------------------------------

def _cert_report(platform, files):
    """Compare the files on disk against the four certificates the agent needs."""
    if platform not in AGENT_DIRS:
        raise ValueError("unknown platform: " + platform)
    present = set(files)
    return {
        "platform": platform,
        "dir": AGENT_DIRS[platform],
        "missing": [c for c in CERTS if c not in present],
        "extra": sorted(present - set(CERTS)),
    }


def exercise_2():
    cases = (
        ("debian", ["agent.cer", "agent.key", "ca.cer", "sftp.cer"]),
        ("debian", ["agent.cer", "ca.cer"]),
        ("rpm", ["ca.cer", "sftp.cer", "agent.cer", "agent.key", "notes.txt"]),
        ("windows", ["ca.cer", "sftp.cer"]),
    )
    reports = [_cert_report(platform, files) for platform, files in cases]

    complete = reports[0]
    assert complete["missing"] == [] and complete["extra"] == []
    assert reports[1]["missing"] == ["sftp.cer", "agent.key"]
    assert reports[2]["extra"] == ["notes.txt"]
    assert reports[3]["missing"] == ["agent.cer", "agent.key"]
    assert AGENT_DIRS["rpm"] == "/etc/openuem-agent"
    assert AGENT_DIRS["debian"] == "/etc/openuem-agent/certificates"
    assert AGENT_DIRS["debian"].startswith(AGENT_DIRS["rpm"])
    assert [c for c in CERTS] == ["ca.cer", "sftp.cer", "agent.cer", "agent.key"]

    for report in reports:
        missing = ",".join(report["missing"]) if report["missing"] else "-"
        extra = ",".join(report["extra"]) if report["extra"] else "-"
        print("%-8s missing=%-22s extra=%-12s dir=%s"
              % (report["platform"], missing, extra, report["dir"]))
    print("[OK] exercise_2 — certificate check reports the four needed files per platform")


# --------------------------------------------------------------------------
# exercise 3 — NATS URL and cluster-list validation
# --------------------------------------------------------------------------

def _check_nats(value):
    """Validate one NATS endpoint or a comma separated cluster list."""
    if value is None or not value.strip():
        return (False, "empty value")
    if "://" in value:
        return (False, "scheme not allowed, use host:port")
    entries = value.split(",")
    if any(not entry.strip() for entry in entries):
        return (False, "empty entry in cluster list")
    hosts = []
    for entry in entries:
        host, sep, port = entry.strip().partition(":")
        if not sep or not host:
            return (False, "missing port in " + entry.strip())
        if not port.isdigit():
            return (False, "non numeric port in " + entry.strip())
        number = int(port)
        if number < 1 or number > 65535:
            return (False, "port out of range in " + entry.strip())
        hosts.append(host)
    if len(set(hosts)) != len(hosts):
        return (False, "duplicate host in cluster list")
    return (True, "%d server(s)" % len(hosts))


def exercise_3():
    cases = (
        "nats.openuem.example:4433",
        "nats1.openuem.example:4433,nats2.openuem.example:4433",
        "https://nats.openuem.example:4433",
        "nats.openuem.example",
        "nats.openuem.example:0",
        "nats.openuem.example:99999",
        "nats.openuem.example:abc",
        "nats.openuem.example:4433,",
        "",
        "nats.openuem.example:4433,nats.openuem.example:4433",
    )
    results = [(value, _check_nats(value)) for value in cases]

    ok_single = results[0][1]
    ok_cluster = results[1][1]
    assert ok_single == (True, "1 server(s)")
    assert ok_cluster == (True, "2 server(s)")
    assert [results[i][1][0] for i in (2, 3, 4, 5, 6, 7, 8, 9)] == [False] * 8
    assert "scheme" in results[2][1][1]
    assert "missing port" in results[3][1][1]
    assert "range" in results[4][1][1]
    assert "range" in results[5][1][1]
    assert "non numeric" in results[6][1][1]
    assert "empty entry" in results[7][1][1]
    assert "empty value" in results[8][1][1]
    assert "duplicate" in results[9][1][1]
    assert sum(1 for _, verdict in results if verdict[0]) == 2

    for value, (ok, reason) in results:
        shown = value if value else "<empty>"
        print("%-5s %-58s %s" % ("OK" if ok else "FAIL", shown, reason))
    print("[OK] exercise_3 — NATS endpoint and cluster list validation rejects bad ports")


# --------------------------------------------------------------------------
# exercise 4 — report interval arithmetic
# --------------------------------------------------------------------------

def _clock(total_minutes):
    """Format minutes since midnight as HH:MM (pure integer arithmetic)."""
    remainder = total_minutes % 1440
    return "%02d:%02d" % (remainder // 60, remainder % 60)


def exercise_4():
    rows = []
    for interval in (60, 30, 15):
        per_day = 24 * 60 // interval
        rows.append((interval, per_day))
    assert rows == [(60, 24), (30, 48), (15, 96)]

    profile_interval = 30
    profile_per_day = 24 * 60 // profile_interval
    assert profile_per_day == 48

    last_report = 9 * 60 + 10          # 09:10
    next_report = last_report + 60     # default 60 minute interval
    next_profile = last_report + profile_interval
    assert _clock(next_report) == "10:10"
    assert _clock(next_profile) == "09:40"

    # Profile checks per report cycle: 60 / 30 = 2
    ratio = 60 // profile_interval
    assert ratio == 2

    # Lateness: now 11:05, last report 09:10, interval 60 -> due 10:10, 55 late.
    now = 11 * 60 + 5
    lateness = now - next_report
    assert lateness == 55
    state = "overdue" if lateness > 0 else "on time"
    assert state == "overdue"

    # A fresh agent reporting every 60 minutes produces a full day of samples.
    samples = [last_report + 60 * step for step in range(3)]
    assert [_clock(s) for s in samples] == ["09:10", "10:10", "11:10"]

    for interval, per_day in rows:
        print("interval=%2d min  reports/day=%2d  gap=%d min" % (interval, per_day, interval))
    print("profile checks/day=%d  per report cycle=%d" % (profile_per_day, ratio))
    print("last=09:10  next report=%s  next profile check=%s"
          % (_clock(next_report), _clock(next_profile)))
    print("now=11:05  lateness=%d min  state=%s" % (lateness, state))
    print("[OK] exercise_4 — report interval arithmetic derives volume, due time and lateness")


# --------------------------------------------------------------------------
# exercise 5 — log triage keyword mapping
# --------------------------------------------------------------------------

LOG_RULES = (
    ("x509: certificate", "certificate"),
    ("certificate signed by unknown authority", "certificate"),
    ("certificate has expired", "certificate"),
    ("no such host", "connectivity"),
    ("connection refused", "connectivity"),
    ("i/o timeout", "connectivity"),
    ("context deadline exceeded", "connectivity"),
    ("waiting for admission", "enrollment"),
    ("not admitted", "enrollment"),
    ("sftp", "sftp"),
    ("vnc", "vnc"),
    ("openuem.ini", "configuration"),
)

LOG_FIXTURE = (
    "agent: connecting to nats.openuem.example:4433",
    "agent: x509: certificate signed by unknown authority",
    "agent: dial tcp 192.168.1.43:4433: i/o timeout",
    "agent: report queued, waiting for admission",
    "agent: sftp server listening on 2022",
    "agent: vnc proxy listening on 1443",
    "agent: openuem.ini loaded from /etc/openuem-agent",
    "agent: rotating log file",
)


def _triage(line):
    """Map one log line to a triage category, first matching rule wins."""
    lowered = line.lower()
    for keyword, category in LOG_RULES:
        if keyword in lowered:
            return category
    return "unclassified"


def exercise_5():
    tagged = [(line, _triage(line)) for line in LOG_FIXTURE]
    counts = {}
    for _, category in tagged:
        counts[category] = counts.get(category, 0) + 1

    assert len(tagged) == len(LOG_FIXTURE)
    assert sum(counts.values()) == len(LOG_FIXTURE)
    assert counts["certificate"] == 1
    assert counts["connectivity"] == 1
    assert counts["enrollment"] == 1
    assert counts["sftp"] == 1
    assert counts["vnc"] == 1
    assert counts["configuration"] == 1
    assert counts["unclassified"] == 2
    assert _triage("agent: connection refused by peer") == "connectivity"
    assert _triage("nothing familiar here") == "unclassified"
    # Rule order matters: a line matching two keywords keeps the first category.
    assert _triage("sftp: x509: certificate has expired") == "certificate"

    for line, category in tagged:
        print("%-12s %s" % (category, line))
    for category in sorted(counts):
        print("count %-12s %d" % (category, counts[category]))
    print("[OK] exercise_5 — log triage maps keywords to certificate, connectivity and service classes")


# --------------------------------------------------------------------------
# exercise 6 — upgrade risk classification
# --------------------------------------------------------------------------

RISK_WEIGHTS = (
    ("cert_expired", 4),
    ("major_version", 3),
    ("config_customised", 2),
    ("offline_agents", 2),
    ("rollback_untested", 1),
)


def _upgrade_risk(factors):
    """Score an agent upgrade scenario and classify it low / medium / high."""
    score = 0
    reasons = []
    for name, weight in RISK_WEIGHTS:
        value = factors.get(name)
        if not value:
            continue
        if name == "offline_agents":
            score += weight
            reasons.append("%d agent(s) offline" % value)
        else:
            score += weight
            reasons.append(name.replace("_", " "))
    level = "high" if score >= 5 else "medium" if score >= 2 else "low"
    return level, score, sorted(reasons)


def exercise_6():
    scenarios = (
        ("patch bump, clean config", {"patch_release": True}),
        ("minor bump with two agents offline",
         {"offline_agents": 2, "config_customised": True}),
        ("major bump with customised ini",
         {"major_version": True, "config_customised": True}),
        ("expired certificate, no rollback test",
         {"cert_expired": True, "rollback_untested": True}),
    )
    results = [(label, _upgrade_risk(factors)) for label, factors in scenarios]

    assert results[0][1][0] == "low" and results[0][1][1] == 0
    assert results[1][1][0] == "medium" and results[1][1][1] == 4
    assert results[2][1][0] == "high" and results[2][1][1] == 5
    assert results[3][1][0] == "high" and results[3][1][1] == 5
    assert _upgrade_risk({}) == ("low", 0, [])
    assert _upgrade_risk({"offline_agents": 1})[0] == "medium"
    assert [level for _, (level, _, _) in results].count("high") == 2

    for label, (level, score, reasons) in results:
        detail = "; ".join(reasons) if reasons else "no risk factor"
        print("%-6s score=%d  %-34s %s" % (level, score, label, detail))
    print("[OK] exercise_6 — upgrade risk classified by certificate, version and config factors")


def main():
    for number in range(1, 7):
        globals()["exercise_%d" % number]()
    print("[PASS] All 6/6 exercises passed successfully.")


if __name__ == "__main__":
    main()
