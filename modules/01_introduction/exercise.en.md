# Module 01 — Exercises

Six exercises to check the concepts learned in Module 01.
The answers can be found in `solution.md`. Each exercise is
checked automatically by `lab.py`.

```bash
python3 modules/01_introduction/lab.py
```

## Exercise 1 — Lifecycle transitions

The agent lifecycle has four states — `Waiting for admission`,
`Enabled`, `Disabled`, `Removed`. Check the five transitions below.

```text
Waiting for admission -> Enabled
Waiting for admission -> Disabled
Enabled -> Disabled
Disabled -> Enabled
Removed -> Enabled
```

Which two transitions are not permitted? Also state the number of
permitted transitions.

## Exercise 2 — Component ports

Write the default ports for the seven OpenUEM components —
`console`, `console-auth`, `nats`, `ocsp-responder`, `agent-sftp`,
`agent-vnc-proxy`, `postgresql`. Order the answer by port and
express it in the form `name=port`.

## Exercise 3 — Report freshness

Using the last report time of each agent below, classify it as `fresh` (under 60 minutes),
`late` (under 240 minutes), or `stale` (over 240 minutes).

```text
ws-001   Enabled                12
ws-002   Waiting for admission  25
srv-010  Enabled                95
mac-004  Disabled               600
ws-003   Enabled                300
```

State the count for each category and the names of the agents that are `stale`.

## Exercise 4 — Capability matrix

From the capabilities below, find those available only on Windows.
Also answer whether `shell-script` is available on macOS.

```text
package-deploy, registry-key, powershell-script, shell-script,
msi-package, bitlocker-status, remote-assistance, wol
```

## Exercise 5 — Port conflict detection

The lab port plan has eight services.

```text
console 1323
console-auth 1324
nats 4433
ocsp-responder 8000
agent-sftp 2022
agent-vnc-proxy 1443
postgresql 5432
console-old 1323
```

Find the duplicated port and state which two services are using it.
Also write the number of unique ports.

## Exercise 6 — Incident triage order

Sort the four incidents below by severity, then by the oldest
(largest age).

```text
INC-104  low       400
INC-101  critical   15
INC-103  high       30
INC-102  critical    5
```
