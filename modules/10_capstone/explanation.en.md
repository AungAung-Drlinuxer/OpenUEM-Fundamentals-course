# Module 10 — The Whole Story: Deploying OpenUEM for One Organization

## 10.1 Scenario setting

This module has no new topic. It is the combination, as one organizational work
plan, of skills learned separately in the previous eight modules. When the
learner finishes this module, memorizing each console button is not required.
What is required is the ability to break a plan into stages, to know which
evidence each stage needs, and to draw a conclusion from the data at hand when
a problem occurs.

The organization in the scenario is `openuem.example`. The head office is in
Yangon and the branch is in Mandalay. Both are managed by a single OpenUEM
instance. The branch has no separate server. Branch endpoints connect to the
head office server over the WAN.

| Item | Value |
|---|---|
| Default organization | `openuem.example` |
| Head office | Yangon — 18 endpoints (Windows 10, Linux 5, macOS 3) |
| Branch | Mandalay — 9 endpoints (Windows 5, Linux 3, macOS 1) |
| Total | 27 endpoints, three platforms |
| Server | one Linux host, PostgreSQL and compose stack |
| Console URL | `console.openuem.example` (through the Caddy reverse proxy) |
| Staff roles | 2 server administrators, 1 helpdesk operator, 1 change approver |
| Maintenance window | Saturday 01:00–05:00 (UTC+06:30) |

The role separation follows the least privilege principle of module 06. Only the
two server administrators can change the certificate and component settings.
The helpdesk operator can perform force report and package deployment on
individual endpoints, but cannot create a profile. The change approver
participates only at the step where the deployment plan is approved.

Three constraints are set at the start of the scenario. The first is that the
branch has no DNS server. Branch hosts therefore use a hosts override. The
second is that the maintenance window exists only once per month. The third is
that branch endpoints are registered with DNS and their own IP, so remote
assistance, file browsing and WOL cannot be used. This constraint is the same as
the remote endpoint limitation described in module 07.

## 10.2 What the earlier modules contribute

In the capstone, each stage uses the output of one earlier module as the input
of the next. The following table shows which stage descends from which module.

| Module | What is brought in | How it appears in the capstone |
|---|---|---|
| 01 | component map, lifecycle, port plan | deciding which service owns which port |
| 02 | PostgreSQL, database role, compose, `.env` | build stages P0 and P1 |
| 03 | certificate, `openuem.ini`, service order | build stage P2 and incident recovery |
| 04 | agent install per platform, log locations | the work of each enrollment wave |
| 05 | agent state, admission, org/site/tag | the wave plan and tag-based filtering |
| 06 | inventory, package deployment, profile | delivering the software baseline |
| 07 | patch pipeline, maintenance window, compliance metrics | the gate and measurement of the single patch wave |
| 08 | reports, dashboard, layered diagnosis, logs | incident diagnosis and the evidence pack |

What this table shows is clear. If one earlier module is not mastered, the
capstone will stall at the corresponding stage. For example, without knowing how
to compute certificate validity, it is not possible to identify which item in
the readiness checklist is a blocker. That item is directly connected to the
root of the later incident.

## 10.3 Build plan

The build is divided into six stages. The next stage is entered only when the
current stage is complete.

| Stage | Goal | How completion is known |
|---|---|---|
| P0 | PostgreSQL and database role ready | connection from `psql` can be verified |
| P1 | compose stack running | all components healthy |
| P2 | CA and component certificates | all files present in the certificate tree |
| P3 | console and authentication | `console.openuem.example:1323` can be reached |
| P4 | three enrollment waves | all 27 endpoints Enabled |
| P5 | baseline and patch wave | profile state and patch progress measurable |

In the first stage the database is built directly on the server host. The
database must exist before the containers start.

```bash
sudo apt install -y postgresql
sudo systemctl enable --now postgresql
sudo -u postgres psql
```

The first command installs the PostgreSQL package. The second command starts the
service now and also sets it to start automatically at boot. The third command
enters the SQL shell as the `postgres` user.

