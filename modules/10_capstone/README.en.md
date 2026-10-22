# Module 10 — Capstone: The Whole Story

This module combines the skills learned separately in the previous eight modules
into a single deployment plan for one organization. There is no new topic. It is
only the application, in order, of parts already learned.

## Story summary

The organization `openuem.example` has two locations, a head office (Yangon) and
a branch (Mandalay). A total of 27 endpoints are managed across three platforms:
Windows, Linux and macOS. The server runs as a compose stack with PostgreSQL on
a single Linux host. The team enrolls the agents in three waves. It then
delivers the software baseline through packages and a profile. One patch wave is
executed inside the maintenance window. Finally, a certificate change causes an
incident in which the agents stop reporting, and the team diagnoses and
recovers it.

## What you will do in this module

- Set the build plan and the acceptance criteria
- Write the enrollment wave plan
- Deliver the software baseline and the patch wave
- Diagnose an incident layer by layer
- Assemble the evidence pack for the review

## Files

- `explanation.en.md` — the full story, acceptance criteria, three figures
- `exercise.en.md` — six exercises
- `solution.en.md` — the real output of `lab.py` with worked answers
- `lab.py` — deterministic lab that checks the six exercises

## Prerequisites

- Modules 01 through 08 must already be read.
- PostgreSQL, compose, certificates and agent installation must be understood
  at a basic level.
- A machine that can run Python 3 is required. The lab uses only the standard
  library and needs no network.

## Running the lab

```bash
python3 modules/10_capstone/lab.py
```

Expected result:

```text
# simulated output — illustrative
[OK] exercise_1 — 11/12 readiness checks pass and the CA validity gap blocks the build
...
[PASS] All 6/6 exercises passed successfully.
```

## Time estimate

| Part | Time |
|---|---|
| Reading the explanation | 90 minutes |
| The six exercises | 180 minutes |
| Assembling the evidence pack | 45 minutes |
| Review discussion | 45 minutes |

## Success criteria

The module is complete when the lab prints
`[PASS] All 6/6 exercises passed successfully.` and the deployment plan can be
explained against the eight acceptance criteria.
