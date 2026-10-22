#!/usr/bin/env python3
"""Module 06 — Device management basics.

Offline, deterministic lab. Python standard library only. Every fixture is
illustrative course data, not a measurement of a real fleet.
"""

INVENTORY_TABS = (
    "overview",
    "hardware",
    "operating_system",
    "monitors",
    "logical_disks",
    "network_adapters",
    "printers",
    "shares",
    "applications",
    "security",
)

PACKAGE_MANAGERS = {
    "windows": "WinGet",
    "linux": "Flatpak",
    "macos": "HomeBrew",
}

PROFILE_TASK_PLATFORMS = {
    "install_package": ("windows", "linux", "macos"),
    "uninstall_package": ("windows", "linux", "macos"),
    "registry_key": ("windows",),
    "local_user": ("windows", "linux", "macos"),
    "local_group": ("windows", "linux", "macos"),
    "powershell_script": ("windows",),
    "shell_script": ("linux", "macos"),
    "msi_package": ("windows",),
}


def exercise_1():
    """Score inventory completeness from the set of tabs an agent reported."""
    reports = {
        "mac-401": ["overview", "hardware", "operating_system", "applications",
                    "security", "shares"],
        "lnx-301": ["overview", "hardware", "operating_system", "logical_disks",
                    "network_adapters", "shares", "applications", "security"],
        "ws-001": ["overview", "hardware", "operating_system", "monitors",
                   "logical_disks", "network_adapters", "shares",
                   "applications", "security"],
        "ws-002": list(INVENTORY_TABS),
    }
    total = len(INVENTORY_TABS)
    rows = []
    for agent in sorted(reports):
        seen = [tab for tab in INVENTORY_TABS if tab in reports[agent]]
        missing = [tab for tab in INVENTORY_TABS if tab not in reports[agent]]
        score = round(len(seen) * 100 / total)
        if score >= 95:
            state = "complete"
        elif score >= 80:
            state = "partial"
        else:
            state = "incomplete"
        rows.append((agent, score, state, missing))

    print("inventory completeness — %d tabs" % total)
    for agent, score, state, missing in rows:
        absent = ", ".join(missing) if missing else "-"
        print("  %-8s %3d%%  %-10s missing: %s" % (agent, score, state, absent))
    tally = {}
    for _agent, _score, state, _missing in rows:
        tally[state] = tally.get(state, 0) + 1
    for state in sorted(tally):
        print("  %-10s %d" % (state, tally[state]))

    assert [row[0] for row in rows] == ["lnx-301", "mac-401", "ws-001", "ws-002"]
    assert rows[0][1] == 80 and rows[0][2] == "partial"
    assert rows[1][1] == 60 and rows[1][2] == "incomplete"
    assert rows[2][1] == 90 and rows[2][3] == ["printers"]
    assert rows[3][1] == 100 and rows[3][2] == "complete"
    assert tally == {"complete": 1, "incomplete": 1, "partial": 2}
    print("[OK] exercise_1 — inventory completeness scoring")


def exercise_2():
    """Pick the deployment engine from the endpoint OS family."""
    endpoints = [
        ("ws-101", "windows", "11"),
        ("srv-201", "windows", "Server 2022"),
        ("lnx-301", "linux", "Ubuntu 24.04"),
        ("lnx-302", "linux", "Fedora 40"),
        ("mac-401", "macos", "14"),
        ("bsd-501", "freebsd", "14"),
    ]
    rows = []
    for host, family, version in endpoints:
        rows.append((host, family, version, PACKAGE_MANAGERS.get(family)))

    print("package manager selection per OS family")
    for host, family, version, manager in rows:
        engine = manager if manager else "unsupported"
        print("  %-8s %-8s %-14s %s" % (host, family, version, engine))
    supported = [row for row in rows if row[3]]
    print("  supported: %d/%d" % (len(supported), len(rows)))

    assert rows[0][3] == "WinGet" and rows[1][3] == "WinGet"
    assert rows[2][3] == "Flatpak" and rows[3][3] == "Flatpak"
    assert rows[4][3] == "HomeBrew"
    assert rows[5][3] is None
    assert len(supported) == 5
    print("[OK] exercise_2 — package manager selection per OS")


def exercise_3():
    """Simulate delivery of deployment requests, including the offline queue."""
    requests = [
        ("ws-001", "7zip.7zip", True),
        ("lnx-301", "org.gimp.GIMP", False),
        ("mac-401", "wget", True),
        ("ws-002", "Microsoft.PowerToys", False),
        ("lnx-302", "org.videolan.VLC", False),
    ]
    state = {}
    print("deployment queue simulation — %d requests" % len(requests))
    print("  pass 1 — delivery attempt")
    for host, package, online in requests:
        if online:
            state[(host, package)] = "delivered"
            print("    %-8s %-22s delivered (agent online)" % (host, package))
        else:
            state[(host, package)] = "queued"
            print("    %-8s %-22s queued (agent offline)" % (host, package))

    reconnect = ["lnx-301", "lnx-302"]
    print("  pass 2 — reconnect wave: %s" % ", ".join(reconnect))
    for host, package, _online in sorted(requests):
        if state[(host, package)] == "queued" and host in reconnect:
            state[(host, package)] = "delivered"
            print("    %-8s %-22s queued request delivered" % (host, package))
    remaining = sorted(key for key, value in state.items() if value == "queued")
    for host, package in remaining:
        print("    %-8s %-22s still queued" % (host, package))

    delivered = sum(1 for value in state.values() if value == "delivered")
    queued = sum(1 for value in state.values() if value == "queued")
    print("  final: delivered=%d queued=%d" % (delivered, queued))

    assert delivered == 4 and queued == 1
    assert remaining == [("ws-002", "Microsoft.PowerToys")]
    assert state[("lnx-301", "org.gimp.GIMP")] == "delivered"
    print("[OK] exercise_3 — deployment request queue simulation")


