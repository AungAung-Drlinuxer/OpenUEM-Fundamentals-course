#!/usr/bin/env python3
"""Module 11 lab — server and agent upgrade decisions, offline and deterministic."""

AGENTS = [
    {"name": "ws-001", "version": "0.12.0", "channel": "stable", "group": "pilot"},
    {"name": "ws-002", "version": "0.11.2", "channel": "stable", "group": "wave-1"},
    {"name": "srv-010", "version": "0.10.0", "channel": "stable", "group": "wave-1"},
    {"name": "mac-004", "version": "0.12.0", "channel": "stable", "group": "wave-2"},
    {"name": "ws-003", "version": "0.11.2", "channel": "stable", "group": "wave-2"},
]

LATEST = {"stable": "0.12.0", "beta": "0.13.0-beta.1"}

TASK_STATES = {
    "Pending": {"In Progress", "Cancelled"},
    "In Progress": {"Success", "Error"},
    "Success": set(),
    "Error": {"Pending"},
    "Cancelled": {"Pending"},
}

RELEASE_HISTORY = ["0.9.4", "0.10.0", "0.11.2", "0.12.0"]

UPGRADE_PATHS = {
    ("server", "native"): "console Update Servers, or apt/dnf upgrade",
    ("server", "docker"): "docker compose pull && docker compose --profile openuem up --force-recreate -d --build",
    ("agent", "any"): "console Update Agents with a release and schedule",
}


def parse(version):
    """Return a comparable tuple for x.y.z versions."""
    core = version.split("-")[0]
    return tuple(int(part) for part in core.split("."))


def exercise_1():
    """Classify agents as outdated or upgradable against the latest release."""
    latest = parse(LATEST["stable"])
    upgradable = sorted(a["name"] for a in AGENTS if parse(a["version"]) < latest)
    highest_in_fleet = max(parse(a["version"]) for a in AGENTS)
    outdated = sorted(a["name"] for a in AGENTS if parse(a["version"]) < highest_in_fleet)
    assert upgradable == ["srv-010", "ws-002", "ws-003"], upgradable
    assert outdated == ["srv-010", "ws-002", "ws-003"], outdated
    print(f"[OK] exercise_1 — latest={LATEST['stable']}; "
          f"can-be-upgraded={len(upgradable)}; fleet-outdated={len(outdated)}")


def exercise_2():
    """Pick the upgrade path for a deployment type."""
    def path(kind, deployment):
        key = (kind, deployment) if (kind, deployment) in UPGRADE_PATHS else (kind, "any")
        return UPGRADE_PATHS[key]

    native = path("server", "native")
    docker = path("server", "docker")
    agent = path("agent", "windows")
    assert "console Update Servers" in native
    assert docker.startswith("docker compose pull")
    assert "force-recreate" in docker
    assert agent.startswith("console Update Agents")
    print(f"[OK] exercise_2 — native={native!r}; docker=compose pull + force-recreate; "
          f"agent=console driven")


def exercise_3():
    """Decide whether a group may upgrade now or must wait for its window."""
    policy = {"pilot": "now", "wave-1": "window", "wave-2": "window"}
    window_open = {"pilot": True, "wave-1": True, "wave-2": False}
    allowed = sorted(
        {a["group"] for a in AGENTS}
        - {g for g in policy if policy[g] == "window" and not window_open[g]}
    )
    blocked = sorted(g for g in policy if g not in allowed)
    assert allowed == ["pilot", "wave-1"], allowed
    assert blocked == ["wave-2"], blocked
    print(f"[OK] exercise_3 — allowed={','.join(allowed)}; blocked={','.join(blocked)}")


def exercise_4():
    """Validate task state transitions."""
    requested = [("Pending", "In Progress"), ("In Progress", "Success"),
                 ("Success", "Pending"), ("Error", "Pending")]
    invalid = [f"{a}->{b}" for a, b in requested if b not in TASK_STATES[a]]
    assert invalid == ["Success->Pending"], invalid
    print(f"[OK] exercise_4 — task states: {len(requested) - len(invalid)}/{len(requested)} "
          f"valid; rejected={','.join(invalid)}")


def exercise_5():
    """Choose the rollback target when the newest release fails."""
    failed = "0.12.0"
    candidates = [v for v in RELEASE_HISTORY if parse(v) < parse(failed)]
    target = candidates[-1]
    assert target == "0.11.2", target
    print(f"[OK] exercise_5 — rollback target: {failed} -> {target} "
          f"(candidates={len(candidates)})")


def exercise_6():
    """Evaluate the post-upgrade checklist and list failures."""
    checks = {
        "services-active": True,
        "console-login": True,
        "agents-reporting": True,
        "upgrade-task-success": False,
        "ocsp-healthy": True,
    }
    failed = sorted(name for name, ok in checks.items() if not ok)
    assert failed == ["upgrade-task-success"], failed
    print(f"[OK] exercise_6 — post-upgrade checks: {len(checks) - len(failed)}/{len(checks)} "
          f"passed; failed={','.join(failed)}")


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
