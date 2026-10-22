# Module 01 — Solutions

The outputs below are the actual output of
`python3 modules/01_introduction/lab.py`.

## Exercise 1 — Lifecycle transitions

It is not possible to move directly from `Waiting for admission` to `Disabled`. That
agent must first be admitted and become `Enabled`, and only then can it be disabled. The
`Removed` state is a terminal state and cannot move back to any other state.

There are three permitted transitions and two rejected transitions.

```text
[OK] exercise_1 — lifecycle: 3/5 transitions valid; rejected=Waiting for admission->Disabled,Removed->Enabled
```

## Exercise 2 — Component ports

The console uses 1323 for the web UI and 1324 for authentication.
NATS, which agents connect to, is 4433. The OCSP responder is 8000.
The agent's SFTP is 2022 and the VNC proxy is 1443. PostgreSQL is 5432.

```text
[OK] exercise_2 — component ports: agent-sftp=2022, agent-vnc-proxy=1443, console=1323, console-auth=1324, nats=4433, ocsp-responder=8000, postgresql=5432
```

## Exercise 3 — Report freshness

`ws-001` (12) and `ws-002` (25) are fresh. `srv-010` (95) is late.
`ws-003` (300) and `mac-004` (600) are stale.
`mac-004` not sending a report is normal, because it is Disabled.

```text
[OK] exercise_3 — freshness: fresh=2 late=1 stale=2; stale=mac-004,ws-003
```

## Exercise 4 — Capability matrix

The capabilities available only on Windows are `bitlocker-status`,
`msi-package`, `powershell-script` and `registry-key`.
`shell-script` can be used on macOS.

```text
[OK] exercise_4 — capability matrix: windows-only=bitlocker-status,msi-package,powershell-script,registry-key; shell-script on macOS=True
```

## Exercise 5 — Port conflict detection

Both `console` and `console-old` are using 1323.
Therefore there are only seven unique ports for the eight services.
In this situation the second service cannot start.

```text
[OK] exercise_5 — port conflict: 1323 used by console and console-old; unique_ports=7
```

## Exercise 6 — Incident triage order

Prioritise by severity, and within the same severity handle the oldest
incident first. `INC-101` is 10 minutes older than
`INC-102`, so it comes first.

```text
[OK] exercise_6 — triage order: INC-101 > INC-102 > INC-103 > INC-104
```
