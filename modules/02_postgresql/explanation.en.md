# Module 02 — Preparing PostgreSQL (Ubuntu 24.04)

## Why the database must be prepared first

Every OpenUEM component — the console, the agent worker, the cert-manager worker,
the notification worker — reads from and writes to PostgreSQL. The first question the
installer asks is `DATABASE_URL`. Without a database the installer cannot create the
schema, so the process stops.

That is why the order of work looks like this.

```text
PostgreSQL install → create role + database → test with the URI
→ OpenUEM install (creates the schema) → workers connect
```

If the database layer is wrong, the failures that appear later show up in confusing
forms such as "connection refused" or "password authentication failed", and the root
cause is hard to find. This module rehearses the database layer on its own and makes
the foundation solid for the remaining steps.

## Installing PostgreSQL on Ubuntu 24.04

Ubuntu's default repository includes PostgreSQL. You do not need to pin a version.

```bash
sudo apt update
sudo apt install -y postgresql postgresql-client
```

`postgresql` is the server, and `postgresql-client` provides the client tools,
including `psql`.

```bash
sudo systemctl enable --now postgresql
```

`enable` makes the service start automatically at boot, and `--now` starts it at this
moment as well.

```bash
systemctl status postgresql --no-pager
pg_lsclusters
ss -ltnp | grep 5432
```

The first command shows the service status, the second shows the cluster name and
version, and the third shows which process holds port 5432 open. The default package
on Ubuntu 24.04 is PostgreSQL 16 — re-check it against your version.

## Creating the database and role

PostgreSQL has a superuser named `postgres`. You enter `psql` with that account.

```bash
sudo -u postgres psql
```

Then create the database and a separate role.

```sql
CREATE DATABASE openuem;
CREATE USER openuem_app WITH ENCRYPTED PASSWORD 'change-this-password';
GRANT ALL PRIVILEGES ON DATABASE openuem TO openuem_app;
ALTER DATABASE openuem OWNER TO openuem_app;
\c openuem
GRANT ALL ON SCHEMA public TO openuem_app;
\q
```

The meaning of each line —

- `CREATE DATABASE openuem;` — creates a new database for OpenUEM.
- `CREATE USER ... WITH ENCRYPTED PASSWORD ...` — creates a role for the
  application. `ENCRYPTED` is used so the password is stored as a hash.
- `GRANT ALL PRIVILEGES ON DATABASE ...` — grants privileges at the database level.
- `ALTER DATABASE ... OWNER TO ...` — sets the owner of the database.
- `\c openuem` — connects to that database.
- `GRANT ALL ON SCHEMA public TO ...` — on PostgreSQL 15 and later, the privilege to
  create tables in the `public` schema is off by default. OpenUEM needs this grant in
  order to create its tables.

> Do not use the superuser `postgres` as OpenUEM's connection user.
> Using a separate role for each application is a basic security principle.

## Building the connection URI

OpenUEM needs a URI in order to connect. The form is —

```text
postgres://USER:PASSWORD@HOST:PORT/DATABASE
```

An example —

```text
postgres://openuem_app:change-this-password@localhost:5432/openuem
```

If the password contains special characters, they must be percent-encoded.
According to PostgreSQL's connection string rules, characters such as `:`, `/`, `@`,
`?`, `#`, `&` and `=` must be encoded.

| Character | Code | Character | Code |
|---|---|---|---|
| space | `%20` | `=` | `%3D` |
| `/` | `%2F` | `?` | `%3F` |
| `:` | `%3A` | `#` | `%23` |
| `@` | `%40` | `&` | `%26` |

For example — if the password is `te=st`, it is written as `te%3Dst` in the URI.
If it is not encoded, the URI is split incorrectly and the password ends up wrong.

**Figure 1 — Database preparation order**

```mermaid
flowchart TD
    A["PostgreSQL install<br/>apt / docker"] --> B["role + database<br/>CREATE USER / DATABASE"]
    B --> C["GRANT on schema public"]
    C --> D["Build the URI<br/>percent-encoding"]
    D --> E{"Test with psql"}
    E -->|"fails"| F["Check pg_hba / password / port"]
    F --> D
    E -->|"succeeds"| G["OpenUEM installer<br/>creates the schema"]
```

Figure walkthrough — First, install PostgreSQL. Second, create the role and the
database. Third, grant privileges on the `public` schema. Fourth, percent-encode the
password and build the URI. Fifth, test directly with `psql`. If the test fails, check
`pg_hba.conf`, the password and the port again, then fix the URI. Only once it
succeeds do you continue with the OpenUEM installer. The installer creates the tables
at this step.

## `pg_hba.conf` and the authentication method

PostgreSQL checks every connection against `pg_hba.conf`. On Ubuntu the file is
`/etc/postgresql/<version>/main/pg_hba.conf`.

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

This command prints the path of the file in use.

By default the method is `peer` for the local socket and `scram-sha-256` or `md5` for
TCP (`127.0.0.1/32`). Because OpenUEM connects over TCP, password authentication must
be enabled on the `127.0.0.1/32` line. On RPM-based hosts the documentation specifies
changing `ident` to `md5`.

```bash
sudo systemctl restart postgresql
```

You must restart after editing `pg_hba.conf`. There are situations where a reload is
enough, but the teaching lab uses a restart.

**Figure 2 — Connection path from a worker to the database**

