# Module 11 — Solutions

Every output below is the real stdout of `python3 modules/11_upgrade/lab.py`.

## Exercise 1 — Outdated vs upgradable

The three agents that are not on `0.12.0` are upgradable. Because `0.12.0` is
also the highest version in the fleet, the same three agents are outdated.

```text
[OK] exercise_1 — latest=0.12.0; can-be-upgraded=3; fleet-outdated=3
```

## Exercise 2 — Upgrade path

A native server can use Update Servers in the console. Docker cannot use that
feature, so the two compose commands are required. Agents are updated in bulk
from the console.

```text
[OK] exercise_2 — native='console Update Servers, or apt/dnf upgrade'; docker=compose pull + force-recreate; agent=console driven
```

## Exercise 3 — Maintenance window

Pilot and wave-1 may proceed now. Wave-2's window is still closed.

```text
[OK] exercise_3 — allowed=pilot,wave-1; blocked=wave-2
```

## Exercise 4 — Task state transitions

`Success` is terminal, so it cannot go back to `Pending`. A new update needs a
new task.

```text
[OK] exercise_4 — task states: 3/4 valid; rejected=Success->Pending
```

## Exercise 5 — Rollback target

Three releases are older than `0.12.0`. Roll back to the nearest one, `0.11.2`.

```text
[OK] exercise_5 — rollback target: 0.12.0 -> 0.11.2 (candidates=3)
```

## Exercise 6 — Post-upgrade checklist

The upgrade task has not succeeded yet, so that item is the first thing to
investigate. The other four checks passed.

```text
[OK] exercise_6 — post-upgrade checks: 4/5 passed; failed=upgrade-task-success
```
