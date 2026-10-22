# Module 05 — Agent deployment

This module teaches installing the OpenUEM agent on endpoints, placing certificates, satisfying port requirements, and telling problems apart from the log. The server side may be fully ready, but without an agent an endpoint cannot be managed. That is why this module is the practical foundation of the whole course.

## Skills you will have after studying

- Explain the agent's work cycle (sending reports, checking profiles every 30 minutes).
- Distinguish the four certificate files each agent needs and know their location per platform.
- Install silently on Windows with `/VERYSILENT` flags.
- Place certificates after installation on Debian and the RPM family, and restart the services.
- List the ports a firewall requires.
- Classify a problem from `openuem-log.txt` by keyword.
- Rate the risk of an upgrade.

## Prerequisites

- Module 01 — OpenUEM's components and the basic idea of ports.
- Module 02 — NATS, PostgreSQL and a basic container practice environment.
- Module 03 — Server installation and certificate creation.
- A machine that can run scripts with the Python 3 standard library. (OpenUEM does not need to be installed.)

## Files

| File | Contents |
| --- | --- |
| `README.md` | The module's purpose and guidance |
| `explanation.md` | Concepts, figures, per-platform procedure and self-check questions |
| `exercise.md` | Six exercises |
| `solution.md` | Answers to the six exercises and the lab output |
| `lab.py` | An offline lab that uses the standard library only |

## Running the lab

```bash
python3 modules/05_agent_deployment/lab.py
```

The lab runs the six exercises in order and prints one `[OK]` line for each, and a `[PASS]` line at the end. The output is identical from run to run. It makes no network connection of any kind.

If you want to modify the lab yourself and run it, you can call each exercise individually.

```bash
python3 -c "import importlib.util,sys; spec=importlib.util.spec_from_file_location('lab','modules/05_agent_deployment/lab.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); m.exercise_1()"
```

## A note on the output

The OpenUEM commands in `explanation.md` are real commands taken from the official documentation. Their output, however, is illustrative output marked `# simulated output — illustrative` and is not a measured result. The output in `solution.md`, by contrast, is the result of actually running `lab.py`.

## What this module does not cover

- Performing admission and managing organizations, sites and tags — Module 06.
- Inventory tabs, package deployment and profile details — Module 07.
- Patch management and automation — Module 08.
- Dashboard triage and step-by-step connectivity checking — Module 09.

## Suggested sequence

1. Read `explanation.md` and make sure you understand the procedure from Figure 1 to Figure 3.
2. Try answering the five self-check questions.
3. Work through the six exercises in `exercise.md` in order.
4. Run the lab and check that you get the `[PASS]` line.
5. Compare with `solution.md`.
