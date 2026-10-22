# Module 07 — Answers

Every output on this page is the actual stdout of running
`python3 modules/07_device_management/lab.py`. The lab data is a fixture created
for teaching and is not a measurement of any real fleet.

## Exercise 1 — Calculating inventory completeness

For each endpoint compute `100 × (tabs received) ÷ 10` and round to the nearest
integer. `lnx-301` received eight tabs, so it scores 80% and falls in the
`partial` group. The two empty tabs are `monitors` and `printers`. `mac-401`
received only six tabs, which is 60% and therefore `incomplete`. `ws-001` is
missing only `printers`, which is 90%. `ws-002` reported all ten tabs.

```text
inventory completeness — 10 tabs
  lnx-301   80%  partial    missing: monitors, printers
  mac-401   60%  incomplete missing: monitors, logical_disks, network_adapters, printers
  ws-001    90%  partial    missing: printers
  ws-002   100%  complete   missing: -
  complete   1
  incomplete 1
  partial    2
[OK] exercise_1 — inventory completeness scoring
```

This score shows how complete the data is, not how fresh it is. An endpoint can
score 100 while its report is more than 24 hours old. The score and the report
time therefore have to be read together.

## Exercise 2 — Choosing the package manager per OS

The OS family is used as the key and the engine is looked up. The two Windows
machines (desktop and server) get WinGet, the two Linux machines (Ubuntu and
Fedora) get Flatpak, and macOS gets HomeBrew. `freebsd` is not in the supported
list, so its result is empty.

```text
package manager selection per OS family
  ws-101   windows  11             WinGet
  srv-201  windows  Server 2022    WinGet
  lnx-301  linux    Ubuntu 24.04   Flatpak
  lnx-302  linux    Fedora 40      Flatpak
  mac-401  macos    14             HomeBrew
  bsd-501  freebsd  14             unsupported
  supported: 5/6
[OK] exercise_2 — package manager selection per OS
```

Note — on Linux the engine does not differ by distribution. Both Ubuntu and
Fedora use Flatpak. That fact means "a separate script per distribution is not
required".

## Exercise 3 — Modelling the deployment queue for an offline agent

In the first pass the requests of the two online agents arrive immediately. The
other three are queued. In the second pass `lnx-301` and `lnx-302` come back, so
their two requests arrive. `ws-002` has not come back yet, so its request is
still queued.

```text
deployment queue simulation — 5 requests
  pass 1 — delivery attempt
    ws-001   7zip.7zip              delivered (agent online)
    lnx-301  org.gimp.GIMP          queued (agent offline)
    mac-401  wget                   delivered (agent online)
    ws-002   Microsoft.PowerToys    queued (agent offline)
    lnx-302  org.videolan.VLC       queued (agent offline)
  pass 2 — reconnect wave: lnx-301, lnx-302
    lnx-301  org.gimp.GIMP          queued request delivered
    lnx-302  org.videolan.VLC       queued request delivered
    ws-002   Microsoft.PowerToys    still queued
  final: delivered=4 queued=1
[OK] exercise_3 — deployment request queue simulation
```

`queued` is not a failure. The request is waiting in NATS. As soon as `ws-002`
comes back it will be carried out.

## Exercise 4 — Validating profile tasks

The check runs in three steps — whether the family is known, whether that family
is available on the target platform, and whether the name is empty. If the first
check fails, the remaining steps are not run.

```text
profile task validation — family, platform, name
    t1  ACCEPT  install_package    windows  7zip.7zip
    t2  REJECT  registry_key       linux    not available on linux
    t3  ACCEPT  powershell_script  windows  baseline.ps1
    t4  REJECT  msi_package        macos    not available on macos
    t5  ACCEPT  shell_script       linux    harden.sh
    t6  REJECT  scheduled_task     windows  unknown task family
    t7  REJECT  local_user         macos    empty task name
  accepted=3 rejected=4
[OK] exercise_4 — profile task validation
```

`t7` is a good example. Its family and platform are correct, but it has no name.
If that task were accepted it would produce a meaningless error on the agent
side. Checking the name before saving a profile therefore matters.

## Exercise 5 — Selecting targets with a tag filter

In `all` mode all tags are required. The agents carrying both `finance` and `lab`
are `lnx-301` and `ws-001`. `mac-401` carries only `finance` and `ws-002` carries
only `lab`, so both are left out. In `any` mode carrying at least one tag is
enough, so `mac-401` is included as well.

```text
tag filter selection over 4 agents
  mode=all  tags=finance,lab   -> lnx-301, ws-001
  mode=any  tags=finance,kiosk -> lnx-301, mac-401, ws-001
  excluded by mode=all: 2
[OK] exercise_5 — tag filter selection
```

The selection result is always sorted alphabetically. The same filter therefore
always produces the same list. That guarantees the result does not change when a
profile is applied repeatedly.

## Exercise 6 — Aggregating health flags

The four flags are checked in order — report time, antivirus, updates, disk.
`ws-002` is past 1500 minutes and has three updates waiting, so it gets two
flags. `lnx-301` has seven updates and 8% free disk. `mac-401` has antivirus
disabled. Only `ws-001` is healthy.

```text
health flag aggregation — 1440 min report window, disk floor
  ws-001   healthy
  ws-002   not_reporting, updates_pending
  lnx-301  updates_pending, low_disk
  mac-401  antivirus_disabled
  antivirus_disabled   1
  low_disk             1
  not_reporting        1
  updates_pending      2
  healthy=1 of 4
[OK] exercise_6 — health flag aggregation
```

In the tally `updates_pending` is 2, because two endpoints carry that flag. The
total number of flags can be larger than the number of endpoints, because one
endpoint can carry several flags. That matters when reading the red section of
the dashboard.