def exercise_4():
    """Reject profile tasks whose family is unsupported on the target OS."""
    tasks = [
        {"id": "t1", "family": "install_package", "platform": "windows",
         "name": "7zip.7zip"},
        {"id": "t2", "family": "registry_key", "platform": "linux",
         "name": "DisableUSB"},
        {"id": "t3", "family": "powershell_script", "platform": "windows",
         "name": "baseline.ps1"},
        {"id": "t4", "family": "msi_package", "platform": "macos",
         "name": "agent.msi"},
        {"id": "t5", "family": "shell_script", "platform": "linux",
         "name": "harden.sh"},
        {"id": "t6", "family": "scheduled_task", "platform": "windows",
         "name": "cleanup"},
        {"id": "t7", "family": "local_user", "platform": "macos", "name": ""},
    ]
    print("profile task validation — family, platform, name")
    accepted, rejected = [], []
    for task in tasks:
        allowed = PROFILE_TASK_PLATFORMS.get(task["family"])
        if allowed is None:
            reason = "unknown task family"
        elif task["platform"] not in allowed:
            reason = "not available on %s" % task["platform"]
        elif not task["name"].strip():
            reason = "empty task name"
        else:
            reason = ""
        if reason:
            rejected.append(task["id"])
            print("    %-3s REJECT  %-18s %-8s %s"
                  % (task["id"], task["family"], task["platform"], reason))
        else:
            accepted.append(task["id"])
            print("    %-3s ACCEPT  %-18s %-8s %s"
                  % (task["id"], task["family"], task["platform"], task["name"]))
    print("  accepted=%d rejected=%d" % (len(accepted), len(rejected)))

    assert accepted == ["t1", "t3", "t5"]
    assert rejected == ["t2", "t4", "t6", "t7"]
    assert PROFILE_TASK_PLATFORMS["registry_key"] == ("windows",)
    print("[OK] exercise_4 — profile task validation")


def exercise_5():
    """Select target agents from a tag filter using all-of or any-of logic."""
    agents = {
        "mac-401": ["finance"],
        "lnx-301": ["finance", "kiosk", "lab"],
        "ws-001": ["finance", "lab"],
        "ws-002": ["lab"],
    }

    def select(required, mode):
        picked = []
        for host in sorted(agents):
            tags = set(agents[host])
            if mode == "all":
                ok = all(tag in tags for tag in required)
            else:
                ok = any(tag in tags for tag in required)
            if ok:
                picked.append(host)
        return picked

    group_all = select(["finance", "lab"], "all")
    group_any = select(["finance", "kiosk"], "any")
    print("tag filter selection over %d agents" % len(agents))
    print("  mode=all  tags=finance,lab   -> %s" % ", ".join(group_all))
    print("  mode=any  tags=finance,kiosk -> %s" % ", ".join(group_any))
    print("  excluded by mode=all: %d" % (len(agents) - len(group_all)))

    assert group_all == ["lnx-301", "ws-001"]
    assert group_any == ["lnx-301", "mac-401", "ws-001"]
    assert "ws-002" in agents and "ws-002" not in group_all
    print("[OK] exercise_5 — tag filter selection")


def exercise_6():
    """Aggregate health flags from a small reporting fixture."""
    endpoints = [
        ("ws-001", 12, True, 0, 42),
        ("ws-002", 1500, True, 3, 55),
        ("lnx-301", 45, True, 7, 8),
        ("mac-401", 90, False, 0, 60),
    ]
    per_agent, tally = [], {}
    for host, minutes, av_on, updates, free in endpoints:
        flags = []
        if minutes > 1440:
            flags.append("not_reporting")
        if not av_on:
            flags.append("antivirus_disabled")
        if updates > 0:
            flags.append("updates_pending")
        if free < 10:
            flags.append("low_disk")
        per_agent.append((host, flags))
        for flag in flags:
            tally[flag] = tally.get(flag, 0) + 1

    print("health flag aggregation — 1440 min report window, disk floor")
    for host, flags in per_agent:
        shown = ", ".join(flags) if flags else "healthy"
        print("  %-8s %s" % (host, shown))
    for flag in sorted(tally):
        print("  %-20s %d" % (flag, tally[flag]))
    healthy = sum(1 for _host, flags in per_agent if not flags)
    print("  healthy=%d of %d" % (healthy, len(per_agent)))

    assert per_agent[0][1] == []
    assert per_agent[1][1] == ["not_reporting", "updates_pending"]
    assert per_agent[2][1] == ["updates_pending", "low_disk"]
    assert per_agent[3][1] == ["antivirus_disabled"]
    assert tally == {"antivirus_disabled": 1, "low_disk": 1,
                     "not_reporting": 1, "updates_pending": 2}
    assert healthy == 1
    print("[OK] exercise_6 — health flag aggregation")


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
