# Module 04 — Solutions

The outputs below are the real output of `python3 modules/04_docker_compose/lab.py`.

## Exercise 1 — `.env` requirements

`CONSOLE_JWT_KEY` is empty. Without the key the console cannot sign JWTs,
so login is impossible. The remaining 17 keys are complete.

```text
[OK] exercise_1 — env: 17/18 required keys set; missing=CONSOLE_JWT_KEY
```

## Exercise 2 — JWT key policy

The default value `averylongsecret` is only 15 characters and is a publicly known
value, so it is rejected. The empty value is rejected.
A random 32-character hex string is accepted.

```text
[OK] exercise_2 — jwt key policy: default,empty,ok; accepted_length=32
```

## Exercise 3 — Hosts entry

The three names are sorted alphabetically and written on a single line.
The NATS host was added twice, but the duplicate is removed.

```text
[OK] exercise_3 — hosts entry: 192.168.1.43  console.openuem.example  nats.openuem.example  ocsp.openuem.example
```

## Exercise 4 — Reverse proxy values

First — no proxy is used, so the ports are empty; valid.
Second — both the host and the two ports are present; valid.
Third — the host is present but the auth port is not; invalid.

```text
[OK] exercise_4 — reverse proxy: no-proxy=ok, full=ok, host-without-auth-port=invalid
```

## Exercise 5 — Startup order

The service with no dependency starts first. After the database,
dependants start one level at a time. Services on the same level
are ordered by name.

```text
[OK] exercise_5 — startup order: openuem-db -> cert-manager -> nats -> ocsp -> agent-worker -> console
```

## Exercise 6 — Teardown risk

`stop` and `down` do not delete the volume, so the data remains.
`down -v` deletes the volume as well, so the data is lost.

```text
[OK] exercise_6 — teardown: data-safe=docker compose down | docker compose stop; data-loss=docker compose down -v
```
