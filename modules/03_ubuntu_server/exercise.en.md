# Module 03 — Exercises

These six exercises use the fixtures inside `lab.py`. Each exercise should be written
on your own first, and only then compared with `solution.md`. Output must be
deterministic — sort before printing a set or a dict.

## Exercise 1 — Mapping packages to component roles

The `PACKAGE_ROLES` fixture holds package names together with their responsibility
and inbound ports. The `REQUESTED_PACKAGES` list has one name mixed in that is not an
OpenUEM package.

To do —

1. Sort the package names alphabetically and show the responsibility and port in
   table form. For a component with no port, show `-`.
2. Mark the name that is absent from the fixture as `UNKNOWN PACKAGE` and count it
   separately.
3. Show how many packages could be mapped and how many could not.
4. Show all inbound ports, sorted.

Acceptance criteria — `openuem-console` must have two ports (1323 and 1324). The
inbound port list must contain 4433 and 8000. Confirm that the workers have no port.

## Exercise 2 — Validating the service start order

`DOCUMENTED_ORDER` is the order from the official documentation. `DEPENDENCIES` is
the set of pairs stating "which service must start before which other service".

To do —

1. Write a function that accepts an order and checks each pair for a violation.
2. Confirm the violation count for `DOCUMENTED_ORDER` is zero.
3. For `PROPOSED_ORDER` (the order that puts the console first), print the sorted
   violations. Write each violation in the form
   `<service> starts before <service>`.
4. Check that the documented order covers every service in the dependency pairs.

Acceptance criteria — exactly two violations must appear. It must show
`openuem-console` starting before `openuem-server-updater` and before
`openuem-ocsp-responder`.

## Exercise 3 — Parsing `openuem.ini` by section

`INI_FIXTURE` contains keys placed before any section, plus `[Console]` and `[JWT]`.
`REQUIRED_INI` is the set of mandatory entries.

To do —

1. Write a parser that skips `#` and `;` comments and reads `[section]` headers and
   `key = value` pairs. Put keys that appear before any section under `(global)`.
2. Convert `port`, `authport` and `reverseproxyauthport` to integers.
3. Show the console's hostname, port, authport, domain and reverse proxy pair.
4. Show the length of the `[JWT] Key`.
5. List which entries from `REQUIRED_INI` are missing. Then build a copy with
   `authport` and the `JWT Key` deleted and show that the copy is missing two
   requirements.

Acceptance criteria — three sections (`(global)`, `Console`, `JWT`) must be returned.
`port` and `authport` must be integers. The broken copy must be missing
`Console.authport` and `JWT.Key`.

## Exercise 4 — Computing expiry from `--years-valid`

`YEARS_VALID_CASES` holds pairs of issue date and validity in years.

To do —

1. Write a helper that adds years to a date. For 29 February the next year does not
   contain that day, so it must be adjusted to the 28th.
2. Reject any case whose validity is under 1 year.
3. Print the issue date, validity, expiry date and day count, one line each. If a
   leap-day adjustment happened, add `leap_day_clamped=yes`.
4. Check that the certificate with the longer validity expires later.

Acceptance criteria — 2026-03-15 plus 2 years is 2028-03-15 with 731 days.
2024-02-29 plus 1 year must be 2025-02-28.

## Exercise 5 — Finding Console/Auth/NATS/OCSP port conflicts

`PORT_PLAN` is the server's official inbound port plan. `EXTRA_LISTENERS` adds two
things that could collide.

To do —

1. Group the listeners using the `(port, protocol)` pair as the key.
2. Treat any group with more than one owner as a conflict.
3. Print the conflicts sorted by port, with the owners sorted alphabetically.
4. Separately show that a pair sharing a port number but not a protocol is not a
   conflict.
5. List the ports below 1024.

Acceptance criteria — there must be exactly one conflict (1323/tcp). Confirm that
4433/udp is not a conflict. The privileged port list must contain 443.

## Exercise 6 — Generating firewall rules from the port plan

Use `PORT_PLAN` to generate a `ufw` rule list.

To do —

1. Build a rule list sorted by port. The format is
   `ufw allow <port>/<proto> comment '<component> <role>'`.
2. Show `ufw default deny incoming` before the list.
3. Show the rule count, the lowest port and the highest port.
4. Generate the list a second time. Both results must be identical.

Acceptance criteria — five rules must be produced. All five ports must appear exactly
once. The lowest must be 443 and the highest 8000.

## Running the lab

```bash
python3 modules/03_ubuntu_server/lab.py
```

Each exercise must print `[OK] exercise_N — ...`. If everything passes, the final
line you will see is
`[PASS] All 6/6 exercises passed successfully.`