```sql
CREATE DATABASE openuem;
CREATE USER openuem_app WITH ENCRYPTED PASSWORD 'change-me';
GRANT ALL PRIVILEGES ON DATABASE openuem TO openuem_app;
ALTER DATABASE openuem OWNER TO openuem_app;
```

The first command creates the base database of OpenUEM. The second command
creates a separate role for the application. The `postgres` superuser must not
be used directly by the application. The third and fourth commands make that
role the owner of the database. Without ownership, a permission error can occur
at the table creation stage.

The connection URI is placed in the `.env` file. If the password contains a
special character such as `=`, percent-encoding is required. For example, `te=st`
is written as `te%3Dst`. If this rule is not followed, an authentication failure
occurs while the components start.

In the second stage the compose deployment is used.

```bash
git clone https://github.com/open-uem/openuem-docker
cd openuem-docker
cp .env-example .env
docker compose up -d
```

The first command fetches the official compose repository. The second command
enters that folder. The third command copies the sample file to `.env`. The file
name must have a leading dot. The fourth command starts the containers in the
background. Podman users can substitute `podman compose`.

The keys that must be filled in `.env` are as follows.

| Key | Example value | Purpose |
|---|---|---|
| `OPENUEM_ORGNAME` | `openuem.example` | default organization name |
| `OPENUEM_COUNTRY` | `MM` | country included in the CA certificate |
| `OPENUEM_DOMAIN` | `openuem.example` | base domain of the components |
| `OPENUEM_DATABASE_URL` | `postgres://openuem_app:***@192.168.1.43:5432/openuem` | URI used by the components |
| `CONSOLE_HOST` | `console.openuem.example` | host name of the console |
| `CONSOLE_PORT` | `1323` | console port |
| `CONSOLE_AUTH_PORT` | `1324` | authentication port |
| `CONSOLE_JWT_KEY` | random 32-character string | session token signing |
| `NATS_HOST`, `NATS_PORT` | `nats.openuem.example`, `4433` | broker the agents connect to |
| `OCSP_URL`, `OCSP_PORT` | `http://ocsp.openuem.example:8000`, `8000` | where certificate revocation is checked |
| `REVERSE_PROXY_*` | Caddy host and port | left empty when no reverse proxy is used |

The hosts override is added on the branch hosts.

```text
192.168.1.43  nats.openuem.example  ocsp.openuem.example  console.openuem.example
```

The LAN IP must be used here. `localhost` or `127.0.0.1` must not be used. Each
container would resolve that name as itself, so the connection would fail.

In the third stage the CA and the component certificates are created.
`openuem-cert-manager` is the command line tool that issues the CA and the
certificates from one place.

```bash
sudo openuem-cert-manager client-cert --name "OpenUEM Agent" --dst ./agents \
  --type="agent" --org "$ORGNAME" --country "$COUNTRY" --province "$ORGPROVINCE" \
  --locality "$ORGLOCALITY" --address "$ORGADDRESS" --years-valid 2 \
  --filename "agent" --ocsp "http://$OCSP_SERVER:$OCSP_PORT" \
  --description "Agent certificate" --cacert ./ca/ca.cer --cakey ./ca/ca.key \
  --dburl "$DATABASE_URL"
```

This command issues one certificate of type agent into the `agents` folder.
`--years-valid 2` sets a validity of two years. `--ocsp` is the OCSP URL that is
embedded in the certificate. `--cacert` and `--cakey` are the CA used for
signing. Pointing at the wrong CA here becomes the cause of the later incident.

**Figure 1 — Build stages: from an empty host to managed endpoints**

```mermaid
flowchart LR
    P0["P0 PostgreSQL and role"] --> P1["P1 compose stack"]
    P1 --> P2["P2 CA and certificates"]
    P2 --> P3["P3 console access"]
    P3 --> P4["P4 three agent waves"]
    P4 --> P5["P5 baseline and patch"]
    P5 --> P6["P6 evidence pack"]
```

