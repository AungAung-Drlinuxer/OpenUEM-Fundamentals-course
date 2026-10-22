# Module 09 — Solutions

Every output in this file is exactly the stdout obtained when `lab.py` is
actually run. The fixture data is illustrative and is not a number measured from
a real fleet.

```bash
python3 modules/09_reporting_troubleshooting/lab.py
```

## Exercise 1 — Filtering report rows

### Approach

Each filter is defined as a dictionary and that dictionary is passed to the view
function. This keeps the filter definition and the result rows together — it is
the basis for writing the filter into the file name.

- `agents` — matches site and state.
- `computers` — checks platform as a tuple and excludes the
  `Waiting for admission` state. Those agents send reports but have not reached
  a manageable state, so they do not appear in the charts.
- `security` — compares the antivirus value directly.
- `software` — checks the install count against a minimum value.

All rows are sorted by name before printing. The output is therefore consistent
for the same filter.

### Output

```text
[report] agents    filter=site:yangon,state:Enabled      rows=3/6 -> lnx-003, lnx-006, ws-001
[report] computers filter=platform:windows|linux,max_hours:24 rows=2/6 -> lnx-003, ws-001
[report] security  filter=antivirus:disabled             rows=1/6 -> ws-002
[report] software  filter=min_installs:3                 rows=3/4 -> 7-Zip, Firefox, VLC
```

### Reading the result

- `rows=3/6` — three of the six agents remain. `lnx-006` has not reported for 80
  hours but its state is `Enabled`, so it appears in the agents view. The agents
  view shows the current state, it does not check report freshness.
- `rows=2/6` — the absence of `ws-005` from the computers view is the result of
  excluding `Waiting for admission`.
- `rows=1/6` — there is only one machine with antivirus disabled.
- `rows=3/4` — three software items with an install count of 3 or more remain.

## Exercise 2 — Dashboard alert prioritisation

### Approach

The sort key is built from three tuples — the severity weight (the smaller
first), the negative of the count (the larger first), and the name
(alphabetical). These three define the priority order precisely. The green and
blue sections are not added to the alert list — those sections are numbers and
status, not work to be done.

### Output

```text
[dashboard] refresh=300s max_data_age=300s
[dashboard] red  priority 1: agents_not_reporting   count=4   severity=critical
[dashboard] red  priority 2: antivirus_disabled     count=7   severity=high
[dashboard] red  priority 3: pending_updates        count=23  severity=medium
[dashboard] red  priority 4: agent_app_updates      count=11  severity=low
[dashboard] green users=42 apps=96 tags=6
[dashboard] blue  console=ok nats=ok ocsp=ok postgres=ok workers=degraded
[dashboard] blue_degraded=workers
```

### Reading the result

- `agents_not_reporting` is critical, so although its count is small it reaches
  first place.
- The count of `pending_updates` (23) is the largest, but its severity is medium,
  so it reaches only third place. This shows that the idea "a larger count is
  more important" is wrong.
- `max_data_age=300s` — the whole refresh period can be the lag.
- `blue_degraded=workers` — a component health fault is shown on a separate
  line.

## Exercise 3 — Evaluating layered connectivity

### Approach

The five layers are traversed in order. A `blocked` flag is used so that every
layer after the first failing layer is marked `not tested`. Without that flag
the lower layers would be wrongly marked "ok".

### Output

```text
[diag] scenario=healthy    first_failure=none                       verdict=healthy
[diag]   endpoint->nats:4433=ok nats->agent-worker=ok agent-worker->postgres:5432=ok console:1323/1324=ok console->ocsp:8000=ok
[diag] scenario=nats_down  first_failure=endpoint->nats:4433        verdict=blocked_at_layer_1
[diag]   endpoint->nats:4433=fail nats->agent-worker=not tested agent-worker->postgres:5432=not tested console:1323/1324=not tested console->ocsp:8000=not tested
[diag] scenario=db_down    first_failure=agent-worker->postgres:5432 verdict=blocked_at_layer_3
[diag]   endpoint->nats:4433=ok nats->agent-worker=ok agent-worker->postgres:5432=fail console:1323/1324=not tested console->ocsp:8000=not tested
[diag] scenario=ocsp_down  first_failure=console->ocsp:8000         verdict=blocked_at_layer_5
[diag]   endpoint->nats:4433=ok nats->agent-worker=ok agent-worker->postgres:5432=ok console:1323/1324=ok console->ocsp:8000=fail
```

