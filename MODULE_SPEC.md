# MODULE_SPEC — OpenUEM Endpoint Management Fundamentals

Decomposition of the learner-supplied 7-section outline into 10 modules
(PostgreSQL, Ubuntu 24.04 server install and Docker are separate modules). Every
writing task: read `WRITING_RULES.md` first, then your module's section below.
Write EXACTLY the five files (`README.md`, `explanation.md`, `exercise.md`,
`solution.md`, `lab.py`) into your module folder and no others. No git
operations, no edits to root files, no edits to other modules.

**Environment reality:** study machines do not run OpenUEM. All labs are pure
stdlib simulations (fixtures + arithmetic + text processing). All command
outputs in docs are simulated fixtures (see WRITING_RULES.md §SIMULATION
policy). Commands themselves must be real commands from the official docs.

---

## §Verified facts (the ONLY permitted source of numbers and names)

Source: openuem.eu/docs (Server installation, Docker/Podman, Agent install,
Console, Administration, Advanced Topics) and the open-uem GitHub project.

### Product shape
- OpenUEM = self-hosted endpoint management: agents on endpoints report
  inventory and security state to a server; administrators act from a web
  console.
- Supported: Windows (desktop and server), Debian-based (Debian, Ubuntu, Mint),
  RPM-based (Fedora, Alma, Rocky, RHEL), macOS agents for Intel and Apple
  Silicon.
- Multi-tenancy: multiple organizations, each with sites; one organization is
  always the default and cannot be removed.
- Console languages: English, Spanish, German.
- Authentication: client certificates, or OpenID Connect through Authelia,
  Authentik, Keycloak or Zitadel.

### Components
- `openuem-console` — web console and auth server (1323 console, 1324 auth).
- `openuem-nats-service` — NATS broker agents connect to (4433).
- `openuem-agent-worker` — consumes agent reports, writes to PostgreSQL.
- `openuem-cert-manager-worker` — issues agent/user certificates.
- `openuem-notification-worker` — outgoing notifications (SMTP).
- `openuem-ocsp-responder` — certificate revocation checks (8000).
- `openuem-cert-manager` — CLI to create the CA and component certificates.
- `openuem-server-updater` — packaged as a service, creates `openuem.ini`.
- PostgreSQL — all persistent state; required before installation.
- Agent-side services: `openuem-agent`, `openuem-agent-updater`; agent runs an
  SFTP server (2022) and a VNC proxy (1443) when enabled.

### PostgreSQL facts (Advanced Topics → Postgres)
```
sudo apt install -y postgresql
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo apt install postgresql-client
sudo -u postgres psql
```
Inside `psql`:
```
CREATE DATABASE openuem;
CREATE USER test WITH ENCRYPTED PASSWORD 'test';
GRANT ALL PRIVILEGES ON DATABASE openuem TO test;
ALTER DATABASE openuem OWNER TO test;
\q
```
- Connection URI: `postgres://user:password@host:5432/openuem`.
- Special characters in the URI must be percent-encoded (Postgres libpq rule):
  `te=st` becomes `te%3Dst`.
- Fedora note: `/var/lib/pgsql/data/pg_hba.conf` must use `md5` instead of
  `ident` for `127.0.0.1/32`, then restart the service.
- Windows: install PostgreSQL, create a login/group role with LOGIN privilege,
  create the database owned by that role, grant privileges.
- Clean reinstall: connect with `\c openuem` and `DROP TABLE ... CASCADE` for
  the OpenUEM tables (agents, computers, applications, deployments, profiles,
  tasks, users, sessions, certificates, updates, system_updates, ...).

### Docker / Podman facts
```
git clone https://github.com/open-uem/openuem-docker
cp .env-example .env
docker compose up -d
```
- `.env` must have no extension and a leading dot.
- `DATABASE_DB_NAME`, `DATABASE_PORT`, `DATABASE_USER`, `DATABASE_PASSWORD`
  create the database on first start; `OPENUEM_DATABASE_URL` is the URI used by
  components.
- Required: `OPENUEM_ORGNAME`, `OPENUEM_COUNTRY`, `OPENUEM_DOMAIN`,
  `OPENUEM_DATABASE_URL`, `CONSOLE_HOST`, `CONSOLE_PORT` (1323),
  `CONSOLE_AUTH_PORT` (1324), `CONSOLE_JWT_KEY`, `NATS_HOST`, `NATS_PORT`
  (4433), `OPENUEM_NATS_SERVERS`, `OCSP_URL`, `OCSP_HOST`, `OCSP_PORT` (8000).
