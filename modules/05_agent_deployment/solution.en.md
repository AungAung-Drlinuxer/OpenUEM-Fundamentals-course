# Module 05 — Answers

Every output in this file is the result of actually running `lab.py`. It is identical from run to run.

```bash
python3 modules/05_agent_deployment/lab.py
```

## Exercise 1 — Building the silent-install flag line

The key point of the answer is that the flag order is fixed. The result must be the same regardless of what the key order in the dictionary happens to be.

```python
def _build_silent_args(params):
    if not params.get("server"):
        raise ValueError("server=<domain:port> is required")
    tenant, site = params.get("tenantid"), params.get("siteid")
    if bool(tenant) != bool(site):
        raise ValueError("tenantid and siteid must be supplied together")
    tokens = ["/VERYSILENT"]
    for name in FLAG_ORDER:
        value = params.get(name)
        if value is not None:
            tokens.append("/%s=%s" % (name, value))
    return " ".join(tokens)
```

The comparison `bool(tenant) != bool(site)` catches the case where only one of the two values is present. If neither value is present there is no gap.

```text
full     : /VERYSILENT /cacert=C:\certs\ca.cer /cert=C:\certs\agent.cer /key=C:\certs\agent.key /sftpcert=C:\certs\sftp.cer /tenantid=1 /siteid=2 /server=nats.openuem.example:4433 /sftp=2022 /vnc=1443
minimal  : /VERYSILENT /server=nats.openuem.example:4433
pairing  : tenantid and siteid must be supplied together
no-server: server=<domain:port> is required
[OK] exercise_1 — silent-install builder orders flags and enforces the tenant/site pair
```

The first line contains all nine flags, and the order runs from `cacert` to `vnc`. The second line contains `server` only. The third and fourth lines are the reasons for the two rejected cases.

## Exercise 2 — Checking certificate files per platform

Building the `missing` list in the order of `CERTS` keeps the output stable. `extra` is sorted with `sorted()`.

```python
present = set(files)
return {
    "platform": platform,
    "dir": AGENT_DIRS[platform],
    "missing": [c for c in CERTS if c not in present],
    "extra": sorted(present - set(CERTS)),
}
```

```text
debian   missing=-                      extra=-            dir=/etc/openuem-agent/certificates
debian   missing=sftp.cer,agent.key     extra=-            dir=/etc/openuem-agent/certificates
rpm      missing=-                      extra=notes.txt    dir=/etc/openuem-agent
windows  missing=agent.cer,agent.key    extra=-            dir=C:\Program Files\OpenUEM Agent
[OK] exercise_2 — certificate check reports the four needed files per platform
```

The first row has all four files. In the second row `sftp.cer` and `agent.key` are missing. In the third row all four files are present and one unneeded `notes.txt` is left over. In the fourth row the Windows endpoint is missing `agent.cer` and `agent.key`. The Debian folder sits under the RPM folder.

## Exercise 3 — Checking the NATS endpoint and cluster list

The check is carried out in stages. There are seven stages: empty value, scheme, space after a comma, missing port, non-numeric, out of range, duplicate host.

```python
host, sep, port = entry.strip().partition(":")
if not sep or not host:
    return (False, "missing port in " + entry.strip())
if not port.isdigit():
    return (False, "non numeric port in " + entry.strip())
```

```text
OK    nats.openuem.example:4433                                  1 server(s)
OK    nats1.openuem.example:4433,nats2.openuem.example:4433      2 server(s)
FAIL  https://nats.openuem.example:4433                          scheme not allowed, use host:port
FAIL  nats.openuem.example                                       missing port in nats.openuem.example
FAIL  nats.openuem.example:0                                     port out of range in nats.openuem.example:0
FAIL  nats.openuem.example:99999                                 port out of range in nats.openuem.example:99999
FAIL  nats.openuem.example:abc                                   non numeric port in nats.openuem.example:abc
FAIL  nats.openuem.example:4433,                                 empty entry in cluster list
FAIL  <empty>                                                    empty value
FAIL  nats.openuem.example:4433,nats.openuem.example:4433        duplicate host in cluster list
[OK] exercise_3 — NATS endpoint and cluster list validation rejects bad ports
```

