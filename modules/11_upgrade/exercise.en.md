# Module 11 — Exercises

Six exercises on server and agent upgrades.

```bash
python3 modules/11_upgrade/lab.py
```

## Exercise 1 — Outdated vs upgradable

The latest stable release is `0.12.0`. Find the agents that are not on the
latest release (upgradable) and the agents that are not on the highest version
in the fleet (outdated).

```text
ws-001   0.12.0
ws-002   0.11.2
srv-010  0.10.0
mac-004  0.12.0
ws-003   0.11.2
```

## Exercise 2 — Upgrade path

State the upgrade method for a native server, a Docker server, and an agent on
any platform. Write the two Docker commands exactly.

## Exercise 3 — Maintenance window

Policy allows the pilot group to upgrade immediately. Wave groups may upgrade
only while their window is open. Right now the window is open for pilot and
wave-1 and closed for wave-2. Which groups may proceed?

## Exercise 4 — Task state transitions

Update task states are `Pending`, `In Progress`, `Success`, `Error` and
`Cancelled`. Validate the four transitions below.

```text
Pending -> In Progress
In Progress -> Success
Success -> Pending
Error -> Pending
```

## Exercise 5 — Rollback target

The `0.12.0` upgrade failed. Release history is `0.9.4`, `0.10.0`, `0.11.2`,
`0.12.0`. Which version do you roll back to, and how many candidates are there?

## Exercise 6 — Post-upgrade checklist

Which check failed?

```text
services-active       true
console-login         true
agents-reporting      true
upgrade-task-success  false
ocsp-healthy          true
```
