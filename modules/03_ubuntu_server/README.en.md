# Module 03 — Installing OpenUEM on Ubuntu 24.04 Server

This module builds an OpenUEM server from start to finish on a single Ubuntu 24.04
Server host using native packages. It begins with adding the apt repository, then
creates certificates, writes `/etc/openuem-server/openuem.ini`, starts the services
in the documented order, verifies them with `systemctl status` and the console URL,
places the console behind a reverse proxy, and finishes with hardening.

## What you will be able to do

| # | Skill |
|---|---|
| 1 | Add the OpenUEM apt repository on Ubuntu 24.04 and install every component package |
| 2 | Distinguish the responsibility and inbound port of each package |
| 3 | Create a certificate tree and issue certificates with `openuem-cert-manager client-cert` |
| 4 | Write the `[Console]` and `[JWT]` sections of `openuem.ini` |
| 5 | Start the seven services in order and verify them with `systemctl status`, `ss` and the console URL |
| 6 | Put the console behind a proxy with Caddy or nginx |
| 7 | Harden the host with the `openuem` user, `600` key permissions and a CA backup |

## Requirements

- **Module 02 must be complete.** The PostgreSQL database `openuem`, its role and the
  connection URI are created there. This module does not repeat that work.
- One Ubuntu 24.04 Server host, `sudo` rights and systemd
- DNS names for the console, NATS and OCSP (or a hosts file in the lab)
- Ports 1323, 1324, 4433 and 8000 free
- Python 3.10 or later to run the labs (no OpenUEM server required)

## Files

| File | Content |
|---|---|
| `README.en.md` | module introduction, objectives, requirements |
| `explanation.en.md` | step-by-step explanation, 3 figures, 6 self-check questions |
| `exercise.en.md` | 6 exercises |
| `solution.en.md` | answers and the lab's real output |
| `lab.py` | deterministic lab written with the Python standard library only |

## Running the lab

```bash
python3 modules/03_ubuntu_server/lab.py
```

The lab connects to no network, OpenUEM server or database. It is fixtures and
computation only. The six exercises are as follows.

| Exercise | Core skill |
|---|---|
| 1 | Mapping packages to component roles |
| 2 | Checking the service start order |
| 3 | Splitting `openuem.ini` by section |
| 4 | Computing the expiry date from `--years-valid` |
| 5 | Finding Console/Auth/NATS/OCSP port conflicts |
| 6 | Generating firewall rules from the port plan |

## Notes

- Every command output on these pages is a sample fixture marked
  `# simulated output — illustrative`. It is not the real output of your machine.
- Package versions and the exact repository lines can change between releases. Those
  points are recorded in the `Technical review notes` of `explanation.md`.
- The Docker/Podman compose path is covered in a separate module of this course.