Only the first two rows are accepted. The remaining eight rows are rejected, and the reason differs from row to row. Both `:0` and `:99999` are out of range.

## Exercise 4 — Calculating the report interval

The number of reports per day is calculated with `1440 // interval`. The time is converted from minutes to `HH:MM` by a function.

```python
def _clock(total_minutes):
    remainder = total_minutes % 1440
    return "%02d:%02d" % (remainder // 60, remainder % 60)
```

```text
interval=60 min  reports/day=24  gap=60 min
interval=30 min  reports/day=48  gap=30 min
interval=15 min  reports/day=96  gap=15 min
profile checks/day=48  per report cycle=2
last=09:10  next report=10:10  next profile check=09:40
now=11:05  lateness=55 min  state=overdue
[OK] exercise_4 — report interval arithmetic derives volume, due time and lateness
```

The first three rows show the number of reports per day for each interval. In the fourth row the profile check runs 48 times a day and twice per report. In the fifth row, 60 minutes after the last report at 09:10 the next report falls at 10:10, while for the profile check interval of 30 minutes it falls at 09:40. In the sixth row, from 10:10 to 11:05 is 55 minutes late, so the state is `overdue`.

## Exercise 5 — Classifying log lines

The rule list is checked in order and the first matching group is taken. The rule order therefore matters.

```python
lowered = line.lower()
for keyword, category in LOG_RULES:
    if keyword in lowered:
        return category
return "unclassified"
```

```text
unclassified agent: connecting to nats.openuem.example:4433
certificate  agent: x509: certificate signed by unknown authority
connectivity agent: dial tcp 192.168.1.43:4433: i/o timeout
enrollment   agent: report queued, waiting for admission
sftp         agent: sftp server listening on 2022
vnc          agent: vnc proxy listening on 1443
configuration agent: openuem.ini loaded from /etc/openuem-agent
unclassified agent: rotating log file
count certificate  1
count configuration 1
count connectivity 1
count enrollment   1
count sftp         1
count unclassified 2
count vnc          1
[OK] exercise_5 — log triage maps keywords to certificate, connectivity and service classes
```

The first row contains the NATS address but matches no keyword, so it is `unclassified`. The last row, `rotating log file`, is also `unclassified`. The other six rows are classified into six kinds of group. The group list is sorted alphabetically, which keeps the output stable.

## Exercise 6 — Rating upgrade risk

The weight list is defined as a tuple, so the order does not change. The score is summed and split into three levels.

```python
score = 0
reasons = []
for name, weight in RISK_WEIGHTS:
    value = factors.get(name)
    if not value:
        continue
    score += weight
    reasons.append(...)
level = "high" if score >= 5 else "medium" if score >= 2 else "low"
```

```text
low    score=0  patch bump, clean config           no risk factor
medium score=4  minor bump with two agents offline 2 agent(s) offline; config customised
high   score=5  major bump with customised ini     config customised; major version
high   score=5  expired certificate, no rollback test cert expired; rollback untested
[OK] exercise_6 — upgrade risk classified by certificate, version and config factors
```

The first row has no reasons, so the score is zero and the level is `low`. In the second row, two offline agents (2) plus an edited ini (2) adds up to 4 and the level is `medium`. The third and fourth rows score 5 and are `high`. An expired certificate alone carries a weight of 4, so paired with an untested rollback it reaches `high`.

## Output of the whole lab

```text
[PASS] All 6/6 exercises passed successfully.
```

If all six exercises pass, this line is shown at the end. If any exercise fails, the run stops with an assertion error and this line does not appear.
