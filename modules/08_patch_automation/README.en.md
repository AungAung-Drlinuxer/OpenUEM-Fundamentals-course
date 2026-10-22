# Module 08 — Patch management and automation

This module teaches how to see the update state of endpoints with OpenUEM, how to arrange the patch workflow step by step, how to connect maintenance windows with change control, how to verify after deployment, and how to measure compliance.

## Prerequisites

- Module 05 (agent deployment) and Module 06 (enrollment) completed.
- The profile and task fundamentals from Module 07 (device management basics).
- At least one agent in enabled state, or just Python 3 to run `lab.py`.

## Learning outcomes

1. Read the four update facts in the Windows security view and distinguish which fact is policy-related and which is state-related.
2. Compare Linux pending security updates with the Windows KB state.
3. Arrange the detect → stage → deploy → verify workflow by wave.
4. Evaluate a maintenance window against timezone offsets.
5. Draw a validation matrix and measure the deployment result.
6. Plan recovery when there is no rollback, using snapshots, waves and package removal.
7. Read the compliance percentage together with the exception list.

## Files

| File | Content |
|---|---|
| `README.md` | This guide |
| `explanation.md` | Core concepts, two figures, workflow stages, self-check questions |
| `exercise.md` | Task list for the six exercises |
| `solution.md` | Answers and the actual output of `lab.py` |
| `lab.py` | Calculation lab that uses the standard library only |

## Running the lab

```bash
# run the module file — uses fixtures only, no network needed
python3 modules/08_patch_automation/lab.py
```

The lab needs no external state. It uses no network. It does not read the clock. Therefore the output is identical from one run to the next.

## Exercise map

| Exercise | Title | Concept practised |
|---|---|---|
| 1 | Analysing the pending-update list | Aggregating counts from the security view |
| 2 | Calculating maintenance-window availability | Timezone offsets and a midnight-spanning window |
| 3 | Ordering patch waves by criticality | Wave rules and window duration |
| 4 | Evaluating the validation matrix | Five post-deployment checks |
| 5 | Calculating compliance percentage | Difference between fleet rate and endpoint rate |
| 6 | Choosing the automation trigger | Choosing between profile, deployment and report |

## Time estimate

| Part | Time |
|---|---|
| Reading `explanation.md` | 40 minutes |
| The six exercises | 70 minutes |
| Review | 20 minutes |

## Points to note

- Every number in this module is demonstration fixture data. It is not a measurement from the OpenUEM console.
- The study computers do not have OpenUEM installed. The commands are real commands taken from the documentation, and the outputs are illustrative.
- OpenUEM is not a full patch orchestrator for OS updates. It reports update state, and a human makes the installation decision. This point is explained in detail in the final section of `explanation.md`.

## Follow-up module

In Module 08 you will continue to study how to present this module's compliance information as a report and how to search for problems.