- `REVERSE_PROXY_HOST`, `REVERSE_PROXY_CONSOLE_PORT`,
  `REVERSE_PROXY_AUTH_PORT` — set to empty when no reverse proxy is used.
- JWT key: replace with a random 32-character string.
- Lab without DNS: add `{YOUR_LOCAL_IP} {NATS_HOST} {OCSP_HOST} {CONSOLE_HOST}`
  to the hosts file. Use the LAN IP, never `localhost`/`127.0.0.1`, because
  each container would resolve to itself.
- Demo domain used by `.env-example`: `openuem.example`.
- Caddy is the supported reverse proxy for the compose deployment.
- Podman users substitute `podman compose`.

### Server install facts (Linux)
Debian/Ubuntu: packages from the OpenUEM apt repository. RPM: repository file
`/etc/yum.repos.d/openuem.repo` pointing at `https://rpm.openuem.eu/packages`,
GPG key `https://rpm.openuem.eu/pgp-key.public`.
- `openuem-server-updater` needs `crudini` (may require EPEL:
  `dnf install epel-release`).
- Certificate tree under `/etc/openuem-server/certificates/{ca,nats,ocsp,
  notification-worker,agents-worker,cert-manager-worker,console,updater,agents,users}`.
- Certificate creation example:
  ```
  sudo openuem-cert-manager client-cert --name "OpenUEM Agent" --dst ./agents \
    --type="agent" --org "$ORGNAME" --country "$COUNTRY" --province "$ORGPROVINCE" \
    --locality "$ORGLOCALITY" --address "$ORGADDRESS" --years-valid 2 \
    --filename "agent" --ocsp "http://$OCSP_SERVER:$OCSP_PORT" \
    --description "Agent certificate" --cacert ./ca/ca.cer --cakey ./ca/ca.key \
    --dburl "$DATABASE_URL"
  ```
- Configuration file: `/etc/openuem-server/openuem.ini`, shared by all
  components; keys include `CACert`, `CAKey`, `NATSCert`, `NATSKey`,
  `OCSPCert`, `OCSPKey`, `NotificationWorkerCert`, `ConsoleCert`, and a
  `[Console]` section with `hostname`, `port`, `authport`,
  `reverseproxyserver`, `reverseproxyauthport`, `domain`, plus `[JWT] Key`.
- Start order used in the docs: ocsp-responder, nats-service,
  server-updater, agent-worker, notification-worker, cert-manager-worker,
  console.
- Installer creates an unprivileged `openuem` user that owns config,
  certificates and logs.

### Agent facts
Windows: `openuem-agent-setup.exe` supports silent install
(`/VERYSILENT`) with flags `/cacert=`, `/cert=`, `/key=`, `/sftpcert=`,
`/tenantid=`, `/siteid=`, `/server=domain:port`, `/sftp=port`, `/vnc=port`.
Certificates can be placed next to the installer instead of using flags.
`/tenantid` and `/siteid` must be supplied together.
Linux Debian: `apt install openuem-agent` (or `apt install ./openuem-agent_0.7.0_amd64.deb`),
interactive questions for NATS server, SFTP port, VNC proxy port; certificates
in `/etc/openuem-agent/certificates` as `ca.cer`, `sftp.cer`, `agent.cer`,
`agent.key`; then
`systemctl restart openuem-agent` and `systemctl restart openuem-agent-updater`.
RPM: `dnf install -y openuem-agent`, edit `/etc/openuem-agent/openuem.ini`
(`[NATS] NATSServers=host:4433`, `SFTPPort=`, VNC port), certificates in the
same folder, `chown openuem-agent:openuem-agent`, then `systemctl enable --now`
both services.
- Agent log: `openuem-log.txt` in the agent `logs` folder; Windows agent folder
  is `C:\Program Files\OpenUEM Agent`.
- Outbound requirement: the agent must reach the NATS server host and port.

### Console behaviour facts
- Agent states: **Waiting for admission** (reports arrive, not manageable, not
  in charts), **Enabled**, **Disabled**.
- Default report interval: 60 minutes (Admin → General Settings → Agents report
  frequency).
- Admission issues a `server.cer`/`server.key` pair for the agent's SFTP and
  VNC proxy TLS.
- Enabled-agent actions: force report, disable, regenerate certificate, force
  restart, show agent log (over SFTP), settings (SFTP on/off, remote
  assistance, ports, debug mode).
- Agents check for new profiles every 30 minutes (configurable in General
  Settings).
