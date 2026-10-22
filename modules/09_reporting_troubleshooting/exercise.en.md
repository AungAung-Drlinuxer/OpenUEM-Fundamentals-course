# Module 09 — Exercises

All six exercises must be built in `lab.py`. Each function must print
`[OK] exercise_N — <description>` when its work is finished. At the end of the
file `[PASS] All 6/6 exercises passed successfully.` must be printed. No
network is required, no third-party package is required, and the run must be
deterministic.

## Exercise 1 — Filtering report rows

A fixture of six agents must be defined. The fields it must carry are name,
site, platform, state, the number of hours since the last report, antivirus
status and the pending update count.

The work to do —

1. For the agents view, filter the rows whose site is `yangon` and whose state
   is `Enabled`, and sort them by name.
2. For the computers view, filter the rows whose platform is `windows` or
   `linux` and whose last report is within 24 hours. Rows in the state
   `Waiting for admission` must not be included — those agents do not appear in
   the charts.
3. For the security view, filter the rows whose antivirus is `disabled`.
4. For the software view, filter the software rows whose install count is 3 or
   more.

For each filter, print `rows=selected/total` and the remaining names sorted by
name. Each filter definition must be stored as a dictionary and re-emitted
alongside the exported result — filter preservation is verified this way.

A sample output line —

```text
[report] agents    filter=site:yangon,state:Enabled      rows=3/6 -> lnx-003, lnx-006, ws-001
```

## Exercise 2 — Dashboard alert prioritisation

A fixture must be defined for the dashboard's three sections.

- Red — `agents_not_reporting`, `antivirus_disabled`, `pending_updates`,
  `agent_app_updates` (each carries a count and a severity)
- Green — user, app and tag counts
- Blue — console, NATS, worker, OCSP and PostgreSQL status

The work to do —

1. Define the weight by severity — `critical` first, `high` second, `medium`
   third, `low` fourth. When the weight is equal, order by the larger count.
   When both are equal, order by name.
2. Print the items inside the red section as a priority list.
3. The green section and the blue section must not appear in the alert list.
   Verify that with an assertion.
4. Calculate and print the maximum age the data can have from the refresh
   period (5 minutes = 300 seconds).

## Exercise 3 — Evaluating layered connectivity

The order of the five layers must be defined —

1. `endpoint→nats:4433`
2. `nats→agent-worker`
3. `agent-worker→postgres:5432`
4. `console:1323/1324`
5. `console→ocsp:8000`

Four states are supplied as fixtures — every layer succeeds, layer 1 fails,
layer 3 fails, layer 5 fails.

The work to do —

1. Evaluate one layer at a time in order. Stop at the first failing layer.
2. Mark the downstream layers that were not tested as `not tested`.
3. For each state print `first_failure`, `verdict` and the state of each layer.
4. Verify with an assertion that the downstream layers are not marked "good".

## Exercise 4 — Classifying logs

Eleven lines from the agent log and the component logs are supplied. The
categories to classify into are `certificate`, `dns`, `auth`, `database`,
`nats`, `sftp`, `other`.

The work to do —

1. Classify by keyword without regard to letter case.
2. Define the precedence order precisely — when a line contains two kinds of
   keyword, the group checked first wins.
3. Print the count per category sorted by name.
4. Verify with an assertion that every line receives exactly one category and
   that the total line count matches.
5. Define the reading order (triage order) as a separate list and verify that
   it contains every category that was found.

## Exercise 5 — Calculating MTTR and recurrence

A fixture of six incidents must be defined. The fields it must carry are
identifier, cause, endpoint, opened time and closed time. The time format is
`YYYY-MM-DDTHH:MM:SS`.

The work to do —

1. Calculate the duration of each incident in minutes.
2. Calculate MTTR (mean time to repair) per cause and print it sorted by cause
   name.
3. Select and print the single incident with the highest MTTR.
4. Calculate the recurrence rate per endpoint and print the endpoints that occur
   two times or more.
5. Print the overall MTTR to one decimal place.

The current time must not be used. Every calculation must come only from the
fixture times.

## Exercise 6 — Alert rule matching

Three rules and samples are supplied.

| Rule | metric | Condition | for_samples | severity |
|---|---|---|---|---|
| `agent_silent` | `hours_since_report` | `>` 24 | 2 | critical |
| `pending_updates_high` | `pending_updates` | `>=` 10 | 1 | high |
| `disk_low` | `free_disk_percent` | `<` 10 | 2 | high |

`for_samples` means that the rule fires when all of the last N samples satisfy
the condition.

The work to do —

1. Check each endpoint's samples in time order.
2. Evaluate the match of each rule and print the alerts that fire sorted by
   severity, then by endpoint.
3. Print the number of fired alerts and the total number of pairs evaluated.
4. Print the cases that did not fire, split by reason (`duration` or
   `threshold`).
5. Verify with an assertion that the fired alert list matches exactly.

## Submission

```bash
python3 modules/09_reporting_troubleshooting/lab.py
```

On success it exits with code 0 and the following line appears.

```text
[PASS] All 6/6 exercises passed successfully.
```

After that the output must be run three times and checked for byte-for-byte
equality.
