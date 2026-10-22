# Module 09 — Reporting and Troubleshooting

## A change without evidence is not a change

OpenUEM manages hundreds of endpoints from a single place. At that scale, when a
problem appears, the first thing required is not an answer but evidence. To be
able to say "one agent is not reporting" the last report time is needed. To be
able to say "the update has not arrived yet" the pending update list is needed.
To be able to say "the database is down" component status and logs are needed.

This module links three kinds of tool into one chain.

- **Report** — extracting the current state as a durable file (PDF/CSV). Used to
  present internally and to record monthly.
- **Dashboard** — the daily screen that shows what must be looked at first
  today.
- **Logs and layered checks** — the path that finds the real cause of a fault.

Mixing these three produces the two mistakes that occur most often. The first
mistake is using the dashboard as a long-term record — the dashboard refreshes
every five minutes and shows a state that has already passed. The second
mistake is restarting a component without reading the log — a restart removes
the symptom, it does not remove the cause.

## The four views a report can be taken from

In the OpenUEM console, PDF and CSV reports can be exported from the agents,
computers, security and software views. Each view answers one kind of question.
Choosing the right view is therefore the first step in the quality of a report.

| View | What it contains | The question it answers | Suitable format |
|---|---|---|---|
| Agents | agent state, last report time, platform | who is not reporting, who is stuck waiting | daily CSV |
| Computers | hardware, operating system, disk, network adapter | which machine has which OS version | monthly PDF |
| Security | antivirus status, update configuration, pending updates, update history | how much compliance there is | PDF for audit |
| Software | software aggregated by name, publisher, install count | which app, which version, on how many machines | CSV for analysis |

The security view is the primary evidence for patch compliance. That view
contains antivirus enabled/updated status, the download and install
configuration of Windows updates, pending updates and update history. For Linux
endpoints, pending security updates are shown in that view. The software view is
aggregated by install count, so it answers the question "which app is installed
on how many machines" directly.

## Preserving the filter as part of the report

The value of a report is not in the number of rows. In the sentence "seven
machines showing antivirus disabled in the security view", the part that matters
is the filter. OpenUEM's PDF/CSV export preserves the current filter and sort.
That means the rows visible on the screen are the rows that appear in the file.

A procedure that works by relying on that property —