### Reading the result

- `healthy` — all five layers are `ok`, `first_failure=none`.
- `nats_down` — stops at layer 1 and the remaining four are `not tested`.
- `db_down` — layers 1 and 2 are good, layer 3 fails. Layers 4 and 5 have not
  been tested.
- `ocsp_down` — good up to layer 4 and fails at layer 5. In that state agent
  reports do not stop, only certificate checking fails.
- In any state, the assertion guarantees that not a single `ok` appears after
  the failing layer.

## Exercise 4 — Classifying logs

### Approach

A keyword list is defined per category, and the category order is defined as
`certificate, dns, auth, database, nats, sftp, other`. Each line is checked
without regard to letter case and the first matching category is taken. That
order is meaningful — a DNS line can contain the word `nats`, so dns must be
checked before nats.

### Output

```text
[logs] classified=11
[logs] auth=2 certificate=3 database=1 dns=1 nats=1 other=2 sftp=1
[logs] triage_order=certificate,dns,auth,database,nats,sftp,other
```

### Reading the result

- `classified=11` — all eleven lines receive exactly one category.
- `certificate=3` — the `ca.cer` line, the `x509` line and the
  `time skew ... TLS handshake` line. Clock skew surfaces through TLS, so it
  lands in the certificate category.
- `dns=1` — the line `lookup nats.openuem.example: no such host` contains the
  word nats but lands in the dns category.
- `auth=2` — the `jwt signature mismatch` and `token expired` lines.
- `other=2` — two healthy status lines. Those lines are not faults, so no
  immediate action is required.
- `triage_order` defines the order in which to read.

## Exercise 5 — Calculating MTTR and recurrence

### Approach

The two time values are read with `datetime.strptime` and the difference is
converted to minutes. Then the values are grouped by cause and the mean is
calculated. The current time is never used — the result is therefore the same no
matter which day it is run.

### Output

```text
[mttr] overall=95.8 min over 6 incidents
[mttr] auth=120.0 certificate=75.0 database=20.0 dns=45.0 nats=240.0
[mttr] longest=inc-03 cause=nats duration=240 min
[mttr] recurrence>=2: ws-001, ws-005
```

### Reading the result

- The MTTR of `certificate` is (90 + 60) / 2 = 75.0 minutes.
- The MTTR of `nats` is 240.0 minutes, which is the highest. Reducing that
  category through automation is therefore the priority.
- `overall=95.8` — the mean of the six incidents.
- `recurrence>=2: ws-001, ws-005` — those two endpoints each have two incidents.
  Recurrence is not a symptom but an indication that a root cause is present.

## Exercise 6 — Alert rule matching

### Approach

For each rule, the last `for_samples` entries of the sample list are taken. The
alert fires only if every value inside that window satisfies the condition. When
it does not fire, the reason is split in two — if the last value itself does not
satisfy the condition it is `threshold`, and if the last value satisfies it but
the window is not full it is `duration`.

### Output

```text
[alert] evaluated=6 pairs, fired=3
[alert] critical agent_silent          AP-1 value=30
[alert] high     pending_updates_high  AP-3 value=12
[alert] high     disk_low              AP-4 value=6
[alert] suppressed duration=1 threshold=2
```

### Reading the result

- `evaluated=6 pairs` — six endpoint and rule matches.
- `AP-1` — the last two `hours_since_report` values (26, 30) are both greater
  than 24, so a critical alert fires.
- `AP-2` — of the two samples (12, 26) only the last one matches. The window is
  not full, so it is suppressed as `duration`.
- `AP-3` and `AP-4` — both the threshold and the window match.
- `AP-5` and `AP-6` — the last value itself does not match, so they are
  suppressed as `threshold`.
- The two high severity alerts are sorted by endpoint, so `AP-3` comes before
  `AP-4`.

## Verification

The lab must be run three times and the stdout compared byte by byte. On success
the following text appears on the last line.

```text
[PASS] All 6/6 exercises passed successfully.
```