Figure walkthrough — this figure arranges the six stages from left to right. In
P0 the database and the application role are built first. If the components
start without a database, they stop immediately. In P1 all containers are made
to run. In P2 the CA and the component certificates are issued. Agents must not
be deployed before this stage is finished. In P3 the console is reached from a
browser and login is tested. In P4 the agents are deployed in order across three
waves. In P5 the software baseline and the patch wave are performed. In P6 the
results are exported and stored as evidence. Each arrow means "continue only
when the previous stage is complete".

## 10.4 Acceptance criteria

Eight measurable criteria are set for deciding that the deployment is "done".
Each criterion includes how it is measured.

| ID | Criterion | How it is measured |
|---|---|---|
| AC-1 | database and stack ready | connection from `psql` works, all containers healthy |
| AC-2 | CA validity above 365 days at go-live | certificate file validity computation |
| AC-3 | all 27 endpoints Enabled | the console agent list |
| AC-4 | reporting above 90% for 7 consecutive days | the 24-hour slot on the dashboard |
| AC-5 | baseline coverage above 85% | software view CSV |
| AC-6 | compliance above 95% after the patch wave | security view CSV |
| AC-7 | evidence pack stored | all files present in the archive |
| AC-8 | incident record closed and runbook amended | the review record |

The criteria are not for decoration. They are used to measure deployment
progress. For example, if AC-2 is checked in advance in the readiness checklist,
the CA is found to have only 120 days left. That single item stops the build. In
this scenario the team correctly identified that blocker, but performed the
remediation quickly without a change record. That decision is directly connected
to the later incident.

## 10.5 Enrollment wave plan

The 27 endpoints are not deployed at once. They are split into three waves. The
first wave is a pilot and contains one endpoint per platform.

| Wave | Scope | Count | Purpose |
|---|---|---|---|
| 1 | head office pilot (one per platform) | 3 | test the install method and the certificate |
| 2 | remaining head office endpoints | 15 | bulk deployment inside the LAN |
| 3 | branch endpoints | 9 | deployment under WAN constraints |

Three days are left between one wave and the next. After the first wave, a force
report confirms that the full inventory has arrived. After the second wave, the
network usage of the head office endpoints is watched for one day. The third
wave starts in the evening so that it does not collide with peak WAN usage.

The Windows agent is deployed with a silent install.

```text
openuem-agent-setup.exe /VERYSILENT /cacert=ca.cer /cert=agent.cer /key=agent.key \
  /server=nats.openuem.example:4433 /sftp=2022 /vnc=1443 /tenantid=1 /siteid=2
```

In this command `/VERYSILENT` installs without showing a window. `/cacert`,
`/cert` and `/key` give the locations of the three certificate files. `/server`
is the NATS host and port. `/sftp` and `/vnc` are the ports of the two
agent-side services. `/tenantid` and `/siteid` must be supplied together. If
only one is given, the install does not accept it.

On Debian-based hosts the agent is installed from the package.

```bash
sudo apt install openuem-agent
sudo systemctl restart openuem-agent
sudo systemctl restart openuem-agent-updater
```

The first command installs the agent package and asks questions for the NATS
server, the SFTP port and the VNC proxy port. The second and third commands
restart the two services after the certificates are placed. The certificates are
kept under `/etc/openuem-agent/certificates` with the names `ca.cer`, `sftp.cer`,
`agent.cer` and `agent.key`.

On RPM-based hosts `dnf install -y openuem-agent` is used and
`/etc/openuem-agent/openuem.ini` is edited directly. That file contains
`[NATS] NATSServers=` and the ports. The folder ownership is then changed to the
`openuem-agent` user. For the macOS agent the official installer is used. The
installer name and its flags can change with the version, so it must be
rechecked against the current documentation.

**Figure 2 — The sequential work of each wave**

```mermaid
sequenceDiagram
    participant ADMIN as Administrator
    participant CONSOLE as OpenUEM console
    participant W1 as Wave 1 pilot
    participant W2 as Wave 2 head office
    participant W3 as Wave 3 branch
    ADMIN->>CONSOLE: approve wave 1
    CONSOLE->>W1: agent install and admission
    W1-->>CONSOLE: report within 60 minutes
    ADMIN->>CONSOLE: check results over 3 days
    ADMIN->>CONSOLE: approve wave 2
    CONSOLE->>W2: agent install and admission
    W2-->>CONSOLE: report and inventory
    ADMIN->>CONSOLE: approve wave 3
    CONSOLE->>W3: install over the WAN
    W3-->>CONSOLE: report and inventory
```