1. Write the question as one sentence (for example — "Windows machines in the
   Yangon site that have not reported within the last 24 hours").
2. Choose the view that matches that question.
3. Set the filters one at a time and watch how the row count changes. If the
   rows do not decrease, the filter has no effect.
4. Record the row count. That number must match the heading of the file.
5. Set the sort — so that the rows with problems reach the top.
6. Export as PDF or CSV.
7. Put the view, the meaning of the filter and the date into the file name
   (for example — `security_antivirus-disabled_yangon_2026-03-02.pdf`).

Step 7 is not a trivial matter. When a file is opened again a few weeks later
and the filter conditions are not known, that file loses value as evidence. The
CSV file must not be assumed to contain the filter definition itself — only the
rows it contains are guaranteed.

```mermaid
flowchart LR
    A["Choose the view — agents / computers / security / software"] --> B["Set the filters one at a time"]
    B --> C["Set the sort"]
    C --> D["Record the row count"]
    D --> E["PDF export"]
    D --> F["CSV export"]
    E --> G["Sign and store, or send"]
    F --> H["Analyse with a spreadsheet or BI"]
```

**Figure 1 — The path by which a report is produced**

Figure walkthrough — Reading Figure 1 starts at the left edge, at "Choose the
view". In the first box you choose the view that matches the question. In the
second box you add the filters one at a time. In the third box you set the sort.
In the fourth box you record the remaining row count — this step is the
foundation for later verification. After that the path splits into two. The
upper path is PDF, for signing and storing or for sending. The lower path is
CSV, for numerical analysis with a spreadsheet or a BI tool. Both paths rest on
the same filter and the same sort.

## Dashboard — the screen that changes on a five-minute cadence

The dashboard answers a single question — "what must be done first now?". That
is why the dashboard is divided by three colours.

| Section | What it contains | Meaning | Response |
|---|---|---|---|
| Red | agents not reporting, pending updates, disabled antivirus, agent/app updates | the work that must actually be done today | within a single day |
| Green | user count, app count, tag count | the scale of management | review weekly |
| Blue | component status such as console, NATS, workers, OCSP | baseline system health | immediately |

The red section has the highest value. The four items contained in that section
must not be given equal weight. An agent that is not reporting is usually a
connectivity or certificate problem, and every other piece of information on
that agent is out of date. So "those not reporting" is ordered first, "disabled
antivirus" second, "pending updates" third, and "agent/app updates" fourth.

The dashboard refreshes once every five minutes by default. That cadence has two
meanings. First — the numbers displayed can be up to five minutes behind.
Second — after a change, do not expect the result immediately. The conclusion
"it has not changed" may be drawn only after waiting at least one refresh cycle.

```mermaid
flowchart TD
    A["Look at the dashboard every five minutes"] --> B{"Is there a fault in the blue section?"}
    B -- "yes" --> C["Resolve component health first"]
    B -- "no" --> D{"Is anyone not reporting in the red section?"}
    D -- "yes" --> E["Check the certificate and NATS connectivity"]
    D -- "no" --> F{"Is any antivirus disabled?"}
    F -- "yes" --> G["Check from the security view"]
    F -- "no" --> H["Roll out pending updates in a planned way"]
    C --> I["Record the change"]
    E --> I
    G --> I
    H --> I
    I --> J["Wait one refresh cycle and re-check"]
```

**Figure 2 — The path by which the dashboard decides priority**

Figure walkthrough — Figure 2 is read from top to bottom. The first box is
looking at the dashboard once every five minutes. After that three questions are
asked in sequence. The first question is "is there a fault in the blue section".
If there is, component health is resolved first — because if a component is
down, the dashboard itself is no longer correct. If the blue section is clean,
you descend to the second question. It asks "is anyone not reporting". If there
is, the certificate and NATS connectivity are checked. If not, you descend to
the third question. It asks "is any antivirus disabled", and if there is, you
enter the security view. If not, pending updates are rolled out in a planned
way. Every path converges on the last two boxes — recording the change and
waiting one refresh cycle before re-checking.

## Component health — which component does what

When hunting a fault, the responsibility of each component must be known. Each
OpenUEM component performs its duty on one specific port.

| Component | Port | Responsibility | Symptom when it goes down |
|---|---|---|---|
| `openuem-console` | 1323 (console), 1324 (auth) | web console and authentication server | the browser does not open, login fails |
| `openuem-nats-service` | 4433 | the broker agents connect to | every agent stops reporting, the dashboard breaks |
| `openuem-agent-worker` | — | accepts agent reports and writes them to PostgreSQL | the report arrives but the data does not appear |
| `openuem-cert-manager-worker` | — | issues agent/user certificates | no certificate after admission |
| `openuem-notification-worker` | — | sends outgoing notifications (SMTP) | the invitation mail does not arrive |
| `openuem-ocsp-responder` | 8000 | checks certificate revocation | TLS checks are slow or fail |
| PostgreSQL | 5432 | all persistent data | the console opens but the data does not appear |

The commands to check (systemd based installation) —

```bash
# check the service status of each component
sudo systemctl status openuem-nats-service
sudo systemctl status openuem-agent-worker
sudo systemctl status openuem-console

# restart a component that has gone down
sudo systemctl restart openuem-nats-service
```

If installed with Docker/Podman compose —

```bash
# check the status of all containers
docker compose ps

# read the last lines of a component log
docker compose logs
```

```text
# simulated output — illustrative
NAME                        SERVICE              STATUS
openuem-console             console              Up 3 hours
openuem-nats-service        nats                 Up 3 hours
openuem-agent-worker        agent-worker         Restarting (1) 20 seconds ago
openuem-ocsp-responder      ocsp                 Up 3 hours
postgres                    database             Up 3 hours
```

In that example the worker showing `Restarting` is the cause. The presence of
containers showing `Up` does not mean the system is healthy — without the
worker, agent reports pile up in NATS and the dashboard becomes progressively
more out of date.

To check the database directly —

```bash
# connect to PostgreSQL and check a basic response
psql "postgres://test:***@192.168.1.43:5432/openuem" -c "select 1;"
```

```text
# simulated output — illustrative
 ?column?
----------
        1
(1 row)
```

If the connection does not succeed, the error sits in one of three layers — the
DNS name does not resolve, the route to port 5432 is closed, or the
user/password is wrong. Those three are broken down in the next section.

## Layered checking — confirming one layer at a time

In fault finding, the mistake that occurs most often is checking all the layers
at once. That approach consumes time and still does not isolate a single cause.
The more effective method is to check one layer at a time in sequence and stop
at the first layer that fails.

```text
[ endpoint agent ]
        |
        | 4433 TCP  (agent to NATS, outbound path)
        v
[ openuem-nats-service ]
        |
        | broker → worker consumer
        v
[ openuem-agent-worker ] ---- 5432 ----> [ PostgreSQL ]
        ^                                      ^
        |                                      |
[ openuem-console 1323 / auth 1324 ] ----------+
        |
        | 8000
        v
[ openuem-ocsp-responder ]
```

The order of the check —

| Layer | What is checked | Expectation | Meaning when it does not succeed |
|---|---|---|---|
| 1. Endpoint → NATS | does the agent reach `nats.openuem.example:4433` | a successful connection line in the agent log | certificate, DNS, firewall or NATS down |
| 2. NATS → worker | is there a consumer on the broker | the worker service active | the worker is down or has not started yet |
| 3. Worker → PostgreSQL | can the worker write data | no error in the worker log | database down, wrong credentials |
| 4. Console 1323/1324 | are the console and auth ports open | the browser opens, login succeeds | console down, reverse proxy wrong |
| 5. Console → OCSP 8000 | does certificate checking answer | OCSP returns an answer | OCSP down, certificate expired |

If one layer fails, the lower layers must be recorded as "not tested yet". That
point matters — while layer 1 is failing, the state of layer 4 cannot be called
"good".

```mermaid
flowchart TD
    S["Endpoint agent"] -->|"4433 TCP"| N["openuem-nats-service"]
    N --> W["openuem-agent-worker"]
    W -->|"5432"| P["PostgreSQL"]
    C["openuem-console 1323 / auth 1324"] -->|"5432"| P
    C -->|"8000"| O["openuem-ocsp-responder"]
    A["Agent certificate and ca.cer"] --> S
```

**Figure 3 — The sequence of layered connectivity**

Figure walkthrough — Figure 3 is read from left to right. The leftmost box is the
agent on the endpoint. From that box, the arrow labelled 4433 reaches the NATS
service — this path is the only path that leaves the endpoint outbound. NATS
continues to the worker. The worker writes to PostgreSQL over 5432. The box
below is the console, listening on 1323 and 1324. The console connects to
PostgreSQL over 5432 and continues to OCSP over 8000. The bottom box is the
agent certificate and `ca.cer`, pointing with an arrow into the agent box — if
the certificate is wrong, even the first arrow (4433) cannot succeed.

```mermaid
flowchart TD
    A["A fault is reported"] --> B["Read the agent log"]
    B --> C{"Did the connection to 4433 succeed?"}
    C -- "no" --> D{"Does DNS resolve?"}
    D -- "no" --> E["Fix the DNS / hosts entry"]
    D -- "yes" --> F{"Are all certificate files present?"}
    F -- "no" --> G["Check ca.cer / agent.cer / agent.key"]
    F -- "yes" --> H["Check the firewall and the NATS service"]
    C -- "yes" --> I{"Does the worker write data?"}
    I -- "no" --> J["Check PostgreSQL and the worker log"]
    I -- "yes" --> K["Check the console view and the filter"]
```

**Figure 4 — The decision tree for finding the cause of a fault**

Figure walkthrough — Figure 4 is read from top to bottom. In the first box a
fault is reported. In the second box the agent log is read — this step is never
skipped. The third box asks "did the connection to 4433 succeed". If it did not,
you take the left path and check DNS. If DNS does not resolve, the hosts entry
or the DNS record is fixed. If DNS resolves, you check whether the three
certificate files are present. If they are missing, `ca.cer`, `agent.cer` and
`agent.key` are checked. If they are present, you descend to the firewall and
the state of the NATS service. If the connection succeeded, you reach the right
path, "does the worker write data". If it does not, PostgreSQL and the worker log
are checked. If it does, the problem is no longer on the server and may sit in
the console view or in the filter.

## Eight common faults

| Symptom | Possible cause | The first thing to check |
|---|---|---|
| the agent never appears at all | wrong certificate path | whether the files exist inside `/etc/openuem-agent/certificates` |
| `ca.cer` is missing | the CA certificate was not copied | copy the `ca.cer` produced by the CA into the agent file location |
| the agent does not see the server | wrong `NATSServers` host/port | the `[NATS]` section of `openuem.ini` |
| the name cannot be resolved | no DNS record | the hosts entry or DNS |
| the connection times out | the firewall has the port closed | whether 4433 is open outbound |
| the TLS check fails | the clocks disagree (clock skew) | the time on the server and on the endpoint |
| the dashboard is empty | the database is down | `systemctl status postgresql` |
| login fails after a redeploy | the JWT key does not match | `[JWT] Key` and `CONSOLE_JWT_KEY` |

### Wrong certificate path

The agent reads the certificate from the file path that is configured. In a
Debian based installation, `ca.cer`, `sftp.cer`, `agent.cer` and `agent.key`
must be present inside `/etc/openuem-agent/certificates`. On Windows the agent
file folder is `C:\Program Files\OpenUEM Agent`, and the certificates may be
placed next to the installer. In an RPM based installation the file ownership is
corrected with `chown openuem-agent:openuem-agent`. If the file exists but is
not readable, the symptom looks the same as "the file is missing".

### `ca.cer` is missing

`ca.cer` is the trust anchor for every other certificate. If that file is
missing, the agent cannot verify the certificate of NATS. The symptom is that
the connection starts and fails immediately. To resolve it, copy the `ca.cer`
produced by the CA into the agent's certificate folder and restart the agent
service.

### Wrong NATS host and port

In the agent's configuration the NATS server is written in the form
`host:4433`. In an RPM based installation, the `[NATS]` section of
`/etc/openuem-agent/openuem.ini` contains `NATSServers=host:4433`. During a
Debian installation the installer asks for the NATS server. If that answer is
wrong, the agent can never connect. After correcting it, both
`openuem-agent` and `openuem-agent-updater` must be restarted.

### DNS does not resolve

In a lab without DNS, `{YOUR_LOCAL_IP} {NATS_HOST} {OCSP_HOST} {CONSOLE_HOST}`
must be added to the hosts file. The LAN IP must be used there. `localhost` or
`127.0.0.1` must not be used — each container would then point at itself. This
mistake produces a very difficult symptom — the name resolves, but it resolves
to the wrong address.

### Firewall

Two kinds of path are required. Outbound — from the endpoint to port 4433 of the
NATS host. Inbound — to the console's 1323/1324 for administrators to enter, to
the agent's SFTP 2022 for the server to enter (used to read the log), and to the
VNC proxy 1443 for remote assistance. When checking the firewall, check in
sequence — first the outbound permission from the endpoint, then the port
listener on the server, and finally the network device in the middle.

### Clocks do not agree (clock skew)

TLS relies on time. A certificate carries two times, "not valid before" and
"expired". If the endpoint's clock runs ahead or behind, even a correct
certificate does not succeed. That symptom looks very much like "the certificate
is wrong". The clock must therefore be checked before the certificate. To
resolve it, NTP must be enabled on both sides.

### The database is down

PostgreSQL is the backing store for every component. So when the database goes
down the symptom is not a single one — workers fail repeatedly, the console
opens but the data does not appear, and the dashboard is empty. The first thing
to check is `sudo systemctl status postgresql`, and after that the host, port,
user and password of the connection URI. If the URI contains special
characters, percent-encoding must be applied — `te=st` is written as `te%3Dst`.

### The JWT key does not match after a redeploy

The JWT key is defined in `.env` as `CONSOLE_JWT_KEY`. That value is a secret
and must be replaced with a random 32-character string. If that value is
regenerated during a redeploy, every old token becomes invalid. The symptom is
logging in and being thrown out immediately, or an authentication prompt on
every page. To resolve it, restore the key to the same value and restart the
console.

## Log sources — which log to read, and when

| Source | Location | What to look for |
|---|---|---|
| Agent log | `openuem-log.txt` inside the agent's `logs` folder (on Windows `C:\Program Files\OpenUEM Agent`) | connectivity, certificate, SFTP, report delivery |
| Reading the agent log from the console | the "show agent log" action of an enabled agent (through SFTP) | reading without entering the endpoint |
| Console log | the component log on the server | HTTP errors, session, authentication |
| Worker log | the log of `openuem-agent-worker` | report acceptance, database writes |
| NATS log | the log of `openuem-nats-service` | client connections, authorization |
| OCSP log | the log of `openuem-ocsp-responder` | certificate check responses |

The installer creates an `openuem` user that owns the files, and makes that user
the owner of the configuration, the certificates and the logs. The log files
must therefore be read as that user.

The reading order must be defined precisely —

1. **Read the agent log first.** Most faults begin on the endpoint side. That
   log shows a missing certificate file, an unresolvable DNS name, and a failure
   to reach 4433 directly.
2. **Then read the NATS log.** The time the agent attempted the connection can
   be compared with the time NATS accepted it.
3. **Then read the worker log.** If the report arrives but does not appear on
   the dashboard, the cause may sit here.
4. **Finally check the database.** If the worker log contains a connection
   error, descend to the database layer.

Reading the agent log from the console is especially useful. The action list of
an enabled agent contains "show agent log", and that action pulls the log
through the agent's SFTP server (2022). So if SFTP is not enabled, or if 2022
is closed, this action does not work. In that situation the endpoint must be
entered directly.

## SMTP for registration mail

When a user is invited, OpenUEM sends that user an email. That process is owned
by `openuem-notification-worker`. So without SMTP settings, a new user's state
stays at "Pending email confirmation". In that state the user does not receive
the mail and therefore cannot confirm. The process steps are Pending email
confirmation → Review request → Certificate sent → Completed.

The order of checks — wrong SMTP host and port, wrong authentication, a missing
sender address, a spam filter blocking it. After that, look in the log of
`openuem-notification-worker` for an SMTP error.

## Integrating with external monitoring — an operational pattern

The methods described in this section are not built-in features of OpenUEM. The
OpenUEM documentation does not describe a Prometheus endpoint. What is described
here is therefore two patterns from practical operations.

**First — scheduled CSV export.** Export and store the CSV from the agents view
and the security view daily or weekly. Send those files to an external system (a
spreadsheet, a BI tool, storage). That way time-based questions such as "the
number of machines that have not reported within the last 30 days" can be
answered. The dashboard shows only the current state. It cannot answer this
question.

**Second — component health checking.** An external system checks the response
of each component on a schedule. The points checked are whether there is a
response on the console's 1323/1324, whether there is a response on OCSP's 8000,
whether a connection to PostgreSQL can be made, and whether the services are
active. That check obtains, from the external system's side, the same
information as the dashboard's blue section.

Both patterns share the same caution — always record the time of the data that
was extracted. A number without a time is worthless in later analysis.

## Operational cautions

- **Do not restart without knowing the cause.** `restart` makes the symptom
  disappear. After that the cause is no longer found in the log. The log must
  therefore be preserved before restarting.
- **Store the report with the date and the filter.** The file name must contain
  three things — the view, the filter and the date.
- **Do not treat the dashboard as the truth.** It can be five minutes behind.
- **Check one layer at a time.** Stop at the first failing layer and record the
  lower layers as "not tested yet".
- **Check the time.** Every certificate problem requires the clock to be checked
  as well.
- **Make a single change at a time.** Do not change the JWT key and the
  certificate at the same time.

## Self-check

**1. Does an exported report follow the filter that was on the screen?**
Yes. OpenUEM's PDF/CSV export preserves the current filter and sort. The filter
definition itself, however, must not be assumed to be contained in the file.

**2. What do the dashboard's three sections represent?**
Red — the work to be done today (those not reporting, pending updates, disabled
antivirus, agent/app updates). Green — the user, app and tag counts. Blue —
component status.

**3. In layered checking, when the first failing layer is found, how are the
lower layers recorded?** They are recorded as "not tested yet". No conclusion
about the state of a lower layer may be drawn before the cause of the failing
layer is resolved.

**4. What symptom does a client clock skew produce?** The TLS check fails. Even
a correct certificate is reported as "not valid before" or "expired".

**5. If a user is stuck at "Pending email confirmation", what must be checked
first?** The SMTP settings and the log of `openuem-notification-worker`. Without
SMTP the invitation mail is not sent.

## Technical review notes

- The content of the dashboard's three sections follows the description in
  MODULE_SPEC. The exact card names and the placement of the sections can change
  with the version — this needs re-checking per version.
- Whether the CSV file contains the filter definition itself is not stated
  precisely in the documentation. Only the point "the rows it contains follow
  the filter" can be confirmed.
- The relationship between clock skew and TLS is inferred from basic TLS theory.
  The exact log text of OpenUEM is not quoted.
- Session invalidation after a JWT key change is written as an analysis based on
  the configuration. There is no official statement on it.
- The absence of a Prometheus endpoint was confirmed, and the monitoring section
  is therefore presented only as an operational pattern.
- `docker compose ps` and `docker compose logs` are standard compose commands
  and are used alongside `docker compose up -d` from the OpenUEM documentation.
- Package versions (for example `0.7.0`) are not cited in this module.
