# Module 04 — Deployment with Docker/Podman

## When the container route is appropriate

OpenUEM is officially supported both when installed from native packages (Module 03)
and when installed with containers.
The container route is more suitable in the following situations.

- you want a lab or a demo within a few hours
- you do not want to install PostgreSQL and seven services separately on the host
- you need a disposable environment
- you want to control version-to-version change with image tags

Conversely, in production, if you want to maintain the host's PostgreSQL separately,
or if the company's package management rules do not permit containers,
the native route is more appropriate.

## Requirements

- Docker Engine and the Compose plugin (or Podman and podman-compose)
- a domain that resolves through DNS (or a hosts override for the lab)
- the ports must be free — 1323, 1324, 4433, 8000, 5432
- disk space — for PostgreSQL data and the images

```bash
docker --version
docker compose version
```

The first command shows the Docker version, the second shows whether the Compose
plugin is present. If the Compose plugin is not present, `docker-compose` (hyphen)
must be used.

## Getting the repository

```bash
git clone https://github.com/open-uem/openuem-docker
cd openuem-docker
```

The `openuem-docker` repository contains the compose file and `.env-example`.

```bash
cp .env-example .env
```

The file name must be `.env`. It must have no extension in its name.
Docker reads the environment variables only under this name.

## Key `.env` values

| Variable | Meaning | Required |
|---|---|---|
| `DATABASE_DB_NAME` | database name (created on the first start) | Yes |
| `DATABASE_PORT` | public port of the database | Yes |
| `DATABASE_USER` | database user | Yes |
| `DATABASE_PASSWORD` | database password | Yes |
| `OPENUEM_DATABASE_URL` | URI used by the components | Yes |
| `OPENUEM_ORGNAME` | organisation name | Yes |
| `OPENUEM_COUNTRY` | country code | Yes |
| `OPENUEM_DOMAIN` | DNS domain | Yes |
| `CONSOLE_HOST` | console host name | Yes |
| `CONSOLE_PORT` | console port (1323) | Yes |
| `CONSOLE_AUTH_PORT` | auth port (1324) | Yes |
| `CONSOLE_JWT_KEY` | JWT signing key | Yes |
| `NATS_HOST` | NATS host name | Yes |
| `NATS_PORT` | NATS port (4433) | Yes |
| `OPENUEM_NATS_SERVERS` | NATS list used by the agents | Yes |
| `OCSP_URL` | OCSP responder URL | Yes |
| `OCSP_HOST` | OCSP host name | Yes |
| `OCSP_PORT` | OCSP port (8000) | Yes |
| `REVERSE_PROXY_HOST` | host when a reverse proxy is used | No |
| `REVERSE_PROXY_CONSOLE_PORT` | port from the proxy to the console | No |
| `REVERSE_PROXY_AUTH_PORT` | port from the proxy to auth | No |
| `TZ` | container time zone | No |

The format of `OPENUEM_DATABASE_URL` is —

```text
postgres://USER:PASSWORD@openuem-db:5432/DATABASE
```

Here the host is not `localhost` but the compose service name (`openuem-db`).
If the password contains special characters, the percent-encoding rule described
in Module 02 must be followed.

## Rotating the JWT key

`.env-example` contains a default value. If all users know the same key,
a token can be forged.

```bash
openssl rand -hex 16
```

This command produces 32 hex characters. The result must be put into
`CONSOLE_JWT_KEY`.

```text
# simulated output — illustrative
9f2c41ab7d3e58c0a6b1f4d92e7c0a38
```

That value must not be put into version control. `.env` must be listed in
`.gitignore`.

## Starting the stack

```bash
docker compose up -d
```

`-d` is detached mode and returns the terminal.
The first start includes pulling the images and creating the database, so it may
take a few minutes.

**Figure 1 — Compose service layout**

```mermaid
flowchart TD
    L["docker compose up -d"] --> D[("openuem-db<br/>PostgreSQL 5432")]
    D --> N["nats<br/>4433"]
    D --> CM["cert-manager worker"]
    N --> AW["agent worker"]
    CM --> C["console<br/>1323 / 1324"]
    AW --> C
    D --> O["ocsp responder<br/>8000"]
    C --> P["reverse proxy (optional)"]
```

Figure walkthrough — compose creates the services at the same time.
First, the database container starts and, on the first start, creates the database
and the user from the `.env` values. Second, NATS and the workers connect to the
database. Third, the console uses the workers and the database to open the web UI.
Fourth, if a reverse proxy is configured, it handles HTTPS in front of the console.
If the workers start before the database is available, connections may fail during
the first seconds, so the container log must be checked.

## Verification

```bash
docker compose ps
```

Shows the state (running/healthy) of each service.

```bash
docker compose logs --tail=50 console
```

Shows the last fifty log lines of the console container.
If startup fails, the cause appears at this point.

