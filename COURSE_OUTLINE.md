# COURSE_OUTLINE — OpenUEM Endpoint Management Fundamentals

Source outline supplied by the learner (7 sections) plus an explicit request:
cover PostgreSQL setup and **Ubuntu 24.04 native installation** as well as the
Docker/Podman deployment. The material is therefore split into ten modules so
each installation path gets its own lab and no module carries two jobs.

| Module | Folder | အကြောင်းအရာ |
|---|---|---|
| 01 | `01_introduction` | Introduction to OpenUEM — endpoint management, components, lifecycle, lab planning |
| 02 | `02_postgresql` | PostgreSQL preparation — install, role/database, `pg_hba`, URI encoding, backup |
| 03 | `03_ubuntu_server` | Installing OpenUEM on Ubuntu 24.04 Server — packages, certificates, `openuem.ini`, services |
| 04 | `04_docker_compose` | Docker/Podman deployment — `openuem-docker`, `.env`, name resolution, verification |
| 05 | `05_agent_deployment` | Agents for Windows, macOS and Linux — certificates, ports, logs |
| 06 | `06_enrollment_organization` | Enrollment — admission, organizations, sites, tags, users and roles |
| 07 | `07_device_management` | Device management — inventory, packages, profiles, remote assistance |
| 08 | `08_patch_automation` | Patch management and automation — visibility, windows, validation, compliance |
| 09 | `09_reporting_troubleshooting` | Reporting, dashboard alerts and layered troubleshooting |
| 10 | `10_capstone` | Capstone lab — two sites, three platforms, incident and review |

## Lesson-level mapping

### Module 01 — Introduction to OpenUEM
1. What endpoint management is and which problems it solves
2. Self-hosted versus SaaS endpoint management
3. OpenUEM component map (console, NATS, workers, OCSP, cert-manager, PostgreSQL)
4. Endpoint lifecycle: install → report → admission → enabled → maintenance
5. Capability inventory (inventory, software, security, remote assistance, WOL)
6. Planning a lab: DNS names, ports, accounts, time budget

### Module 02 — PostgreSQL preparation
1. Why the database exists before the application
2. Installing PostgreSQL on Ubuntu 24.04 and on RPM hosts
3. Creating the database and a dedicated role with `psql`
4. Connection URI format and percent-encoding rules
5. `pg_hba.conf` authentication method and restart discipline
6. Verifying connectivity before the OpenUEM installer runs
7. Backup, restore and clean reinstall (`DROP TABLE ... CASCADE`)
8. Operational cautions: passwords, locale, disk, connections

### Module 03 — Installing OpenUEM on Ubuntu 24.04 Server
1. Prerequisites and the DNS name the console certificate must carry
2. Adding the OpenUEM apt repository and installing server packages
3. Package-to-role map (console, NATS, workers, OCSP, updater, cert-manager)
4. Creating the certificate tree and component certificates
5. Writing `/etc/openuem-server/openuem.ini`
6. Starting services in the documented order and verifying health
7. Reverse proxy with Caddy or nginx and console ports
8. Hardening: `openuem` user, key permissions, backups, JWT key
9. First login and the initial administrator account

### Module 04 — Docker/Podman deployment
1. When containers are the better fit and what changes operationally
2. Cloning `openuem-docker` and creating `.env`
3. Required environment variables (database, domains, NATS, console, JWT)
4. Starting the stack and verifying containers
5. Name resolution in a lab without DNS (hosts overrides)
6. Reverse proxy variables and Caddy
7. Volumes, upgrades and teardown
8. Comparing native and container deployments side by side

### Module 05 — Agent deployment
1. What an agent does and how it reaches the server
2. Certificates required by every agent
3. Windows silent install flags and wizard install
4. Debian/Ubuntu install and post-install certificate placement
5. RPM-based agent install and `openuem.ini`
6. macOS agent install
7. Ports (NATS 4433, SFTP 2022, VNC proxy 1443) and firewall rules
8. Agent log locations and first-response triage

### Module 06 — Enrollment and organization
1. Agent states: waiting for admission, enabled, disabled
2. Admission workflow and automatic admission setting
3. Report frequency and force report
4. Organizations and sites (multi-tenancy)
5. Tags, metadata and notes
6. Users, certificate login, OpenID Connect and approval states
7. Role separation and least privilege for administrators
8. CSV bulk import for organizations and users

### Module 07 — Device management basics
1. Inventory views and what each tab answers
2. Package deployment with WinGet, Flatpak and HomeBrew
3. Uninstall requests and pending deliveries
4. Profiles as desired state: task types per platform
5. Profile scheduling, verification and failure signals
6. Remote assistance, SFTP browsing and WOL
7. Health indicators: last report, disk, antivirus, updates

### Module 08 — Patch management and automation
1. Windows update inventory and history
2. Linux pending security updates
3. Patch workflow: detect → stage → deploy → verify
4. Scheduling and maintenance windows
5. Validation matrix and rollback thinking
6. Automating routine work with profiles and tasks
7. Compliance metrics and reporting cadence

### Module 09 — Reporting and troubleshooting
1. Report generation (PDF/CSV) and filter preservation
2. Dashboard sections and alert triage
3. Component health checks (console, NATS, workers, OCSP, database)
4. Layer-by-layer connectivity diagnosis
5. Common failures: certificates, DNS, ports, clock skew, database
6. Log sources and what to read first
7. Integrating alerts with external monitoring

### Module 10 — Capstone
1. Scenario brief: two sites, three platforms, mixed roles
2. Build plan and acceptance criteria
3. Enrollment wave plan
4. Policy and patch rollout
5. Incident simulation and recovery
6. Evidence pack and review discussion

## Conventions
- One folder per module, exactly five files.
- Each module: 6 exercises, one deterministic stdlib lab, solutions that match
  real lab output.
- Formal Burmese prose, English technical terms, no colloquial particles.
