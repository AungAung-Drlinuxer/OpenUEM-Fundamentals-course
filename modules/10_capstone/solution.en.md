# Module 10 — Solutions

The solutions of this module are based on the real output of `lab.py`. Each
output below can be reproduced by running that file. All numbers are teaching
fixtures and are not measured results.

```bash
python3 modules/10_capstone/lab.py
```

## Exercise 1 — Checking the readiness checklist

11 of the 12 checks pass. The failing item is `ca-cert-days-left`. The rule is
365 days or above and the current value is 120 days. The gate is therefore
`NOT-READY`.

```text
[exercise_1] Build readiness for the openuem.example deployment
  check               rule  expected      actual        verdict
  db-service          eq    active        active        PASS
  db-name             eq    openuem       openuem       PASS
  db-owner            eq    openuem_app   openuem_app   PASS
  ca-cert-days-left   ge    365           120           FAIL
  console-port-1323   eq    free          free          PASS
  auth-port-1324      eq    free          free          PASS
  nats-port-4433      eq    free          free          PASS
  ocsp-port-8000      eq    free          free          PASS
  hosts-override      eq    present       present       PASS
  console-health      eq    200           200           PASS
  nats-handshake      eq    ok            ok            PASS
  clock-skew-seconds  le    300           42            PASS
[RESULT] 11/12 checks passed
[RESULT] blocking item(s): ca-cert-days-left
[RESULT] build gate: NOT-READY
[RESULT] action: renew the CA certificate and re-run the checklist
[OK] exercise_1 — 11/12 readiness checks pass and the CA validity gap blocks the build
```

Interpretation:

- The three items `db-service`, `db-name` and `db-owner` show that the database
  is ready. Without this stage the components cannot start.
- Checking that the four ports (`1323`, `1324`, `4433`, `8000`) are free
  prevents a port collision at build time.
- `ca-cert-days-left` alone holds the gate closed. This item is the beginning of
  the later incident.
- `clock-skew-seconds` is only 42 seconds, which confirms there is no time
  difference.

The ability of the readiness checklist to identify a single blocker avoids
having to stop in the middle of the build. In this scenario the team found that
blocker correctly. However, the remediation was performed without a change
record, and the later certificate incident followed.

## Exercise 2 — Writing the enrollment wave plan

The three waves are split as 3, 15 and 9. The total is 27. Each wave contains
three platforms.

```text
[exercise_2] Enrollment wave plan
  wave    scope         endpoints   platforms
  wave 1  pilot         3           linux,macos,windows
  wave 2  head-office   15          linux,macos,windows
  wave 3  branch        9           linux,macos,windows
[RESULT] assigned 27/27 endpoints, duplicates 0
[RESULT] wave size cap 20 respected: yes
[RESULT] plan accepted: yes
[OK] exercise_2 — three waves of 3/15/9 cover all 27 endpoints and every wave spans three platforms
```

How it is computed:

- The three endpoints from the head office whose names end in `-01` are selected
  as the pilot. They are `LNX-HO-01`, `MAC-HO-01` and `WIN-HO-01`.
- The other 15 head office endpoints are assigned as the second wave.
- The 9 branch endpoints are assigned as the third wave.
- Zero duplicates is checked by comparing the list length with the set length.

The reason the pilot contains three platforms is that the install method and the
certificate placement differ by platform. Windows needs the silent flags, Debian
needs the package and the certificate folder, and macOS needs the installer and
the HomeBrew preparation. Only if all three are in the pilot can the same class
of problem be avoided in the next two waves.

## Exercise 3 — Evaluating the rollout gate

The decision sequence is `HOLD -> GO -> HOLD`.

```text
[exercise_3] Patch wave gate for the Saturday maintenance window
  window 2026-03-14 01:00-05:00 (+06:30), 27 targets
  attempt           at      reporting  rate    validation decision
  first-attempt     01:05   24/27      0.889   1          HOLD
    reason: reporting-rate-below-0.90
    reason: validation-failures-present
  after-remediation 02:40   27/27      1.000   0          GO
  late-evaluation   06:15   27/27      1.000   0          HOLD
    reason: outside-maintenance-window
[RESULT] decision sequence: HOLD -> GO -> HOLD
[RESULT] wave executed in-window after remediation: yes
[OK] exercise_3 — the gate holds on two blockers, opens after remediation, and closes outside the window
```

Cause analysis:

- First measurement (01:05): reporting 24/27 is 0.889, so it does not meet the
  90% requirement. There is also one validation failure. Two gates fail, so the
  result is `HOLD`.
- Second measurement (02:40): reporting 27/27 and zero failures. It is inside the
  window, so all four gates are met. The result is `GO`.
- Third measurement (06:15): every condition is good, but it is outside the
  window, so `outside-maintenance-window` alone causes `HOLD`.

The third measurement shows that the gate always checks time, not only
conditions. Without that check, patches would be deployed at the time of peak
use.

## Exercise 4 — Producing the compliance evidence summary

The overall compliance is 24/27 = 88.9%.