```bash
docker compose exec openuem-db psql -U openuem -d openuem -c "\dt"
```

Shows the tables inside the database. If the tables are present, schema creation
succeeded.

The console is opened in the browser with `http://CONSOLE_HOST:1323`.
If a reverse proxy is configured, it is `https://REVERSE_PROXY_HOST`.

## Name resolution in a lab without DNS

If the lab has no DNS server, the hosts file can be edited.
On Linux it is `/etc/hosts`, on Windows
`C:\Windows\System32\drivers\etc\hosts`, on macOS `/private/etc/hosts`.

```text
192.168.1.43  nats.openuem.example  ocsp.openuem.example  console.openuem.example
```

The host's LAN IP must be entered in place of `192.168.1.43`.
`localhost` or `127.0.0.1` must not be used. Each container resolves itself
through those names and therefore cannot reach another container.

Docker copies these hosts file entries into the containers.
The names defined in `.env` must therefore match the hosts entries.

## Reverse proxy and ports

If no reverse proxy is used, the `REVERSE_PROXY_*` values must be left empty.

```text
REVERSE_PROXY_HOST=
REVERSE_PROXY_CONSOLE_PORT=
REVERSE_PROXY_AUTH_PORT=
```

If a reverse proxy is used, Caddy can be used. In the documentation,
Caddy is the proxy supported for compose deployment.
In that situation the host and the ports must be filled in.

**Figure 2 — First startup verification path**

```mermaid
sequenceDiagram
    participant A as "Admin"
    participant C as "Compose"
    participant D as "openuem-db"
    participant W as "console"
    A->>C: "docker compose up -d"
    C->>D: "create db + user (first start)"
    D-->>C: "ready"
    C->>W: "start console"
    A->>C: "docker compose ps"
    C-->>A: "services running"
    A->>W: "http://console:1323"
    W-->>A: "login page"
```

Figure walkthrough — first, the administrator starts compose. Second, the database
container creates the database and the user. Third, the console container starts.
Fourth, the administrator checks the state with `docker compose ps`.
Fifth, the console is opened from the browser and the appearance of the login page
confirms that basic connectivity succeeded.

## Upgrade and teardown

```bash
git pull
docker compose pull
docker compose up -d
```

The first command fetches the new compose file and `.env-example`.
The second pulls the new image tags. The third recreates the containers that
changed. A database dump must be taken before upgrading.

```bash
docker compose down
```

Stops and deletes the containers. The volumes remain, so the data
is not lost.

```bash
docker compose down -v
```

`-v` deletes the volumes as well. All database data is lost.
It must be used only when the lab is to be restarted from scratch.

| Command | Container | Volume/Data |
|---|---|---|
| `docker compose stop` | stopped | remains |
| `docker compose down` | deleted | remains |
| `docker compose down -v` | deleted | deleted |

## Native and container comparison

| Aspect | Native (Ubuntu 24.04) | Container (compose) |
|---|---|---|
| Install time | configure each package | fill in `.env` and start once |
| Service management | `systemctl` | `docker compose` |
| Database | the host's PostgreSQL | container + volume |
| Upgrade | apt/dnf | image tag |
| Log | journald / file | `docker compose logs` |
| Teardown | package remove + DB drop | `down -v` |
| Production suitability | high | medium (single host) |

## Practices to watch in the workplace

- `.env` contains secrets, so its permission must be `600`.
- `docker compose down -v` must not be used casually. The database is lost.
- If ports overlap, the containers cannot start. The port list described in
  Module 01 must be checked in advance.
- A hosts override must be used only in the lab. In production, DNS must
  be used.
- Setting the container time zone (`TZ`) keeps log times consistent.
- Without a reverse proxy the console is reachable only over HTTP.
  In production HTTPS is mandatory.

## Self-check questions

**1. Why must the database host in `.env` be the service name rather than
`localhost`?**
Inside each container, `localhost` points to itself.
To reach another service within the compose network, it must be resolved by
service name.

**2. What is the difference between `docker compose down` and `down -v`?**
`down` deletes only the containers and the volumes remain.
`down -v` deletes the volumes as well, so the database data is lost.

**3. Which IP must be entered in the hosts file in the lab?**
The host's LAN IP must be entered. `127.0.0.1` must not be used.

**4. How can a JWT key be generated?**
`openssl rand -hex 16` yields 32 hex characters.
The default value must not be used.

## Technical review notes

- The `.env` values, the hosts override, and the Caddy details are taken from
  openuem.eu/docs (Installation → Server → Docker/Podman) and from the
  `open-uem/openuem-docker` repository.
- The compose service name (`openuem-db`) can change from file to file in the
  repository — it needs to be rechecked per version.
- For deployments before 2025 December 22 there is a different legacy compose
  file. That point is covered in the Legacy section of the documentation.
- Caddy is the supported proxy in the documentation for a reverse proxy.
  For other proxies, the headers and ports must be tested yourself.