```mermaid
sequenceDiagram
    participant W as "Agent worker"
    participant P as "PostgreSQL"
    participant H as "pg_hba.conf"
    W->>P: "postgres://openuem_app:...@localhost:5432/openuem"
    P->>H: "find a rule (host 127.0.0.1/32)"
    H-->>P: "scram-sha-256"
    P->>P: "check the password"
    P-->>W: "connection accepted"
    W->>P: "CREATE TABLE ... (schema)"
    P-->>W: "OK"
```

Figure walkthrough — The worker connects with the URI. PostgreSQL looks up the matching
line in `pg_hba.conf` by connection type and address. That line returns the
authentication method. If the password is correct, the connection is accepted and the
worker can create tables. In this figure you can see where the path can fail — the rule
does not match, the method is wrong, or the password is wrong.

## Testing the connection

Before starting the installer you must test the URI directly.

```bash
psql "postgres://openuem_app:change-this-password@localhost:5432/openuem" -c "SELECT current_user, current_database();"
```

```text
# simulated output — illustrative
 current_user | current_database
--------------+------------------
 openuem_app  | openuem
(1 row)
```

From this output you can confirm that the user and database names are correct. To keep
the password out of the shell history you can use `PGPASSWORD`.

```bash
PGPASSWORD='change-this-password' psql -h localhost -U openuem_app -d openuem -c "SELECT 1;"
```

`-h localhost` instructs the client to connect over TCP. Without `-h` it uses the local
socket and you end up testing with `peer` authentication. That therefore cannot match
OpenUEM's situation.

## Backup and restore

The database holds all of OpenUEM's data — agent reports, deployment records, user and
certificate metadata. It must be backed up together with the certificate folder.

```bash
pg_dump -Fc -h localhost -U openuem_app -d openuem -f openuem.dump
```

`-Fc` is the custom format, and it can be restored with `pg_restore`.

```bash
createdb -h localhost -U openuem_app openuem_restore
pg_restore -h localhost -U openuem_app -d openuem_restore openuem.dump
```

While restoring, the OpenUEM services must be stopped. Otherwise the workers can mix in
unfinished transactions.

## Clean reinstall

If you want to start over from scratch in the lab, there are two approaches.

1. **Drop the database and create it again** — the cleanest approach. `DROP DATABASE openuem;`
   followed by re-creating it.
2. **Drop the tables** — keep the database and drop only the OpenUEM tables. The
   documentation lists them as `\c openuem` followed by `DROP TABLE "agents" CASCADE;`
   and so on.

```sql
\c openuem
DROP TABLE "certificates" CASCADE;
DROP TABLE "agents" CASCADE;
DROP TABLE "computers" CASCADE;
DROP TABLE "deployments" CASCADE;
DROP TABLE "profiles" CASCADE;
DROP TABLE "tasks" CASCADE;
DROP TABLE "users" CASCADE;
\q
```

When dropping, `CASCADE` also drops the dependent foreign keys. So if there is data you
need, take a backup first.

## Installing the database in a container

If you use `openuem-docker`, the compose file creates PostgreSQL for you automatically.
These values must be set in `.env`.

```text
DATABASE_DB_NAME=openuem
DATABASE_PORT=5432
DATABASE_USER=openuem
DATABASE_PASSWORD=change-this-dbpassword
OPENUEM_DATABASE_URL=postgres://openuem:change-this-dbpassword@openuem-db:5432/openuem
```

Here the host name is not `localhost` but the compose service name (`openuem-db`).
Containers reach each other by service name.

| Aspect | Native PostgreSQL | Compose PostgreSQL |
|---|---|---|
| install | `apt install postgresql` | the image is pulled automatically |
| data location | `/var/lib/postgresql` | named volume |
| backup | `pg_dump` | `docker compose exec` + `pg_dump` |
| upgrade | package upgrade | change the image tag |
| maintenance | you do it yourself | compose manages it |
| suitable for | production, a dedicated DB server | lab, single-host deployment |

## Points to watch in production

- When the password is placed in `.env` or `openuem.ini`, restrict the file
  permissions (`chmod 600`).
- Do not expose the database port (5432) to the internet. Only the host that runs the
  OpenUEM components should be able to connect.
- Check disk space in advance. The database grows as agent reports accumulate.
- Before a PostgreSQL version upgrade, take a backup with `pg_dump` and test the
  restore on a separate host.
- Keep the time zone and clock synchronised with NTP. Certificate and log timestamps
  can otherwise be wrong.

## Self-check questions

**1. Why is `GRANT ALL ON SCHEMA public` needed?**
On PostgreSQL 15 and later, the privilege to create tables in the `public` schema is
off for ordinary users. OpenUEM needs this grant in order to create the schema.

**2. If the password contains `@`, how is it written in the URI?**
It is encoded as `%40`. Otherwise the URI parser splits it incorrectly as the host
part.

**3. Why add `-h localhost` when testing with `psql`?**
Without `-h` the client uses the local Unix socket, which means `peer` authentication.
OpenUEM connects over TCP, so you must test through the same path.

**4. In a Compose deployment, what is the host in `OPENUEM_DATABASE_URL`?**
Not `localhost`, but the name of the database service (for example `openuem-db`).
It is resolved by service name inside the container network.

## Technical review notes

- The SQL and `pg_hba.conf` details are taken from openuem.eu/docs
  (Advanced Topics → Postgres).
- The PostgreSQL version on Ubuntu 24.04 (16) can differ per distribution — re-check
  it against your version.
- `GRANT ALL ON SCHEMA public` is based on the default change in PostgreSQL 15+.
  Older versions may not need it.
- The full OpenUEM table list can change between versions, so use the list in the
  documentation.
