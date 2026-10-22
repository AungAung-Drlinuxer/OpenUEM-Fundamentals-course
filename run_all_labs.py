#!/usr/bin/env python3
"""Run every module lab and print an aligned dashboard.

Discovery: modules/*/lab.py — each must exit 0, print its per-exercise
[OK] lines and end with '[PASS] All 6/6 exercises passed successfully.'
Usage: python3 run_all_labs.py
"""
import subprocess
import sys
import time
from pathlib import Path

MODULE_DESCRIPTIONS = {
    "01_introduction": "Endpoint management, components, lifecycle",
    "02_postgresql": "PostgreSQL install, role/db, pg_hba, URI encoding",
    "03_ubuntu_server": "Ubuntu 24.04 native server install and config",
    "04_docker_compose": "Docker/Podman compose deployment and .env",
    "05_agent_deployment": "Windows/macOS/Linux agents, certificates, ports",
    "06_enrollment_organization": "Admission, orgs/sites, tags, users, roles",
    "07_device_management": "Inventory, packages, profiles, remote assistance",
    "08_patch_automation": "Update visibility, windows, validation, compliance",
    "09_reporting_troubleshooting": "Reports, dashboard triage, layered diagnosis",
    "10_capstone": "Two-site, three-platform end-to-end scenario",
}


def main() -> int:
    root = Path(__file__).resolve().parent
    rows = []
    total_ok = 0
    failed = []
    for mod in sorted((root / "modules").iterdir()):
        lab = mod / "lab.py"
        if not mod.is_dir() or not lab.exists():
            rows.append((mod.name, MODULE_DESCRIPTIONS.get(mod.name, ""), 0,
                         "MISSING", "-"))
            failed.append(mod.name)
            continue
        t0 = time.perf_counter()
        r = subprocess.run([sys.executable, str(lab)], capture_output=True,
                           text=True, cwd=root)
        dt = time.perf_counter() - t0
        ok = r.stdout.count("[OK]")
        passed = r.returncode == 0 and "[PASS]" in r.stdout
        if passed:
            total_ok += ok
        else:
            failed.append(mod.name)
        rows.append((mod.name, MODULE_DESCRIPTIONS.get(mod.name, ""), ok,
                     "PASS" if passed else "FAIL", f"{dt:.2f}s"))

    w1 = max(len(r[0]) for r in rows)
    w2 = max(len(r[1]) for r in rows)
    print(f"{'Module'.ljust(w1)}  {'Topics'.ljust(w2)}  "
          f"{'Ex':>3}  {'Status':6}  {'Time':>6}")
    print("-" * (w1 + w2 + 24))
    for name, desc, ok, status, dt in rows:
        print(f"{name.ljust(w1)}  {desc.ljust(w2)}  {ok:3d}  {status:6}  {dt:>6}")
    print("-" * (w1 + w2 + 24))
    if failed:
        print(f"FAILED module(s): {', '.join(failed)}")
        return 1
    print(f"[PASS] All {len(rows)} modules passed — {total_ok} exercises OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