Figure walkthrough — this figure has five participants. The leftmost is the
administrator. That participant signals to the console that a wave is approved.
The console sends the agent install and admission to the relevant wave group.
The wave group sends a report back. The order of each arrow matters. Wave 2 must
not start until the pilot is finished and its results have been checked for
three days. Wave 3 starts only when wave 2 is complete. This order limits the
impact of a problem to a single wave. The branch wave includes WAN latency, so
reports can take longer to arrive.

Inside each wave the endpoints are grouped by tag. Tags such as
`site=head-office`, `site=branch` and `platform=windows` simplify filtering and
report export. Tag names must not change during the scenario. If they change,
comparison with earlier reports breaks.

## 10.6 Software baseline and profile

The baseline is "the list of packages every endpoint must have". Because the
package manager differs by platform, the list is split into three.

| Platform | Package manager | Baseline items | Profile task type |
|---|---|---|---|
| Windows | WinGet | browser, archive tool, media player | WinGet configuration (DSC) |
| Linux | Flatpak | browser, media player | Ansible |
| macOS | HomeBrew | browser, media player | Ansible |

A profile is a desired state. Each task states "bring the endpoint to this
state". The agent checks for a new profile every 30 minutes. Therefore the
result is not expected immediately after a profile is published. If an endpoint
is offline, it accepts the task when it returns. Package requests queue in NATS.

Two preparations are required. On Windows, Microsoft Store and App Installer
must be updated to use WinGet. On macOS, HomeBrew must be installed by hand. If
the profile is deployed without those two preparations, the tasks fail. That
failure is found in the agent log.

After the baseline is deployed, a CSV is exported from the software view. That
file aggregates package name, publisher and install count. In this scenario 24
of the 27 endpoints are compliant. The remaining three are `LNX-BR-02` (the
Flatpak package is missing), `MAC-HO-03` (one update pending) and `WIN-BR-04`
(the user removed the package). As a percentage this is 88.9 percent.

## 10.7 Patch wave and maintenance window

The patch wave is performed only between 01:00 and 05:00 on Saturday. This time
slot is the same for both the head office and the branch. Four gates must be
passed before the wave starts.

| Gate | Requirement | Action when unmet |
|---|---|---|
| G1 | current time inside the window | move to the next window |
| G2 | reporting above 90% | find the silent endpoints |
| G3 | zero validation failures | remove the failing host and recheck |
| G4 | no open P1 incident | close the incident first |

**Figure 3 — Gate decisions for the patch wave**

```mermaid
flowchart TD
    S["Wave start 01:00"] --> W{"Inside the window?"}
    W -- "no" --> H1["HOLD: move to the next window"]
    W -- "yes" --> R{"Reporting above 90%?"}
    R -- "no" --> H2["HOLD: find the silent endpoints"]
    R -- "yes" --> V{"Zero validation failures?"}
    V -- "no" --> H3["HOLD: remove the host and recheck"]
    V -- "yes" --> P{"Open P1 incident?"}
    P -- "yes" --> H4["HOLD: close the incident first"]
    P -- "no" --> G["GO: deploy and verify"]
```

Figure walkthrough — this figure flows from top to bottom. The first check is
time. If it is not the window, the path goes left and stops. If it is inside the
window, the reporting percentage is checked. If it is below 90%, the silent
endpoints must be found first. If it is sufficient, the validation result is
checked. If there is one failure, that host is removed from the wave and
rechecked. Only then is the question asked whether an open P1 incident exists.
Only when all four pass does the path reach the rightmost green branch. This
order means "if one fails, all stop". There is no half-deployed state in the
middle.

