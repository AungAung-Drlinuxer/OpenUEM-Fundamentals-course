# Module 03 — Solutions

These answers match the real output of `lab.py` exactly. Each output block is copied
in the same lines that the exercise produces. If your own run differs, an unsorted
dict or set is probably still outstanding.

## Exercise 1 — Mapping packages to component roles

The core idea is that a package name directly determines that package's
responsibility and inbound port. That difference is expressed as a table.

How to answer —

1. Sort `REQUESTED_PACKAGES` with `sorted()`.
2. Look each name up in `PACKAGE_ROLES`. If found, take the responsibility and the
   port list. If not found, mark it `UNKNOWN PACKAGE`.
3. Show `-` for a component with no port.
4. Collect all inbound ports and sort them with `sorted()`.

Check — `openuem-console` owns 1323 and 1324. NATS is 4433, OCSP is 8000. The four
workers and the cert-manager CLI have no inbound port. `openuem-telemetry-sidecar` is
not an OpenUEM package, so it lands in the unmapped list.

```text
== Exercise 1 — package to role mapping ==
  openuem-agent-worker          agent-report-worker       -
  openuem-cert-manager-worker   certificate-issuer-worker -
  openuem-console               console+auth-server       1323,1324
  openuem-nats-service          nats-broker               4433
  openuem-notification-worker   notification-worker       -
  openuem-ocsp-responder        ocsp-responder            8000
  openuem-server-updater        ini-generator-service     -
  openuem-telemetry-sidecar     UNKNOWN PACKAGE           -
  mapped=7 unmapped=1
  listener ports: 1323,1324,4433,8000
[OK] exercise_1 — resolved 7 packages to roles and flagged 1 unknown package
```

## Exercise 2 — Validating the service start order

The core idea is to check an order against the pairs. Build a position map, and for
each pair a violation exists when the index of the "before" service is greater than
the index of the "after" service.

How to answer —

1. Build the position map as `{name: index}`.
2. For each `(before, after)` pair, if `position[before] > position[after]` then add
   `"<after> starts before <before>"` to the list.
3. Sort the result with `sorted()`.

This method shows that the documented order has no violations. `PROPOSED_ORDER` moves
the console to the front, so two violations appear — the console ends up before the
updater and before OCSP.

```text
== Exercise 2 — service start-order validation ==
  documented order: ocsp-responder -> nats-service -> server-updater -> agent-worker -> notification-worker -> cert-manager-worker -> console
  documented order violations: 0
  proposed order: console, nats-service, ocsp-responder, server-updater, agent-worker, notification-worker, cert-manager-worker
  proposed order violations: 2
    - openuem-console starts before openuem-ocsp-responder
    - openuem-console starts before openuem-server-updater
[OK] exercise_2 — documented order is valid and the proposed order breaks 2 dependencies
```

## Exercise 3 — Parsing `openuem.ini` by section

`configparser` does not accept keys that appear before any section, so writing a
hand-rolled parser fits the real shape of this file better.

How to answer —

1. Start `sections` as `{"(global)": {}}`.
2. Treat a line that starts with `[` and ends with `]` as a section header.
3. Skip lines starting with `#` or `;`, and skip blank lines.
4. Split a line containing `=` at the first `=` only.
5. Convert the three port keys with `int()`.
6. Walk `REQUIRED_INI` and list the entries that are missing.

The broken copy is produced by deleting the `authport` line and the `[JWT] Key` line.
That copy is then missing two requirements.

```text
== Exercise 3 — openuem.ini section parsing ==
  sections: (global), Console, JWT
  (global) keys: CACert, CAKey, NATSCert
  Console: hostname=console.openuem.example port=1323 authport=1324 domain=openuem.example
  Console reverse proxy: caddy.openuem.example:443
  JWT key length=32
  missing required entries: none
  broken fixture missing: Console.authport, JWT.Key
[OK] exercise_3 — parsed 3 ini sections and detected 2 missing entries in the broken copy
```

## Exercise 4 — Computing expiry from `--years-valid`

The core idea is that adding years must not be replaced with adding 365 days.
`date.replace(year=...)` raises `ValueError` for 29 February. That case must be
adjusted to the 28th.

How to answer —

1. In `_add_years(day, years)`, try `day.replace(year=day.year + years)`. If it
   raises `ValueError`, retry with `day=28`.
2. Reject the case when `years < 1`.
3. Find the day count with `(expiry - issued).days`.
4. If the issue date is 29 February, add `leap_day_clamped=yes`.

Two computations are checked. 2026-03-15 plus 2 years is 2028-03-15, and that window
contains 29 February 2028, so it is 731 days. 2024-02-29 plus 1 year is 2025-02-28,
which is 365 days.

```text
== Exercise 4 — certificate expiry from --years-valid ==
  issued=2026-03-15 years=2 expires=2028-03-15 term_days=731
  issued=2024-02-29 years=1 expires=2025-02-28 term_days=365 leap_day_clamped=yes
  issued=2026-03-15 years=0 rejected (window must be >= 1 year)
  accepted=2 rejected=1
[OK] exercise_4 — computed 2 expiry dates and rejected 1 invalid window
```

## Exercise 5 — Finding Console/Auth/NATS/OCSP port conflicts

The core idea is that a conflict is defined by the `(port, protocol)` pair, not by the
port number alone. TCP and UDP are separate namespaces.

How to answer —

1. Merge `PORT_PLAN` and `EXTRA_LISTENERS`.
2. Group with `{(port, proto): [owners]}`.
3. Take any group with more than one owner as a conflict.
4. Print with `sorted(conflicts)` and sort the owners with `sorted()`.
5. For a UDP group, check whether a TCP group exists on the same port.
6. Collect the ports below 1024 separately.

The result is a single conflict — 1323/tcp is used by both console and probe-agent.
4433/udp cannot conflict with TCP 4433.

```text
== Exercise 5 — port conflict detection ==
  plan entries: 5 extra listeners: 2
  conflicts (1):
    1323/tcp -> openuem-console(console), probe-agent(http)
  same number, other protocol (no conflict): 4433/udp vs 4433/tcp
  privileged ports (<1024): 443
[OK] exercise_5 — found 1 real conflict and ignored 1 same-number/different-protocol pair
```

## Exercise 6 — Generating firewall rules from the port plan

The core idea is that firewall rules are generated from the port plan rather than
written by hand. That way the plan and the firewall cannot disagree.

How to answer —

1. Build a `(port, proto, line)` tuple for each entry in `PORT_PLAN`.
2. The line format is `ufw allow <port>/<proto> comment '<component> <role>'`.
3. Sort the tuple list with `sorted()`. The port is the first element, so the sort
   follows the port.
4. Show `ufw default deny incoming` first.
5. Generate the rules a second time and check that both results are identical.

Five rules come out — 443, 1323, 1324, 4433 and 8000. Each port appears exactly once.

```text
== Exercise 6 — firewall rules from the port plan ==
  ufw default deny incoming
  ufw allow 443/tcp comment 'caddy https'
  ufw allow 1323/tcp comment 'openuem-console console'
  ufw allow 1324/tcp comment 'openuem-console auth'
  ufw allow 4433/tcp comment 'openuem-nats-service nats'
  ufw allow 8000/tcp comment 'openuem-ocsp-responder ocsp'
  rules=5 lowest_port=443 highest_port=8000
[OK] exercise_6 — generated 5 idempotent firewall rules covering every planned port
```

## Final check

Running `lab.py` should show the `[OK]` line of all six exercises together with the
following line.

```text
[PASS] All 6/6 exercises passed successfully.
```