```text
[exercise_4] Compliance evidence summary (software baseline + patch level)
  platform  total   compliant  rate
  linux     8       7          87.5%
  macos     4       3          75.0%
  windows   15      14         93.3%
[RESULT] overall compliance: 24/27 = 88.9%
[RESULT] gap(s), sorted:
  LNX-BR-02   software-baseline   Flatpak browser package missing
  MAC-HO-03   patch-level         one pending update above the baseline
  WIN-BR-04   software-baseline   WinGet package removed by the user
[OK] exercise_4 — 24 of 27 endpoints are compliant (88.9 percent of the fleet)
```

Result by platform:

| Platform | Total | Compliant | Percentage |
|---|---|---|---|
| linux | 8 | 7 | 87.5% |
| macos | 4 | 3 | 75.0% |
| windows | 15 | 14 | 93.3% |

macOS is the lowest. On a platform with a small count, one failing endpoint
drops the percentage sharply. A decision must therefore not be made from the
overall figure alone. The figure of each platform must be looked at separately.

## Exercise 5 — Selecting the root cause of the incident

The selected cause is `trust-anchor-mismatch`. Only that cause matches all four
expectations.

```text
[exercise_5] Incident root cause after the certificate rotation
  rotated certificates: 23   endpoints reporting: 4/27
  signal                           observed
  agent_log_unknown_authority     True
  agents_reporting                4
  agents_total                    27
  certificates_rotated            23
  clock_skew_seconds              3
  console_https_200               True
  dns_resolution_ok               True
  nats_port_4433_open             True
  ocsp_responder_200              True
  postgres_accepting              True
  candidate               matched  required  score
  trust-anchor-mismatch   4        4         1.00
  dns-resolution-failure  0        1         0.00
  endpoint-clock-skew     0        1         0.00
  nats-service-down       0        1         0.00
  postgres-unavailable    0        1         0.00
[RESULT] selected root cause: trust-anchor-mismatch (score 1.00)
[RESULT] evidence: the agent log reports an unknown certificate authority while NATS, OCSP, DNS and PostgreSQL all answer
[RESULT] recovery plan
   1. freeze the certificate rotation batch
   2. restore the previous CA certificate in openuem.ini and in the certificate tree
   3. re-issue agent certificates from the trusted CA
   4. openuem-ocsp-responder
   5. openuem-nats-service
   6. openuem-server-updater
   7. openuem-agent-worker
   8. openuem-notification-worker
   9. openuem-cert-manager-worker
  10. openuem-console
  11. force report on the affected endpoints
  12. confirm reporting rate returns to 27/27
[OK] exercise_5 — trust-anchor mismatch is the only candidate that fits the evidence
```

The causes that were excluded:

- `nats-service-down` — the connection on port 4433 succeeds. The NATS service
  is alive.
- `postgres-unavailable` — the console returns HTTP 200. Data can be read from
  the database.
- `dns-resolution-failure` — name resolution succeeds. The branch hosts can also
  reach the same names.
- `endpoint-clock-skew` — the clock skew is only 3 seconds. It cannot affect the
  certificate validity check.

The chain of evidence:

1. The agent log says `x509: certificate signed by unknown authority`. That
   means the server does not trust the signer of the agent certificate.
2. The 4 endpoints whose certificates were not replaced continue to report. That
   shows the infrastructure is not broken.
3. All 23 replaced endpoints are silent. That connects the change directly to
   the failure.
4. The order of the services in the recovery plan matches the order of module 03
   exactly. OCSP first, then NATS, the updater, the workers and the console.

## Exercise 6 — Computing the final scorecard

The weighted total score is 85.5. The lowest domain is `incident-response` at a
score of 70.

```text
[exercise_6] Capstone scorecard
  domain              weight   score   contribution
  build-readiness     15%      80      12.0
  enrollment-waves    15%      100     15.0
  software-baseline   20%      90      18.0
  patch-wave          20%      85      17.0
  incident-response   20%      70      14.0
  evidence-pack       10%      95      9.5
[RESULT] weight total: 100%
[RESULT] weighted score: 85.5 / 100
[RESULT] lowest domain: incident-response at 70
[RESULT] verdict: meets
[RESULT] capstone gate: PASS
[OK] exercise_6 — weighted 85.5 with every domain at or above the 60 floor

[PASS] All 6/6 exercises passed successfully.
```

How it is computed:

- `build-readiness`: 15 × 80 = 1200, contribution 12.0
- `enrollment-waves`: 15 × 100 = 1500, contribution 15.0
- `software-baseline`: 20 × 90 = 1800, contribution 18.0
- `patch-wave`: 20 × 85 = 1700, contribution 17.0
- `incident-response`: 20 × 70 = 1400, contribution 14.0
- `evidence-pack`: 10 × 95 = 950, contribution 9.5

The sum is 8550, and dividing by 100 gives 85.5. Two requirements are checked.
First, the total must be 75 or above. Second, no domain may be below 60.
`incident-response` is 70, so the floor requirement is met. The gate is therefore
`PASS`.

The reason a domain below 60 is a fail even when the total score is high is that
one weak domain can put the whole operation at risk. For example, if incident
response is weak, the fact that the other five domains are good is of no use
when the endpoints go silent.
