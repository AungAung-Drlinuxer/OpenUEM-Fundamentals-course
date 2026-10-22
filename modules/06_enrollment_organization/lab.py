#!/usr/bin/env python3
"""Module 05 — Enrollment and organization lab (standard library only).

The lab simulates console bookkeeping on fixtures: no network, no clock, no
randomness, no temporary files. Every exercise asserts the rule it prints
before emitting its own [OK] line.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Exercise 1 — agent state transitions
# ---------------------------------------------------------------------------

ALLOWED_TRANSITIONS = {
    ("waiting_for_admission", "enabled"): "allow: admit from the console",
    ("waiting_for_admission", "disabled"): "allow: reject the admission request",
    ("enabled", "disabled"): "allow: disable a manageable agent",
    ("disabled", "enabled"): "allow: re-enable a disabled agent",
}


def exercise_1() -> None:
    """Validate candidate state changes against the admission state machine."""
    attempts = [
        ("agent-01", "waiting_for_admission", "enabled"),
        ("agent-02", "waiting_for_admission", "disabled"),
        ("agent-03", "enabled", "disabled"),
        ("agent-04", "disabled", "enabled"),
        ("agent-05", "enabled", "waiting_for_admission"),
        ("agent-06", "disabled", "waiting_for_admission"),
        ("agent-07", "enabled", "enabled"),
    ]

    print("exercise 1 — agent state transition validation")
    allowed_count = 0
    denied_count = 0
    for name, source, target in attempts:
        verdict = ALLOWED_TRANSITIONS.get((source, target))
        if verdict is None:
            if source == target:
                verdict = "deny: state is already the requested one"
            else:
                verdict = "deny: no rule returns to the admission queue"
            denied_count += 1
        else:
            allowed_count += 1
        print(f"  {name}  {source:<21} -> {target:<21} {verdict}")

    assert allowed_count == 4, allowed_count
    assert denied_count == 3, denied_count
    assert ("enabled", "waiting_for_admission") not in ALLOWED_TRANSITIONS
    assert ("disabled", "waiting_for_admission") not in ALLOWED_TRANSITIONS
    print(f"  summary: allow={allowed_count} deny={denied_count}")
    print("[OK] exercise_1 — state transitions follow the admission state machine")


# ---------------------------------------------------------------------------
# Exercise 2 — admission queue summary
# ---------------------------------------------------------------------------

AGENTS = [
    {"name": "PC-001", "org": "head-office", "platform": "windows",
     "state": "enabled", "wait_minutes": 0},
    {"name": "PC-002", "org": "head-office", "platform": "linux",
     "state": "enabled", "wait_minutes": 0},
    {"name": "PC-003", "org": "branch-office", "platform": "windows",
     "state": "disabled", "wait_minutes": 0},
    {"name": "PC-004", "org": "head-office", "platform": "macos",
     "state": "waiting_for_admission", "wait_minutes": 240},
    {"name": "PC-005", "org": "lab", "platform": "linux",
     "state": "enabled", "wait_minutes": 0},
    {"name": "PC-006", "org": "branch-office", "platform": "windows",
     "state": "enabled", "wait_minutes": 0},
    {"name": "PC-007", "org": "branch-office", "platform": "windows",
     "state": "waiting_for_admission", "wait_minutes": 1840},
    {"name": "PC-008", "org": "lab", "platform": "macos",
     "state": "disabled", "wait_minutes": 0},
    {"name": "PC-009", "org": "head-office", "platform": "linux",
     "state": "waiting_for_admission", "wait_minutes": 920},
    {"name": "PC-011", "org": "lab", "platform": "linux",
     "state": "waiting_for_admission", "wait_minutes": 75},
    {"name": "PC-012", "org": "head-office", "platform": "windows",
     "state": "enabled", "wait_minutes": 0},
    {"name": "PC-014", "org": "branch-office", "platform": "macos",
     "state": "waiting_for_admission", "wait_minutes": 1560},
]

STATE_ORDER = ("disabled", "enabled", "waiting_for_admission")


def exercise_2() -> None:
    """Summarise a mixed fixture into a state census and an owner queue."""
    by_state = {state: 0 for state in STATE_ORDER}
    waiting_by_org: dict[str, int] = {}
    for agent in AGENTS:
        by_state[agent["state"]] += 1
        if agent["state"] == "waiting_for_admission":
            waiting_by_org[agent["org"]] = waiting_by_org.get(agent["org"], 0) + 1

    waiting = [a for a in AGENTS if a["state"] == "waiting_for_admission"]
    waiting.sort(key=lambda a: (-a["wait_minutes"], a["name"]))

    print("exercise 2 — admission queue summary")
    print(f"  fixture size: {len(AGENTS)} agents")
    print("  state                   count")
    for state in STATE_ORDER:
        print(f"  {state:<23} {by_state[state]:>5}")
    print("  waiting per organization")
    for org in sorted(waiting_by_org):
        print(f"  {org:<23} {waiting_by_org[org]:>5}")
    print("  oldest waiting (top 3)")
    for agent in waiting[:3]:
        print(f"  {agent['name']:<8}{agent['org']:<16}"
              f"{agent['platform']:<9}{agent['wait_minutes']:>6} min")

    assert len(AGENTS) == 12
    assert sum(by_state.values()) == 12
    assert by_state["waiting_for_admission"] == 5
    assert sum(waiting_by_org.values()) == 5
    assert waiting[0]["name"] == "PC-007"
    assert max(waiting_by_org.values()) == 2
    print("[OK] exercise_2 — queue census and per-organization backlog agree")


# ---------------------------------------------------------------------------
# Exercise 3 — organization / site assignment resolution
# ---------------------------------------------------------------------------

ORGANIZATIONS = {
    "branch-office": {"sites": ["warehouse"], "default": False},
    "head-office": {"sites": ["hq-floor1", "hq-floor2"], "default": True},
    "lab": {"sites": [], "default": False},
}
DEFAULT_ORG = "head-office"

ASSIGNMENT_REQUESTS = [
    ("PC-101", "", ""),
    ("PC-102", "branch-office", ""),
    ("PC-103", "head-office", "hq-floor2"),
    ("PC-104", "lab", ""),
    ("PC-105", "branch-office", "hq-floor1"),
    ("PC-106", "unknown-org", "warehouse"),
]


def exercise_3() -> None:
    """Resolve organization and site columns using the documented rules."""
    print("exercise 3 — organization and site assignment resolution")
    resolved = 0
    rejected = 0
    results = []
    for endpoint, org, site in ASSIGNMENT_REQUESTS:
        chosen_org = org if org else DEFAULT_ORG
        entry = ORGANIZATIONS.get(chosen_org)
        if entry is None:
            results.append((endpoint, chosen_org, site,
                            "error: unknown organization"))
            rejected += 1
            continue
        available = sorted(entry["sites"])
        if not available:
            results.append((endpoint, chosen_org, site,
                            "error: organization has no site"))
            rejected += 1
            continue
        chosen_site = site if site else available[0]
        if chosen_site not in available:
            results.append((endpoint, chosen_org, chosen_site,
                            "error: site does not belong to organization"))
            rejected += 1
            continue
        results.append((endpoint, chosen_org, chosen_site, "ok"))
        resolved += 1

    for endpoint, org, site, status in results:
        print(f"  {endpoint:<8}{org:<16}{site:<12}{status}")
    print(f"  summary: resolved={resolved} rejected={rejected}")

    assert resolved == 3, resolved
    assert rejected == 3, rejected
    by_endpoint = {r[0]: r for r in results}
    assert by_endpoint["PC-101"][1] == "head-office"
    assert by_endpoint["PC-101"][2] == "hq-floor1"
    assert by_endpoint["PC-104"][3].startswith("error")
    print("[OK] exercise_3 — default organization and site fallback resolved")


# ---------------------------------------------------------------------------
# Exercise 4 — CSV import validation
# ---------------------------------------------------------------------------

EXISTING_ORGS = {"branch-office", "head-office"}
EXISTING_EMAILS: set[str] = set()

ORG_ROWS = [
    (1, "east-branch", "depot-a"),
    (2, "west-branch", ""),
    (3, "east-branch", "depot-b"),
    (4, "head-office", "hq-floor3"),
    (5, "central", "depot-c"),
]

USER_ROWS = [
    (1, "a@openuem.example", "head-office", "hq-floor1"),
    (2, "b@openuem.example", "ghost-org", "depot"),
    (3, "c@openuem.example", "branch-office", "hq-floor1"),
    (4, "a@openuem.example", "head-office", "hq-floor2"),
    (5, "d@openuem.example", "east-branch", "depot-a"),
]


def exercise_4() -> None:
    """Validate organization CSV rows, then user CSV rows that depend on them."""
    print("exercise 4 — CSV import validation (organizations then users)")

    known_orgs = set(EXISTING_ORGS)
    org_sites: dict[str, list[str]] = {
        "branch-office": ["warehouse"],
        "head-office": ["hq-floor1", "hq-floor2"],
    }
    org_errors = []
    org_accepted = 0
    for row, name, site in ORG_ROWS:
        if not site:
            org_errors.append((row, name, "error: site column is empty"))
        elif name in known_orgs:
            reason = ("error: duplicate organization name in file"
                      if name not in EXISTING_ORGS
                      else "error: organization already exists on the server")
            org_errors.append((row, name, reason))
        else:
            known_orgs.add(name)
            org_sites[name] = [site]
            org_accepted += 1

    print(f"  organization rows: {len(ORG_ROWS)}  accepted: {org_accepted}"
          f"  rejected: {len(org_errors)}")
    for row, name, reason in sorted(org_errors):
        print(f"    row {row}  {name:<14}{reason}")

    known_emails = set(EXISTING_EMAILS)
    user_errors = []
    user_accepted = 0
    for row, email, org, site in USER_ROWS:
        if org not in known_orgs:
            user_errors.append((row, email, f"error: unknown organization {org}"))
        elif site not in org_sites.get(org, []):
            user_errors.append(
                (row, email, f"error: site {site} does not belong to {org}"))
        elif email in known_emails:
            user_errors.append((row, email, "error: duplicate user email in file"))
        else:
            known_emails.add(email)
            user_accepted += 1

    print(f"  user rows: {len(USER_ROWS)}  accepted: {user_accepted}"
          f"  rejected: {len(user_errors)}")
    for row, email, reason in sorted(user_errors):
        print(f"    row {row}  {email:<20}{reason}")
    print("  note: organizations are imported before users because row 5 needs"
          " east-branch")

    assert org_accepted == 2, org_accepted
    assert len(org_errors) == 3, org_errors
    assert user_accepted == 2, user_accepted
    assert len(user_errors) == 3, user_errors
    assert any("already exists" in reason for _, _, reason in org_errors)
    assert any("duplicate" in reason for _, _, reason in org_errors)
    assert any("does not belong" in reason for _, _, reason in user_errors)
    print("[OK] exercise_4 — CSV rows rejected for duplicates and missing site")


# ---------------------------------------------------------------------------
# Exercise 5 — capability matrix and least privilege
# ---------------------------------------------------------------------------

CAPABILITIES = [
    "admit_agent",
    "export_reports",
    "force_report",
    "manage_orgs",
    "manage_users",
    "remote_assistance",
    "view_inventory",
]

ROLE_CAPS = {
    "administrator": {
        "admit_agent", "export_reports", "force_report", "manage_users",
        "remote_assistance", "view_inventory",
    },
    "operator": {
        "export_reports", "force_report", "remote_assistance", "view_inventory",
    },
    "owner": set(CAPABILITIES),
    "read_only": {"export_reports", "view_inventory"},
}

REQUIRED_DUTY = {"force_report", "view_inventory"}
PROPOSED_ASSIGNMENT = ("helpdesk-01", "administrator")


def exercise_5() -> None:
    """Show the matrix and pick the smallest role that covers a duty."""
    print("exercise 5 — administrator capability matrix and least privilege")
    roles = sorted(ROLE_CAPS)
    header = "  " + f"{'capability':<22}" + "".join(f"{r:<17}" for r in roles)
    print(header.rstrip())
    for capability in CAPABILITIES:
        cells = "".join(
            f"{('Y' if capability in ROLE_CAPS[r] else '-'):<17}" for r in roles
        )
        print(f"  {capability:<22}{cells}".rstrip())

    candidates = []
    for role in roles:
        caps = ROLE_CAPS[role]
        if REQUIRED_DUTY <= caps:
            candidates.append((len(caps - REQUIRED_DUTY), role))
    candidates.sort()

    print("  required capabilities: " + ", ".join(sorted(REQUIRED_DUTY)))
    print("  candidates (excess capabilities):")
    for excess, role in candidates:
        print(f"    {role:<16}excess {excess}")
    minimal_role = candidates[0][1]
    print(f"  least privilege role: {minimal_role}")

    user, proposed = PROPOSED_ASSIGNMENT
    proposed_excess = len(ROLE_CAPS[proposed] - REQUIRED_DUTY)
    verdict = ("rejected (operator sufficient, excess "
               f"{proposed_excess})") if proposed != minimal_role else "accepted"
    print(f"  proposal {user} -> {proposed}: {verdict}")

    assert len(CAPABILITIES) == 7
    assert ROLE_CAPS["read_only"] < ROLE_CAPS["operator"] < ROLE_CAPS["owner"]
    assert "manage_orgs" not in ROLE_CAPS["administrator"]
    assert minimal_role == "operator", minimal_role
    assert candidates[0][0] == 2
    assert verdict.startswith("rejected")
    print("[OK] exercise_5 — smallest sufficient role selected for the duty")


# ---------------------------------------------------------------------------
# Exercise 6 — certificate lifecycle states
# ---------------------------------------------------------------------------

CERTIFICATE_RULES = {
    ("absent", "admission_issue"):
        ("issued", "allow: server.cer/server.key pair created"),
    ("issued", "first_report"):
        ("active", "allow: agent reports over TLS with the pair"),
    ("active", "regenerate"):
        ("issued", "allow: old certificate revoked, new pair created"),
    ("issued", "regenerate"):
        ("issued", "allow: pair replaced before activation"),
    ("issued", "revoke"):
        ("revoked", "allow: administrators revoke the certificate"),
    ("active", "revoke"):
        ("revoked", "allow: administrators revoke the certificate"),
    ("revoked", "admission_issue"):
        ("issued", "allow: re-admission creates a fresh pair"),
}

CERTIFICATE_EVENTS = [
    ("PC-201", ["admission_issue", "first_report", "regenerate", "first_report"]),
    ("PC-202", ["admission_issue", "revoke"]),
    ("PC-203", ["admission_issue", "revoke", "admission_issue"]),
    ("PC-204", ["first_report"]),
]


def exercise_6() -> None:
    """Walk certificate events per agent and validate every step."""
    print("exercise 6 — certificate lifecycle states")
    final_states = {}
    denials = 0
    for agent, events in CERTIFICATE_EVENTS:
        state = "absent"
        for event in events:
            rule = CERTIFICATE_RULES.get((state, event))
            if rule is None:
                denials += 1
                print(f"  {agent:<8}{event:<17}{state:<9} -> {state:<9}"
                      "deny: event is not permitted in the current state")
                continue
            target, verdict = rule
            print(f"  {agent:<8}{event:<17}{state:<9} -> {target:<9}{verdict}")
            state = target
        final_states[agent] = state

    print("  final states")
    for agent in sorted(final_states):
        print(f"  {agent:<8}{final_states[agent]}")

    assert final_states["PC-201"] == "active", final_states["PC-201"]
    assert final_states["PC-202"] == "revoked", final_states["PC-202"]
    assert final_states["PC-203"] == "issued", final_states["PC-203"]
    assert final_states["PC-204"] == "absent", final_states["PC-204"]
    assert denials == 1, denials
    assert "active" in {t for t, _ in CERTIFICATE_RULES.values()}
    print("[OK] exercise_6 — certificate lifecycle states and revocations traced")


def main() -> int:
    exercise_1()
    exercise_2()
    exercise_3()
    exercise_4()
    exercise_5()
    exercise_6()
    print("[PASS] All 6/6 exercises passed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
