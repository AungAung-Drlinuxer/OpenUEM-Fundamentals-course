# Module 06 — Enrollment and organization

This module looks at how an agent is formally admitted into management, the
certificate issued alongside that admission, the report frequency, the
organization and site structure, tags and notes, the user account workflow, CSV
bulk import, and the separation of administrator roles.

## Objectives

After completing this module you will have the following skills —

- Explain the three states of an agent (Waiting for admission, Enabled, Disabled)
  and the actions permitted in each.
- Know the admission process and the risk of the automatic admission option.
- State the job of the `server.cer`/`server.key` pair issued at admission.
- Understand the difference between the 60-minute report frequency and a force
  report.
- Explain the organization and site structure, and why the default organization
  cannot be deleted.
- Know the four stages of a user account and the risk of CSV import.
- Evaluate the division of roles according to least privilege.

## File layout

| File | Contents |
|---|---|
| `README.md` | Module summary and objectives |
| `explanation.md` | Core lesson (including 2 figures) |
| `exercise.md` | Six exercises |
| `solution.md` | Answers and lab output |
| `lab.py` | Lab using only the Python standard library |

## About the lab

The lab needs neither a network nor an OpenUEM server. It models the console's
list management with fixture data. Each exercise checks the rule it teaches with
an assertion before it prints an `[OK]` line.

```bash
python3 modules/06_enrollment_organization/lab.py
```

Expected final line —

```text
[PASS] All 6/6 exercises passed successfully.
```

The lab prints no time, path or random value, so the output of one run is
identical to the next.

## Exercise overview

| # | Title | Main skill |
|---|---|---|
| 1 | State transition validation | Checking the state transition rules |
| 2 | Admission queue summary | Summarizing the list of waiting agents |
| 3 | Organization and site resolution | Resolving the default organization and the site assignment |
| 4 | CSV import validation | Checking duplicates and missing sites |
| 5 | Capability matrix | Choosing a role under least privilege |
| 6 | Certificate lifecycle | Checking the certificate state path |

## Prerequisites

- Module 05 completed (agent installation and certificate placement)
- Python 3.10 or later
- A lab environment with access to the console (for study only; not needed for the lab)

## Note

- Console menu names, role names and the identity provider list may change
  between versions. They are recorded in the Technical review notes of
  `explanation.md`.
- Command output in the documents is fixture data marked
  `# simulated output — illustrative`.
