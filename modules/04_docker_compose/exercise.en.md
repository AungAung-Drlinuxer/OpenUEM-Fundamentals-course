# Module 04 — Exercises

Six exercises on container deployment.

```bash
python3 modules/04_docker_compose/lab.py
```

## Exercise 1 — `.env` requirements

In the following `.env`, one of the 18 required keys is missing. Which key is it?
State the completeness ratio.

```text
DATABASE_DB_NAME=openuem
DATABASE_PORT=5432
DATABASE_USER=openuem
DATABASE_PASSWORD=db-secret
OPENUEM_DATABASE_URL=postgres://openuem:db-secret@openuem-db:5432/openuem
OPENUEM_ORGNAME=Example Org
OPENUEM_COUNTRY=MM
OPENUEM_DOMAIN=openuem.example
CONSOLE_HOST=console.openuem.example
CONSOLE_PORT=1323
CONSOLE_AUTH_PORT=1324
CONSOLE_JWT_KEY=
NATS_HOST=nats.openuem.example
NATS_PORT=4433
OPENUEM_NATS_SERVERS=nats.openuem.example:4433
OCSP_URL=http://ocsp.openuem.example:8000
OCSP_HOST=ocsp.openuem.example
OCSP_PORT=8000
```

## Exercise 2 — JWT key policy

The default key of `.env-example` is `averylongsecret`. Evaluate the following three
candidates against the policy (at least 32 characters, must not be the default value,
must not be empty).

```text
averylongsecret
(empty)
9f2c41ab7d3e58c0a6b1f4d92e7c0a38
```

## Exercise 3 — Hosts entry

The lab host's IP is `192.168.1.43`. Build one hosts entry line for the NATS host,
the OCSP host, and the console host. If a name repeats, add it only once.
`127.0.0.1` must not appear.

## Exercise 4 — Reverse proxy values

Check the following three situations as valid or invalid.
If no proxy is used, both ports must be empty. If a proxy is used,
both the host and the two ports must be filled.

```text
host=            console_port=       auth_port=
host=console...  console_port=443     auth_port=4443
host=console...  console_port=443     auth_port=
```

## Exercise 5 — Startup order

The dependencies of the services are as follows.

```text
openuem-db      (none)
nats            openuem-db
ocsp            openuem-db
cert-manager    openuem-db
agent-worker    openuem-db, nats
console         openuem-db, nats, agent-worker
```

Write the correct startup order according to the dependencies.

## Exercise 6 — Teardown risk

Split the following three commands into "data remains" and "data lost".

```text
docker compose stop
docker compose down
docker compose down -v
```
