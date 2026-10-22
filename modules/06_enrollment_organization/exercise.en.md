# Module 06 — Exercises

Each of the six exercises gives you data and rules, and you work out the result
yourself. The answers are in `solution.md`. The result of each exercise can be
confirmed with `lab.py`.

## Exercise 1 — State transition validation

The following rules are defined for the change of an agent's state.

| From | To | Action |
|---|---|---|
| waiting_for_admission | enabled | admit |
| waiting_for_admission | disabled | reject |
| enabled | disabled | disable |
| disabled | enabled | enable |

All other changes are refused. There is no path back to the admission queue. A
change to the same state (for example enabled to enabled) is treated as a no-op
request.

Check the following seven requests —

| Agent | From | To |
|---|---|---|
| agent-01 | waiting_for_admission | enabled |
| agent-02 | waiting_for_admission | disabled |
| agent-03 | enabled | disabled |
| agent-04 | disabled | enabled |
| agent-05 | enabled | waiting_for_admission |
| agent-06 | disabled | waiting_for_admission |
| agent-07 | enabled | enabled |

Tasks —

1. State the allow/deny decision and the reason for each request.
2. Count the number allowed and the number denied.
3. Explain in one sentence why the change from enabled to waiting_for_admission
   has to be refused.

## Exercise 2 — Admission queue summary

The following fixture contains 12 agents. `wait_minutes` is the time spent
waiting for admission and is zero in the other states.

| Agent | Organization | Platform | State | Wait (min) |
|---|---|---|---|---|
| PC-001 | head-office | windows | enabled | 0 |
| PC-002 | head-office | linux | enabled | 0 |
| PC-003 | branch-office | windows | disabled | 0 |
| PC-004 | head-office | macos | waiting_for_admission | 240 |
| PC-005 | lab | linux | enabled | 0 |
| PC-006 | branch-office | windows | enabled | 0 |
| PC-007 | branch-office | windows | waiting_for_admission | 1840 |
| PC-008 | lab | macos | disabled | 0 |
| PC-009 | head-office | linux | waiting_for_admission | 920 |
| PC-011 | lab | linux | waiting_for_admission | 75 |
| PC-012 | head-office | windows | enabled | 0 |
| PC-014 | branch-office | macos | waiting_for_admission | 1560 |

Tasks —

1. Show how many agents are in each state, as a table.
2. Count the waiting agents per organization.
3. List the three agents with the longest waiting time, in order.
4. On the basis of that list, recommend which agent should be admitted first.

## Exercise 3 — Organization and site resolution

The following organizations exist. `head-office` is the default organization.

| Organization | Sites |
|---|---|
| branch-office | warehouse |
| head-office | hq-floor1, hq-floor2 |
| lab | (none) |

Resolution rules —

1. If the organization column is empty, the default organization is used.
2. If the site column is empty, the sites of that organization are sorted
   alphabetically and the first site is chosen.
3. If the organization does not exist, the request is rejected.
4. If the site is not a site of that organization, the request is rejected.
5. If the organization has no site, the request is rejected.

Requests —

| Endpoint | Organization | Site |
|---|---|---|
| PC-101 | (empty) | (empty) |
| PC-102 | branch-office | (empty) |
| PC-103 | head-office | hq-floor2 |
| PC-104 | lab | (empty) |
| PC-105 | branch-office | hq-floor1 |
| PC-106 | unknown-org | warehouse |

Tasks —

1. State the result of each request (organization, site, ok/error).
2. Count the number that succeed and the number refused.
3. Explain by which rule the site of PC-101 is chosen.

## Exercise 4 — CSV import validation

The columns of the organization CSV are `name` and `site`. The server already has
`head-office` and `branch-office`. The row number is the sequence number in the
file.

| Row | name | site |
|---|---|---|
| 1 | east-branch | depot-a |
| 2 | west-branch | (empty) |
| 3 | east-branch | depot-b |
| 4 | head-office | hq-floor3 |
| 5 | central | depot-c |

The columns of the user CSV are `email`, `organization` and `site`.

| Row | email | organization | site |
|---|---|---|---|
| 1 | a@openuem.example | head-office | hq-floor1 |
| 2 | b@openuem.example | ghost-org | depot |
| 3 | c@openuem.example | branch-office | hq-floor1 |
| 4 | a@openuem.example | head-office | hq-floor2 |
| 5 | d@openuem.example | east-branch | depot-a |

Rules — the organization rows are checked first and the organizations that
succeed become available to the user rows that follow. Each user row is checked
for a duplicate email.

Tasks —

1. State the result of each organization row. Count the rows accepted and the
   rows rejected.
2. State the result of each user row. Count the rows accepted and the rows
   rejected.
3. Explain how the result of row 5 depends on the result of row 1.

## Exercise 5 — Capability matrix and least privilege

Use the following table for seven capabilities and four roles.

| Capability | administrator | operator | owner | read_only |
|---|---|---|---|---|
| admit_agent | yes | no | yes | no |
| export_reports | yes | yes | yes | yes |
| force_report | yes | yes | yes | no |
| manage_orgs | no | no | yes | no |
| manage_users | yes | no | yes | no |
| remote_assistance | yes | yes | yes | no |
| view_inventory | yes | yes | yes | yes |

The capabilities needed for a business duty are `force_report` and
`view_inventory`. An administrator proposes to assign the `helpdesk-01` account
the administrator role.

Tasks —

1. List the roles that can satisfy the requirement of that duty.
2. Calculate the number of excess capabilities in each role.
3. Choose the smallest sufficient role under least privilege.
4. Accept or reject the proposal for `helpdesk-01` and state the reason.

## Exercise 6 — Certificate lifecycle states

There are four certificate states — absent, issued, active, revoked. The
permitted events are as follows.

| From | Event | To |
|---|---|---|
| absent | admission_issue | issued |
| issued | first_report | active |
| issued | revoke | revoked |
| active | regenerate | issued |
| issued | regenerate | issued |
| active | revoke | revoked |
| revoked | admission_issue | issued |

In the `regenerate` event the old certificate is revoked and a new pair is
issued. If an event not in the table occurs it is refused and the state does not
change.

The event sequences of four agents are as follows.

| Agent | Event sequence |
|---|---|
| PC-201 | admission_issue → first_report → regenerate → first_report |
| PC-202 | admission_issue → revoke |
| PC-203 | admission_issue → revoke → admission_issue |
| PC-204 | first_report |

Tasks —

1. State the state transition for each event of each agent.
2. State the final state of each agent.
3. Count the total number of refused events.
4. State which state the second `admission_issue` of PC-203 starts from.
