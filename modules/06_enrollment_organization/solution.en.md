# Module 06 — Answers

The answer to each exercise is given below. The output boxes are the exact
output produced by running `lab.py`.

```bash
python3 modules/06_enrollment_organization/lab.py
```

## Exercise 1 — Allow/deny decisions

The first four requests are paths that appear in the table, so they are allowed.
agent-05 and agent-06 are refused because there is no path from a manageable
state back to the admission queue. agent-07 is refused because it is a change to
the same state, so it is a no-op request. In total 4 are allowed and 3 are
refused.

```text
exercise 1 — agent state transition validation
  agent-01  waiting_for_admission -> enabled               allow: admit from the console
  agent-02  waiting_for_admission -> disabled              allow: reject the admission request
  agent-03  enabled               -> disabled              allow: disable a manageable agent
  agent-04  disabled              -> enabled               allow: re-enable a disabled agent
  agent-05  enabled               -> waiting_for_admission deny: no rule returns to the admission queue
  agent-06  disabled              -> waiting_for_admission deny: no rule returns to the admission queue
  agent-07  enabled               -> enabled               deny: state is already the requested one
  summary: allow=4 deny=3
[OK] exercise_1 — state transitions follow the admission state machine```

The reason for the refusal is connected with the admission queue being a step
that can be crossed only once. If an endpoint is to be checked again after an
agent has been admitted, that is done by moving it to Disabled and enabling it
again.

## Exercise 2 — The list of waiting agents

The fixture contains 12 agents: 2 disabled, 5 enabled and 5
waiting_for_admission. Splitting the five waiting agents per organization gives 2
for branch-office, 2 for head-office and 1 for lab. The longest wait is PC-007
(1840 minutes), so it is recommended for admission first.

```text
exercise 2 — admission queue summary
  fixture size: 12 agents
  state                   count
  disabled                    2
  enabled                     5
  waiting_for_admission       5
  waiting per organization
  branch-office               2
  head-office                 2
  lab                         1
  oldest waiting (top 3)
  PC-007  branch-office   windows    1840 min
  PC-014  branch-office   macos      1560 min
  PC-009  head-office     linux       920 min
[OK] exercise_2 — queue census and per-organization backlog agree```

A wait of 1840 minutes is more than a day, so it signals that admitting that
endpoint has been forgotten. Reports keep arriving in the Waiting for admission
state, so it is known that the endpoint's network connection is healthy.

## Exercise 3 — Organization and site resolution

For PC-101 both columns are empty, so the default organization `head-office` is
used and the alphabetically first site of that organization, `hq-floor1`, is
chosen. For PC-102 the site is empty, so `warehouse` is obtained. For PC-103 both
columns are complete, so it is confirmed directly. The organization of PC-104 has
no site. The site of PC-105 is a site of another organization. The organization
of PC-106 does not exist. There are 3 successes and 3 refusals.

```text
exercise 3 — organization and site assignment resolution
  PC-101  head-office     hq-floor1   ok
  PC-102  branch-office   warehouse   ok
  PC-103  head-office     hq-floor2   ok
  PC-104  lab                         error: organization has no site
  PC-105  branch-office   hq-floor1   error: site does not belong to organization
  PC-106  unknown-org     warehouse   error: unknown organization
  summary: resolved=3 rejected=3
[OK] exercise_3 — default organization and site fallback resolved```

PC-105 is the most common mistake in practice. If the site name is correct but
the organization is wrong, that endpoint ends up in the reports of the wrong
department.

## Exercise 4 — CSV import validation

Of the 5 organization rows only rows 1 and 5 succeed. Row 2 has an empty site.
Row 3 is a name duplicated inside the file. The name of row 4 already exists on
the server. Of the 5 user rows only rows 1 and 5 succeed. The organization of row
2 does not exist. The site of row 3 is not a site of that organization. The email
of row 4 is duplicated inside the file.

```text
exercise 4 — CSV import validation (organizations then users)
  organization rows: 5  accepted: 2  rejected: 3
    row 2  west-branch   error: site column is empty
    row 3  east-branch   error: duplicate organization name in file
    row 4  head-office   error: organization already exists on the server
  user rows: 5  accepted: 2  rejected: 3
    row 2  b@openuem.example   error: unknown organization ghost-org
    row 3  c@openuem.example   error: site hq-floor1 does not belong to branch-office
    row 4  a@openuem.example   error: duplicate user email in file
  note: organizations are imported before users because row 5 needs east-branch
[OK] exercise_4 — CSV rows rejected for duplicates and missing site```

Row 5 references `east-branch`. That organization is created by row 1, so the
organization import has to be completed first. If the order is wrong, a valid
user row will also be rejected.

## Exercise 5 — Least privilege assessment

There are three roles that can satisfy the two required capabilities. The number
of excess capabilities is 2 for operator, 4 for administrator and 5 for owner.
The smallest, operator, is chosen. The administrator proposal for `helpdesk-01`
is rejected because it contains 4 excess capabilities.

```text
exercise 5 — administrator capability matrix and least privilege
  capability            administrator    operator         owner            read_only
  admit_agent           Y                -                Y                -
  export_reports        Y                Y                Y                Y
  force_report          Y                Y                Y                -
  manage_orgs           -                -                Y                -
  manage_users          Y                -                Y                -
  remote_assistance     Y                Y                Y                -
  view_inventory        Y                Y                Y                Y
  required capabilities: force_report, view_inventory
  candidates (excess capabilities):
    operator        excess 2
    administrator   excess 4
    owner           excess 5
  least privilege role: operator
  proposal helpdesk-01 -> administrator: rejected (operator sufficient, excess 4)
[OK] exercise_5 — smallest sufficient role selected for the duty```

The proposal is rejected because granting more authority than a duty needs
increases risk. The administrator role includes user management, so if a helpdesk
account were stolen it would be possible to create new accounts.

## Exercise 6 — Certificate state path

PC-201 ends in the active state because it sends a report again after regenerate.
PC-202 is revoked after revoke. PC-203 returns to issued through a second
admission_issue after revoke. PC-204 is refused because it sends a report while
no certificate exists yet. The total number of refusals is 1.

```text
exercise 6 — certificate lifecycle states
  PC-201  admission_issue  absent    -> issued   allow: server.cer/server.key pair created
  PC-201  first_report     issued    -> active   allow: agent reports over TLS with the pair
  PC-201  regenerate       active    -> issued   allow: old certificate revoked, new pair created
  PC-201  first_report     issued    -> active   allow: agent reports over TLS with the pair
  PC-202  admission_issue  absent    -> issued   allow: server.cer/server.key pair created
  PC-202  revoke           issued    -> revoked  allow: administrators revoke the certificate
  PC-203  admission_issue  absent    -> issued   allow: server.cer/server.key pair created
  PC-203  revoke           issued    -> revoked  allow: administrators revoke the certificate
  PC-203  admission_issue  revoked   -> issued   allow: re-admission creates a fresh pair
  PC-204  first_report     absent    -> absent   deny: event is not permitted in the current state
  final states
  PC-201  active
  PC-202  revoked
  PC-203  issued
  PC-204  absent
[OK] exercise_6 — certificate lifecycle states and revocations traced
[PASS] All 6/6 exercises passed successfully.```

The second admission_issue of PC-203 starts from the revoked state. That path is
not a reuse of the old certificate but the issuance of a fresh pair. The final
state of PC-204 is absent, which shows that admitting that endpoint has not been
carried out yet.
