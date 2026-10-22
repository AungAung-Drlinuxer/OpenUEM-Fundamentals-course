# Module 10 — Exercises

The six exercises of this module travel through a single scenario in order. Each
exercise corresponds to one function of `lab.py`. Do not move to the next one
until the current exercise is finished.

```bash
python3 modules/10_capstone/lab.py
```

This command runs all six exercises in order and ends with
`[PASS] All 6/6 exercises passed successfully.`

## Exercise 1 — Checking the readiness checklist

Read the `checks` table in `exercise_1()`. There are 12 checks, and each one
contains a rule (`eq`, `ge`, `le`) and two values.

To do:

1. Evaluate each check against its rule.
2. List the names of the failing checks.
3. If there is one failure, set the build gate to `NOT-READY`. If there is no
   failure it is `READY`.
4. Write one line on how the failing check connects to the later incident.

Question: why is it important that the readiness checklist can identify a single
blocker?

## Exercise 2 — Writing the enrollment wave plan

`exercise_2()` obtains the endpoint list from `_endpoints()`. The head office has
Windows 10, Linux 5 and macOS 3, and the branch has Windows 5, Linux 3 and
macOS 1.

To do:

1. Choose the pilot wave from the head office. There must be one endpoint per
   platform.
2. Assign the remaining head office endpoints as the second wave.
3. Assign all branch endpoints as the third wave.
4. For each wave, check the endpoint count, the set of platforms, whether there
   are duplicates, and the total coverage.
5. Check the constraint that a wave must not exceed 20 endpoints.

Question: explain why the pilot wave must contain three platforms.

## Exercise 3 — Evaluating the rollout gate

`exercise_3()` contains three measurements. The four gate requirements are as
follows.

| Gate | Requirement |
|---|---|
| G1 | current time inside the 01:00–05:00 window |
| G2 | reporting at 90% or above |
| G3 | zero validation failures |
| G4 | no open P1 incident |

To do:

1. Check the four gates in order for each measurement.
2. Record the name of each gate that is not met.
3. Produce the decision (`GO` or `HOLD`).
4. Write one line on the sequence of decisions across the three measurements.
5. Explain why the second measurement is `GO`.

Question: why is the third measurement `HOLD` even though every condition is met?

## Exercise 4 — Producing the compliance evidence summary

`exercise_4()` contains the list of the three non-compliant endpoints. Each one
has a category (`software-baseline` or `patch-level`) and a short reason.

To do:

1. Compute the total, the compliant count and the percentage for each platform.
2. State the overall compliance percentage to one decimal place.
3. List the non-compliant endpoints in alphabetical order.
4. Identify the platform with the lowest percentage.

Question: the overall figure of 88.9% is an acceptable number, so why must the
figure of a single platform be looked at separately?

## Exercise 5 — Selecting the root cause of the incident

`exercise_5()` contains ten observations (`signals`) and five causes
(`candidates`). Each cause has a list of expectations describing "which facts
would appear if that cause were true".

To do:

1. Count how many expectations match for each cause.
2. Compute the match ratio as a score.
3. Select the cause with the highest score.
4. Write one line for each of the other four causes stating which evidence
   excludes it.
5. Check the order of the services in the recovery plan.

Question: which cause is excluded by the fact that the 4 endpoints whose
certificates were not replaced continue to report?

## Exercise 6 — Computing the final scorecard

`exercise_6()` contains the weights and scores of six domains. The total weight
must be 100.

To do:

1. Compute the contribution of each domain (weight × score ÷ 100).
2. Check whether the total weight is 100.
3. State the weighted total score to one decimal place.
4. Identify the domain with the lowest score.
5. Decide pass or fail with the following requirement. The total must be 75 or
   above. No domain may be below 60.

Question: if one domain falls below 60, why is the result a fail even though the
total score is high?
