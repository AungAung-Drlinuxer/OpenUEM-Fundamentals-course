# Module 09 — Reporting and Troubleshooting

This module teaches evidence extraction (reporting) and fault resolution
(troubleshooting) from the OpenUEM console as a pair. The objective is a single
one — to be able to obtain evidence before making a change, and to break that
evidence down layer by layer.

## Learning objectives

- Producing PDF/CSV reports from the four views agents, computers, security and
  software, and preserving the filter and sort in the report
- The dashboard's three sections (red, green, blue) and the five-minute refresh
  cadence
- Component health checks — console, NATS, workers, PostgreSQL, OCSP
- Layered connectivity checks — endpoint → NATS (4433) → worker → PostgreSQL →
  console (1323/1324) → OCSP (8000)
- The symptoms of the eight common faults and the first thing to check
- Log sources — the agent's `openuem-log.txt` (through SFTP) and the component
  logs on the server
- The SMTP requirement for user invitation and registration mail
- Building integration with external monitoring as an operational pattern

## Prerequisite

Modules 01 through 07 completed. In particular, the ports (4433, 1323, 1324,
8000, 2022, 1443) and the certificate locations must be familiar.

## Files

| File | Content |
|---|---|
| `README.md` | This introduction and guide |
| `explanation.md` | Concept explanation, four figures, code samples |
| `exercise.md` | The tasks of six exercises |
| `solution.md` | The solutions and the real output of `lab.py` |
| `lab.py` | Python standard library only, offline lab |

## Running the lab

```bash
cd /path/to/OpenUEM-Fundamentals-course
python3 modules/09_reporting_troubleshooting/lab.py
```

The lab requires no network. It practises report filtering, dashboard
prioritisation, layered checking, log classification, MTTR calculation and
alert rule matching on fixture data. On success the last line is

```text
[PASS] All 6/6 exercises passed successfully.
```

Estimated time — 45 minutes reading, 90 minutes for the exercises.

## Note

The commands in this module are real OpenUEM commands. All output, however, is
an illustrative fixture and is marked `# simulated output — illustrative`.
The course machines do not have OpenUEM installed.
