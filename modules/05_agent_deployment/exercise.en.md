# Module 05 — Exercises

Each of the six exercises consists of filling in or amending the corresponding function in `modules/05_agent_deployment/lab.py`. Each exercise can be run on its own.

```bash
python3 -c "import importlib.util; spec=importlib.util.spec_from_file_location('lab','modules/05_agent_deployment/lab.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); m.exercise_1()"
```

Change `exercise_N` to try each exercise. After each exercise the corresponding `[OK]` line must appear.

## Exercise 1 — Building the silent-install flag line

In order to deploy Windows endpoints at the same time you must build a single argument line for `openuem-agent-setup.exe` from a dictionary.

Requirements —

- The result must start with `/VERYSILENT`. It must appear exactly once.
- The flag order must be `cacert`, `cert`, `key`, `sftpcert`, `tenantid`, `siteid`, `server`, `sftp`, `vnc`.
- If `server` is absent, reject with `ValueError`.
- `tenantid` and `siteid` may only be accepted together. If only one is present, reject with `ValueError`.
- Only the flags that were supplied may appear in the result. Do not insert an empty value for a flag that was not supplied.
- The values for `sftp` and `vnc` must be 2022 and 1443.

Checked aspects — that `/VERYSILENT` appears exactly once, that `cacert` comes before `server`, and that both the pairing rule and the missing-`server` case are rejected.

## Exercise 2 — Checking certificate files per platform

The four files an agent needs are `ca.cer`, `sftp.cer`, `agent.cer`, `agent.key`. Compare the given platform and file list, and find the files that are missing.

Requirements —

- Return the correct folder for each platform. For Debian and Ubuntu `/etc/openuem-agent/certificates`, for the RPM family `/etc/openuem-agent`, and for Windows `C:\Program Files\OpenUEM Agent`.
- The `missing` list must follow the defined order of the four files.
- Files that are not needed must go into the `extra` list in alphabetical order.
- Reject an unknown platform with `ValueError`.
- In the case where all four files are present, both `missing` and `extra` must be empty.

Checked aspects — the case on Debian where `sftp.cer` and `agent.key` are missing, the case on RPM where an unneeded `notes.txt` is present, and the case on Windows where `agent.cer` and `agent.key` are missing.

## Exercise 3 — Checking the NATS endpoint and cluster list

The agent needs a `host:port` form in order to connect to the NATS server. If a cluster contains several servers, a comma-separated list must be accepted.

Requirements —

- If the `host:port` form is correct, accept it and return the number of servers.
- Reject a value containing `://`. A scheme is not needed.
- Reject a missing port, a port containing non-digit characters, and a port outside 1 to 65535.
- Reject a space after a comma, and a value that is entirely empty.
- If two servers with the same host are present, reject.
- Every rejection case must contain a reason string.

Checked aspects — that only the two correct values are accepted, that the other eight are rejected, and that each reason string is correct.

## Exercise 4 — Calculating the report interval

From the report interval, calculate the number of reports per day, the time the next report is due, and the lateness.

Requirements —

- Calculate the number of reports per day for 60, 30 and 15 minutes.
- For the profile check interval of 30 minutes, calculate the number per day and the number of profile checks per report.
- For a last report time of 09:10 and an interval of 60 minutes, show the next report time in `HH:MM` form.
- If `now` is 11:05, calculate the lateness in minutes and determine the state.
- Do not read the time from the machine. Calculate with fixed values only.

Checked aspects — the three report counts, the profile count of 48, 2 per cycle, the lateness of 55 minutes and the `overdue` state.

## Exercise 5 — Classifying log lines

Group the lines from `openuem-log.txt` by keyword. The groups are `certificate`, `connectivity`, `enrollment`, `sftp`, `vnc`, `configuration` and `unclassified`.

Requirements —

- Check the rule list from top to bottom and take the first group that matches.
- Compare in lower case.
- If no keyword matches, assign `unclassified`.
- Count the lines in each group and show them in alphabetical order.
- For the eight fixed log lines, seven kinds of group must come out.

Checked aspects — the count of each group, the two `unclassified` lines, and the effect of the rule order (`sftp: x509: certificate has expired` being `certificate`).

## Exercise 6 — Rating upgrade risk

For an agent upgrade, weight five factors, compute a score, and classify the risk as `low`, `medium` or `high`.

Requirements —

- The weights — certificate expiry 4, major version jump 3, a hand-edited `openuem.ini` 2, offline agents present 2, rollback untested 1.
- A score of 5 and above is `high`, 2 and above is `medium`, and the rest is `low`.
- Show the reason list in alphabetical order.
- If offline agents are present, include the count in the reason string.
- If there are no reasons, the score must be zero and the level `low`.

Four checked cases — a patch bump (`low`, 0), two offline agents with an edited ini (`medium`, 4), a major version with an edited ini (`high`, 5), and an expired certificate with an untested rollback (`high`, 5).
