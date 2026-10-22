# Module 02 — Solutions

The outputs below are the real output of `python3 modules/02_postgresql/lab.py`.

## Exercise 1 — Validating `.env` requirements

`DATABASE_PASSWORD` and `OPENUEM_DATABASE_URL` are not present.
Only three of the five required keys are complete, so the `.env` cannot be used.
Without `OPENUEM_DATABASE_URL` the components cannot connect to the database.

```text
[OK] exercise_1 — env validation: 3/5 required keys present; missing=DATABASE_PASSWORD,OPENUEM_DATABASE_URL
```

## Exercise 2 — URI percent-encoding

`=` is encoded as `%3D`, and `@` as `%40`.
The result is `te%3Dst%40lab`, and the URI can be built with host `localhost`, port
`5432`, database `openuem`.

```text
[OK] exercise_2 — uri encoding: te=st@lab -> te%3Dst%40lab; host=localhost port=5432 db=openuem
```

## Exercise 3 — `pg_hba.conf` decision

For `127.0.0.1/32` the second rule matches, so the method is `scram-sha-256`.
For `10.0.0.5/32` no rule matches, so the connection is rejected.
For the local socket the first rule, `peer`, applies.

```text
[OK] exercise_3 — pg_hba: 127.0.0.1/32=scram-sha-256, 10.0.0.5/32=reject, local=peer
```

## Exercise 4 — Classifying errors

Look at the key phrase in the text and classify by cause.
`password authentication failed` is credentials, `no pg_hba.conf entry` is a missing
rule, `Connection refused` is a service that is not listening, and `does not exist` is
a wrong database name.

```text
[OK] exercise_4 — error causes: credentials,hba-rule,service-or-port,wrong-database
```

## Exercise 5 — Schema privileges

The ACL contains `openuem_app=UC/openuem_app`, so both `U` (usage) and `C` (create)
are present. There is no entry for `readonly_user`, so it has no privileges.

```text
[OK] exercise_5 — schema privileges: openuem_app=UC create=True; readonly_user=none
```

## Exercise 6 — Backup/restore runbook order

The services must be stopped before the dump is taken. After the dump, create a new
database for the restore and run `pg_restore`. At the end the services are started
again.

```text
[OK] exercise_6 — runbook order: stop OpenUEM services -> pg_dump -Fc openuem -> createdb openuem_restore -> pg_restore -d openuem_restore -> start OpenUEM services
```