In the first measurement the reporting was 24/27 and there was one validation
failure. The gate decided HOLD. There were two causes. The team removed
`LNX-HO-04` from the wave and rechecked the other three endpoints with a force
report. At 02:40 a second measurement gave 27/27 and zero failures, so GO was
granted. That wave started at 03:10 and finished at 04:35. Measuring again at
06:15 produced HOLD because it was outside the window. This shows that the gate
always includes the time in its check.

## 10.8 Incident: agents stall after a certificate change

Four hours after the patch wave finished, at 09:05, one group of agent
certificates was replaced. At 09:20 the red section of the dashboard raised an
alert. Only 4 of the 27 endpoints were still reporting.

| Time | Event |
|---|---|
| 09:05 | 23 agent certificates replaced |
| 09:20 | reporting drops to 4/27, the dashboard alerts |
| 09:35 | layered diagnosis begins |
| 09:50 | unknown authority found in the agent log |
| 10:15 | root cause confirmed |
| 10:40 | recovery begins |
| 11:40 | reporting returns to 27/27 |

The layered diagnosis follows the method of module 09. It climbs from the
bottom layer upward.

| Item | Finding | Cause it excludes |
|---|---|---|
| `console.openuem.example:1323` | HTTP 200 | the console and database are working |
| port 4433 | TCP connection succeeds | the NATS service is not down |
| OCSP responder 8000 | HTTP 200 | the OCSP service is not down |
| PostgreSQL | connection accepted | the database is not broken |
| DNS resolution | succeeds | it is not a name resolution problem |
| clock skew | 3 seconds | it is not a time difference |
| agent log | `x509: certificate signed by unknown authority` | the certificate chain does not match |

The agent log is the main piece of evidence. That string says "the server does
not know who signed the agent's certificate". Two related facts make this
conclusion firm. First, the 4 endpoints whose certificates were not replaced
(three pilots and one extra) continue to report normally. Second, all 23 that
were replaced are silent. This pattern points at a certificate problem, not at
an infrastructure problem.

The root cause is that. During the replacement, `openuem-cert-manager` was
called with a newly created CA. However, `CACert` in `openuem.ini` and the OCSP
responder still trusted the old CA. The new agent certificate was therefore not
accepted by NATS. When the agent sent its report, the TLS handshake failed.

Recovery is performed in order.

1. Freeze the certificate replacement batch.
2. Restore the previous CA in `openuem.ini` and in the certificate tree.
3. Re-issue the agent certificates from the trusted CA.
4. Start `openuem-ocsp-responder`.
5. Start `openuem-nats-service`.
6. Start `openuem-server-updater`.
7. Start `openuem-agent-worker`.
8. Start `openuem-notification-worker`.
9. Start `openuem-cert-manager-worker`.
10. Start `openuem-console`.
11. Perform a force report on the affected endpoints.
12. Confirm that reporting has returned to 27/27.

The service order is the order defined in module 03. OCSP starts first. Then
NATS, the updater, the workers, and finally the console. If the order is wrong,
the workers cannot obtain the certificate and fail again.

Two lessons come from this incident. First, finding the CA validity blocker in
the readiness checklist was correct. However, the remediation was performed
without a change record. Second, a certificate replacement must be tested on one
endpoint first, and the rest of the batch performed only when the result is
good. Replacing everything at once costs a great deal of recovery time.

## 10.9 Evidence pack

In the review, saying "it was done" is not enough. Files that can demonstrate
the state of the deployment are required. The following files are collected and
stored in one place.

| ID | Evidence | Source | What it proves |
|---|---|---|---|
| E1 | dashboard screenshot | console dashboard | reporting, platform mix |
| E2 | agent list CSV | console agent view | state and last report time |
| E3 | inventory overview PDF | per endpoint | hardware and OS facts |
| E4 | software CSV | software view | baseline coverage |
| E5 | security CSV | security view | patch state |
| E6 | profile list | console profile view | desired state definitions |
| E7 | wave record | external document | which endpoint at which time |
| E8 | incident timeline | incident record | diagnosis and recovery |
| E9 | `lab.py` output | lab run | the results of all computations |
| E10 | verifier output | repo verifier | the structural correctness of the module |

