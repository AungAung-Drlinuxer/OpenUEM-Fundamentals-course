# Module 07 — Device management basics

## Purpose of this module

This module covers how an endpoint that has finished enrollment is managed day
to day. It explains which question each inventory tab answers, which engine
distributes a package on each platform, how a profile holds the desired state,
and which actions can be performed remotely.

## Prerequisites

- Module 06 completed (the agent has reached the Enabled state)
- Python 3.10 or later (for the lab)
- No OpenUEM server is required. The lab is entirely offline.

## Skills you will have after studying

1. State the question that each inventory tab answers.
2. Choose the correct deployment engine for Windows, Linux and macOS.
3. Explain the queueing of a request for an offline agent.
4. Check whether a profile task is valid on the target platform.
5. Select a target group with a tag filter.
6. Aggregate health flags and set priorities.

## Files

| File | Contents |
|---|---|
| `README.md` | This page |
| `explanation.md` | Core theory, comparison tables, commands and operational cautions |
| `exercise.md` | Six exercises |
| `solution.md` | Answers and lab output |
| `lab.py` | Deterministic script that checks the six exercises |

## Running the lab

```bash
python3 modules/07_device_management/lab.py
```

If the script succeeds it finishes with the following line.

```text
[PASS] All 6/6 exercises passed successfully.
```

## Suggested reading order

Read `explanation.md` sections 7.1 to 7.5, then do exercises 1 and 2 of
`exercise.md`. Then read 7.6 to 7.8 and continue with exercises 3 and 4. Finally
read sections 7.9 to 7.12 and finish exercises 5 and 6. About 90 minutes are
needed.

## Note

Every command output in this module is a teaching fixture marked
`# simulated output — illustrative`. The data in the lab is likewise example
data created for teaching, not a measurement of any real fleet. Points that may
change between versions are recorded in `Technical review notes` in
`explanation.md`.
