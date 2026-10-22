# Module 07 — Exercises

All six exercises are implemented in `lab.py`. You can run them one at a time by
calling the function name, or run the whole file.

```bash
python3 modules/07_device_management/lab.py
```

Each exercise reads fixture data in code and computes the result. It is
recommended that you compute it yourself before looking at the answer.

## Exercise 1 — Calculating inventory completeness

You are given a fixture of which tabs are present in the inventory report of
four endpoints. Using the ten inventory tabs in total as the basis, for each
endpoint —

1. Find the number of tabs received.
2. Compute the percentage score (round to an integer).
3. Assign a state by score — 95 and above is `complete`, 80 and above is `partial`, the rest is `incomplete`.
4. List the tabs that are missing.

Sort by endpoint name and show the result. Finally summarise the count of each
state. Check the result with an assertion.

## Exercise 2 — Choosing the package manager per OS

You are given the OS family and version of six endpoints. For each OS family
pick the relevant deployment engine —

- `windows` → WinGet
- `linux` → Flatpak
- `macos` → HomeBrew
- any other family → no support

For each endpoint show the name, the OS family, the version and the engine.
Compare the number of supported endpoints with the total. Check with an
assertion that the result for a family without an engine is empty.

## Exercise 3 — Modelling the deployment queue for an offline agent

You are given five deployment requests. Each request carries an endpoint, a
package, and whether the agent is online.

1. In the first pass, check each request. If the agent is online mark it `delivered`; if not, mark it `queued`.
2. In the second pass, assume two endpoints come back and connect. Change the queued requests of those endpoints to `delivered`.
3. Show the requests that are still `queued`.
4. Finally summarise the two counts.

The schedule must always produce the same result. Sort by endpoint name.

## Exercise 4 — Validating profile tasks

A profile contains seven tasks. Each task has an `id`, a `family`, a `platform`
and a `name`. Accept or reject them with the following rules —

- `registry_key`, `powershell_script` and `msi_package` are available only on Windows.
- `shell_script` is available only on Linux and macOS.
- `install_package`, `uninstall_package`, `local_user` and `local_group` are available on all platforms.
- Reject an unknown family.
- Reject a task whose name is empty.

For each task show `ACCEPT` or `REJECT` together with the reason for rejection.
Summarise the accepted and rejected counts.

## Exercise 5 — Selecting targets with a tag filter

Four agents carry tags. A filter contains a list of tags and a mode (`all` or
`any`).

- In `all` mode select the agents that carry all of the tags.
- In `any` mode select the agents that carry at least one of the tags.

Compute two filters — `finance` and `lab` in `all` mode, then `finance` and
`kiosk` in `any` mode. Show the selected agent names sorted alphabetically.
Compute how many were left out in each mode.

## Exercise 6 — Aggregating health flags

You are given four kinds of state for four endpoints — the minutes elapsed since
the last report, whether antivirus is running, the number of pending updates,
and the free disk percentage. Set flags with the following rules —

- more than 1440 minutes → `not_reporting`
- antivirus disabled → `antivirus_disabled`
- one or more pending updates → `updates_pending`
- free disk below 10 percent → `low_disk`

Show the flags of each endpoint (if there is no flag, `healthy`). Then show the
count of each flag sorted alphabetically. Finally compare the number of healthy
endpoints with the total.