E1 and E2 are exported on the day the deployment finishes. E4 and E5 are
exported twice, before and after the patch wave, and compared. When a CSV is
exported, the filter and the sort must not be cleared. The report comes out
according to the current filter. That fact makes the comparison accurate.

The evidence files are stored in a folder that carries a date. The file name must
include the date and the stage. For example, 2026-03-14_wave1_agents.csv. If
files are stored without a name, the review cannot tell which file belongs to
which stage.

## 10.10 Review discussion

The review is set at 45 minutes. There are five parts. 10 minutes for presenting
results, 15 minutes for incident analysis, 10 minutes for evidence checking,
5 minutes for identifying gaps, and 5 minutes for setting the next step.

Questions to discuss:

- Can the number of the 27 endpoints that are reporting be found in the
  evidence files?
- With what plan will the three endpoints that do not meet the baseline be
  fixed?
- Was the first gate of the patch wave correct to return HOLD? How much time
  did that decision cost?
- If the certificate replacement had been tested on one endpoint first, could
  the incident have happened?
- If an incident happens again, which piece of data will be looked at first?
- If this deployment is extended to another site, which stages must be
  repeated?

A good answer always pairs a number with a file. General statements such as
"everything is fine" are not evidence.

## 10.11 Self-check

**1. If the CA validity fails in the readiness checklist, what must be done?**
Do not start the build. Issue a new CA, re-issue all component certificates, and
record it in a change record.

**2. What do the counts of the three waves show?**
The three pilots test the install method. The 15 head office endpoints
demonstrate bulk deployment inside the LAN. The 9 branch endpoints demonstrate
deployment under WAN constraints. The impact is confined to a single wave.

**3. If the gate shows HOLD, is the wave cancelled entirely?**
No. HOLD means "do not do it now". The cause can be removed and the measurement
repeated inside the window. If the window has been left, it moves to the next
window.

**4. In the certificate incident, why is OCSP checked first?**
If the OCSP responder is down, the agent's certificate check fails. Isolating
the state of a single service while the other layers are correct reduces the
number of candidate causes.

**5. How many files are needed in the evidence pack?**
The count is not the point. There must be at least one piece of evidence for each
acceptance criterion. In this scenario ten files are defined.

## 10.12 Operational cautions

- Do not use `localhost` in `.env`. Each container would resolve that name as
  itself.
- The agent must have an outbound connection to the NATS host and port. If the
  firewall blocks that path, the agent stays in the Waiting for admission state.
- The "24 hours" slot on the dashboard shows a rolling period. To distinguish a
  gap in report times, look directly at the last report time in the agent list.
- Changing `CONSOLE_JWT_KEY` breaks all current sessions. Change it only inside
  the maintenance window.
- Changing the certificate and the CA is a change. Test on one endpoint first,
  then perform the rest of the batch.
- Evidence files must be exported before teardown. If the stack is deleted and a
  report is then attempted, the data is no longer there.
- On remote endpoints such as the branch, remote assistance, file browsing and
  WOL cannot be used. Another method must be defined for those tasks.
- Console menu names and dashboard card names can change with the version.
  Record the version in the runbook.

## Technical review notes

- Correction: the first draft wrote the wave counts as 4/14/9. Because the pilot
  is defined as one per platform, it must be 3. Both the current text and
  `lab.py` have been aligned at 3/15/9.
- Correction: the reporting requirement in the patch gate was changed from 85%
  to 90%. The first measurement of 24/27 is 88.9%, so under that requirement two
  failures appear.
- Correction: the evidence file list originally had only nine items. The
  verifier output was added as the tenth.
- Needs verification: the exact flags of the macOS agent installer. No command
  is given for it in this document. It must be rechecked against the version.
- Needs verification: the flag set of `openuem-cert-manager` can change with the
  version. This document copies the example from the documentation as it stands.
- Needs verification: the console menu names (dashboard card, profile view) can
  differ with the version. This document uses generic names.
- All numbers (27 endpoints, waves 3/15/9, compliance 24/27, 23 certificates,
  scorecard 85.5) are teaching examples. They are not measured results.