- Inventory tabs: overview, hardware, operating system, monitors, logical
  disks (BitLocker status), network adapters, printers, shares, applications,
  security.
- Security view: antivirus enabled/updated, Windows update download/install
  configuration, pending updates, update history; Linux pending security
  updates; PDF/CSV report with filters preserved.
- Software view: installed software aggregated by name, publisher, install
  count; PDF/CSV export.
- Package deployment: Windows via WinGet, Linux via Flatpak, macOS via
  HomeBrew; OpenUEM refreshes those catalogues daily; uninstall uses the same
  flow; requests queue in NATS for agents that are offline.
- WinGet may need Microsoft Store and App Installer updates on fresh Windows;
  HomeBrew must be installed manually on macOS.
- Profiles: desired-state groups of tasks applied by agents. Task families:
  install/uninstall packages (WinGet/Flatpak/Brew), registry keys, local users,
  local groups, PowerShell scripts (Windows), shell scripts (Linux/macOS),
  MSI packages on Windows. Windows uses WinGet configuration (DSC); Linux and
  macOS use Ansible.
- Dashboard: agents reporting in the last 24 hours, platform mix, OS versions;
  red section = agents not reporting, pending updates, disabled antivirus,
  agent/app updates; green = counts of users, apps, tags; blue = component
  status. Refreshes every 5 minutes by default.
- Users: certificate login or OpenID Connect; states Pending email
  confirmation → Review request → Certificate sent → Completed; CSV import
  skips approval; regenerate certificate revokes the old one.
- Organizations: name plus initial site name; CSV import supported; default
  organization cannot be deleted.
- Remote endpoints (identified with DNS plus reported IP) cannot use file
  browsing, remote assistance or WOL.

### Reports / integrations
- PDF and CSV export exist in agents, computers, security and software views,
  preserving active filters and sorting.
- SMTP settings are required for user invitation and registration mail.
- No native Prometheus endpoint is documented; monitoring integration in this
  course is described as an operational pattern (export CSV/PDF, poll
  component health), never as a built-in feature.

Release-dependent claims (mark "version အလိုက် ပြန်စစ်ရန် လိုသည်"):
package versions, exact console menu labels, dashboard card names, supported
Identity Provider list, NetBird integration, RustDesk/RDP support details.

---

## Module 01 — Introduction to OpenUEM (`01_introduction`)
Teach: endpoint management problem, self-hosted versus SaaS, component map,
lifecycle, capabilities, lab planning. Two figures minimum: component
topology; lifecycle state machine.

Lab themes (6): lifecycle transition validation; component-to-port mapping;
report-freshness classification from timestamps; capability matrix lookup;
lab port plan conflict detection; incident triage ordering.

## Module 02 — PostgreSQL preparation (`02_postgresql`)
Teach: why the database comes first; install on Ubuntu 24.04 with apt and on
RPM hosts; role/database creation in psql; `GRANT ... ON SCHEMA public`;
connection URI and percent-encoding; `pg_hba.conf` methods; connectivity test;
backup/restore; clean reinstall; native versus containerised database.
Figures: preparation order; connection path through pg_hba.

Lab themes (6): required `.env` key validation; URI percent-encoding;
pg_hba rule resolution; connection error classification; schema privilege
check; backup/restore runbook ordering.

## Module 03 — Installing OpenUEM on Ubuntu 24.04 Server (`03_ubuntu_server`)
Teach: prerequisites and DNS name; OpenUEM apt repository; package-to-role
map; certificate tree and `openuem-cert-manager`; `openuem.ini`; service
start order; health verification; reverse proxy (Caddy/nginx); hardening;
first login. Figures: install sequence; certificate/trust layout.

Lab themes (6): package→role mapping; service start-order validation; ini
section parsing; certificate expiry from `--years-valid`; port conflict
detection across console/auth/NATS/OCSP; firewall rule generation.

## Module 04 — Docker/Podman deployment (`04_docker_compose`)
Teach: when containers fit; clone `openuem-docker`; `.env` creation and
required variables; JWT key policy; `docker compose up -d`; verification;
hosts overrides for a DNS-less lab; reverse proxy variables; upgrades;
teardown safety; native versus container comparison.
Figures: compose service layout; first startup verification path.

Lab themes (6): required `.env` validation; JWT key policy; hosts entry
generation; reverse-proxy consistency; startup order from dependencies;
teardown data-loss classification.

