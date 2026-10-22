# Module 08 — Exercises

These six exercises use the fixtures in `lab.py`. For each exercise you write one function and check the result with `assert`. To run —

```bash
python3 modules/08_patch_automation/lab.py
```

## Exercise 1 — Analysing the pending-update list

The `PENDING_UPDATES` fixture contains the number of pending updates by severity for each endpoint.

To do —

1. Calculate the total number of pending updates for each endpoint.
2. Calculate the fleet total for each severity (critical, important, moderate, low).
3. Sort the endpoint list by name and show it together with the totals.
4. Choose the two endpoints with the largest critical count as the priority list.

To check — the fleet total must be 31. The critical total must be 8. The endpoint with the fewest pending updates must be `MB-CEO-01`.

## Exercise 2 — Calculating maintenance-window availability

`MAINTENANCE_WINDOWS` defines the windows in UTC. Some windows continue past midnight. `ENDPOINT_OFFSETS` contains the UTC offset of each endpoint. `REFERENCE_NOW` is a fixed instant.

To do —

1. Calculate the local time of each endpoint using its offset.
2. Write a function that decides whether a time is inside a window. It must handle a midnight-spanning window correctly.
3. Treat the window start as inside and the window end as outside.
4. Sort and show the names of the windows available to each endpoint.

To check — `MB-CEO-01` must get `windows-ring-1`. `SRV-DB-01` must get `linux-ring-1`, which is the midnight-spanning window. `WS-ACC-01` must have no available window.

## Exercise 3 — Ordering patch waves by criticality

`UPDATE_BACKLOG` contains the severity of each patch and whether it needs a reboot. The wave rule is critical → wave 1, important → wave 2, moderate and low → wave 3.

To do —

1. Assign a wave to each patch.
2. Calculate the window duration — a base of 30 minutes, plus 60 minutes if a reboot is required.
3. Within a wave, put the patches that need a reboot first. Then sort by severity, then by name.
4. Show the member count and the maximum required window duration of each wave.

To check — wave 1 must contain two patches. Wave 3 must contain four patches. The window for wave 1 must be 90 minutes.

## Exercise 4 — Evaluating the validation matrix

`POST_DEPLOY_OBSERVATIONS` contains the facts measured after deployment. `VALIDATION_RULES` contains five checks.

To do —

1. Evaluate each endpoint against the five checks.
2. Store the names of the failed checks, sorted.
3. Calculate the total number of passes across all checks.
4. Treat an endpoint that fails `service_healthy` as requiring rollback.

To check — the total number of checks must be 15. The number of passes must be 11. The endpoint requiring rollback must be `SRV-APP-01` only.

## Exercise 5 — Calculating compliance percentage

`COMPLIANCE_ROWS` contains, for each endpoint, the number of patches required, the number installed, and the number of critical updates outstanding. The compliance criterion is a patch rate above 95 percent with zero critical pending.

To do —

1. Calculate the patch rate of each endpoint to one decimal place.
2. Decide whether the compliance criterion is met.
3. Calculate the fleet patch rate as the ratio of the total installed to the total required.
4. Produce the endpoint compliance percentage and the list of endpoints that do not meet the criterion.

To check — the fleet patch rate must be 94.4 percent. Endpoint compliance must be 60.0 percent. The exception list must contain two endpoints.

## Exercise 6 — Choosing the automation trigger

`AUTOMATION_JOBS` contains, for each job, the scope (fleet or single), the repetition (continuous or one-off) and whether a desired state is required.

To do —

1. Treat a job that has to be done once for a single endpoint as a deployment.
2. Among the remaining jobs, treat those that need a desired state as a profile.
3. Treat the remaining jobs as reports.
4. Sort and show the job names under each trigger. In addition, calculate the number of profile checks and report sends per day.

To check — all three triggers must have two jobs each. The profile check must be 48 times per day and the report 24 times.
