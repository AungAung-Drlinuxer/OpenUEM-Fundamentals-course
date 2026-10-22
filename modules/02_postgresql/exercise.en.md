# Module 02 — Exercises

Six exercises on PostgreSQL preparation and connections.
The solutions are in `solution.en.md`.

```bash
python3 modules/02_postgresql/lab.py
```

## Exercise 1 — Validating `.env` requirements

The `.env` below contains only three of the five required keys.
Which two keys are missing? Also state the completeness ratio.

```text
DATABASE_DB_NAME=openuem
DATABASE_PORT=5432
DATABASE_USER=openuem_app
OPENUEM_DOMAIN=openuem.example
CONSOLE_HOST=console.openuem.example
```

The required keys are `DATABASE_DB_NAME`, `DATABASE_PORT`, `DATABASE_USER`,
`DATABASE_PASSWORD`, `OPENUEM_DATABASE_URL`.

## Exercise 2 — URI percent-encoding

The password `te=st@lab` has to be placed in a connection URI.
How are `=` and `@` encoded? After encoding, state the host, port and database name.

## Exercise 3 — `pg_hba.conf` decision

The following rules exist, in order.

```text
local   all  all                  peer
host    all  all  127.0.0.1/32    scram-sha-256
host    all  all  ::1/128         scram-sha-256
```

Give the authentication method for three kinds of TCP connection —
`127.0.0.1/32`, `10.0.0.5/32`, and the local socket.

## Exercise 4 — Classifying errors

Sort the four errors below by cause category
(`credentials`, `hba-rule`, `service-or-port`, `wrong-database`).

```text
FATAL:  password authentication failed for user "openuem_app"
FATAL:  no pg_hba.conf entry for host "10.0.0.5", user "openuem_app", database "openuem"
could not connect to server: Connection refused
FATAL:  database "openuem" does not exist
```

## Exercise 5 — Schema privileges

The ACL of the `public` schema is as follows.

```text
openuem_app=UC/openuem_app,postgres=CTc/postgres
```

Does `openuem_app` have the create privilege? Does `readonly_user` have any privileges?

## Exercise 6 — Backup/restore runbook order

Put the following five steps in the correct order.

```text
pg_restore -d openuem_restore
start OpenUEM services
pg_dump -Fc openuem
stop OpenUEM services
createdb openuem_restore
```