## Module 05 — Agent deployment (`05_agent_deployment`)
Teach: agent duty cycle; four certificates; Windows silent flags; Debian and
RPM installs; macOS; ports; logs. Figures: agent bootstrap sequence;
certificate placement per platform.

Lab themes (6): silent-install flag builder; certificate file check per OS;
NATS URL validation; report interval arithmetic; log triage mapping; upgrade
risk classification.

## Module 06 — Enrollment and organization (`06_enrollment_organization`)
Teach: states and transitions; admission; report frequency; orgs/sites; tags;
users and roles; CSV import. Figures: admission state machine; org/site/tag
hierarchy.

Lab themes (6): state transition validation; admission queue summary;
org/site assignment resolution; CSV import validation; role capability
matrix; certificate lifecycle states.

## Module 07 — Device management basics (`07_device_management`)
Teach: inventory tabs; package deployment per platform; queues; profiles and
tasks; remote assistance/SFTP/WOL constraints; health indicators. Figures:
deployment request path; profile application loop.

Lab themes (6): inventory completeness scoring; package manager selection per
OS; deployment request queue simulation; profile task validation; tag filter
selection; health flag aggregation.

## Module 08 — Patch management and automation (`08_patch_automation`)
Teach: Windows update visibility; Linux security updates; detect→stage→deploy
→verify; maintenance windows; validation matrix; automation with profiles;
compliance metrics. Figures: patch pipeline; maintenance window gate.

Lab themes (6): pending-update counts; maintenance window eligibility;
patch wave planner; validation matrix; compliance percentage; automation
trigger selection.

## Module 09 — Reporting and troubleshooting (`09_reporting_troubleshooting`)
Teach: report types and filters; dashboard triage; component health; layered
connectivity diagnosis; common failures; log sources; alert integration.
Figures: diagnostic decision tree; layered connectivity stack.

Lab themes (6): report row filtering; dashboard alert prioritisation; layered
connectivity evaluation; log classification; MTTR metrics; alert rule
matching.

## Module 10 — Capstone (`10_capstone`)
Teach: full scenario with two sites and three platforms; build plan;
enrollment waves; policy and patch rollout; incident; evidence pack.

Lab themes (6): readiness checklist validation; enrollment wave planning;
rollout gate evaluation; compliance evidence summary; incident root-cause
selection; final scorecard.

---

## Module 11 — Server and agent upgrades (`11_upgrade`)
Teach: routine upgrade cadence; server-first order; Admin → Update Servers
(select servers, pick release, schedule ASAP or datetime, states Pending →
In Progress → Success/Error, brief console disconnect); Docker caveat (console
feature does not work; `docker compose pull` +
`docker compose --profile openuem up --force-recreate -d --build`); Admin →
Update Agents (console checks every 6 hours and at service start, bulk select,
release, schedule, Pending/error/success, rollback by selecting the previous
release, dashboard outdated vs upgradable counts); pre/post checklists.
Figures: upgrade path decision; console-driven agent upgrade sequence.

Lab themes (6): outdated/upgradable classification; upgrade path selection;
maintenance-window eligibility; task state validation; rollback target;
post-upgrade checklist.

## Module 12 — RustDesk remote desktop (`12_rustdesk`)
Teach: remote assistance paths (VNC for Windows and Linux X11, RDP for
Linux Wayland/Gnome, RustDesk for Windows/Linux/macOS); hbbs ID server, hbbr
relay, `id_ed25519.pub`; Docker deployment (`oss.yml`, or `docker run` with
`--net=host` and `-v ./data:/root`); ports 21115 TCP, 21116 TCP+UDP, 21117 TCP,
21118/21119 web (keep closed), 21114 Pro web console; UFW rules; Windows MSI,
Linux `.deb`, macOS `.dmg` plus Screen Recording/Accessibility; client Network
settings (ID server required, key required, relay optional, API for Pro);
OpenUEM 0.10.0+ org RustDesk tab (relay, ID server, public key, permanent
password → random per session).
Figures: connection path; console-initiated session sequence.

Lab themes (6): mandatory port check; base64 key validation; client config
completeness; direct/relay/blocked routing; org settings readiness; OS
permission checklist.

**English edition:** every module also ships `README.en.md`,
`explanation.en.md`, `exercise.en.md` and `solution.en.md` — faithful
translations with identical code, tables and fixtures. `lab.py` is shared.

## Acceptance gate (run before you answer)
```
python3 modules/NN_slug/lab.py
python3 scripts/verify_course_build.py --repo . --modules NN --min-chars 5000 --exercises 6 --runs 3
```
Both must pass. Do not claim PASS without running them.
