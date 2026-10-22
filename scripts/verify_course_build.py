#!/usr/bin/env python3
"""Verify a course built as one folder per module with a runnable lab.

Expected module layout: `modules/NN_snake_name/{README.md, explanation.md,
exercise.md, solution.md, lab.py}`. Every check below has caught a real defect
that a writing agent reported as done.

Checks (a failure sets exit code 1):
  * the required file set exists; anything extra is listed as info
  * `explanation.md` is at least `--min-chars` characters (Burmese is multi-byte:
    count characters, never bytes)
  * `exercise.md`'s `## Exercise N — <title>` headings and `lab.py`'s
    `def exercise_N()` count agree, and the count matches --exercises when given
  * a helper named `exercise_N_something` is reported — name helpers
    `_exercise_N_something`, or the exercise count is inflated
  * Mermaid fences are balanced, and the number of `Figure N —` captions equals the
    number of `ပုံရှင်းလင်းချက်` walkthroughs
  * no banned colloquial particle in prose, no foreign-script glyph, no emoji
  * `lab.py` exits 0, prints the pass line, and its stdout is byte-identical over
    `--runs` runs with a randomised hash seed — a lab that prints a wall-clock time
    or a temporary directory path passes once and then fails forever after

Reported as info only, never as a failure: backtick-quoted file paths that do not
resolve locally, because a course legitimately cites files in its own source
repository (`phases/...`, `code/...`).

Usage:
  python3 verify_course_build.py --repo ~/Documents/<Course>-course
  python3 verify_course_build.py --repo . --modules 01,03 --min-chars 6000 --runs 3
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

REQUIRED = ("README.md", "explanation.md", "exercise.md", "solution.md", "lab.py")

BANNED = ["ပါတယ်", "ပါဘူး", "ရမယ်", "ဖြစ်တယ်", "တဲ့", "နဲ့", "ဖို့", "ရဲ့",
          "နော်", "ပေါ့", "လို့", "ဆိုတာ", "ဒီ"]

# Ranges that never belong in a Burmese/English technical course. ✓ ✗ → — … ။ ၊
# are deliberate marks and sit outside these ranges on purpose.
FOREIGN = (("CJK punctuation", 0x3000, 0x303F), ("kana", 0x3040, 0x30FF),
           ("CJK ideographs", 0x4E00, 0x9FFF), ("Hangul", 0xAC00, 0xD7AF),
           ("Devanagari", 0x0900, 0x097F), ("Thai", 0x0E00, 0x0E7F),
           ("Cyrillic", 0x0400, 0x04FF))
EMOJI = (0x1F300, 0x1FAFF)

PASS_RE = re.compile(r"\[PASS\] All \d+/\d+ exercises passed successfully\.")
EX_HEAD = re.compile(r"^##\s+Exercise\s+\d+\s*[—–-]", re.M)
DEF_MAIN = re.compile(r"^def\s+exercise_(\d+)\s*\(", re.M)
DEF_HELP = re.compile(r"^def\s+exercise_\d+_\w+\s*\(", re.M)
FIG = re.compile(r"Figure\s+\d+\s*[—–-]")
WALK = "ပုံရှင်းလင်းချက်"
PATH_RE = re.compile(r"`([A-Za-z0-9_./~-]+\.(?:py|md|sh|json|yml|yaml|toml|txt|rs|ts|ipynb|csv))`")


def prose_lines(text: str):
    """Yield (line number, line) for lines OUTSIDE fenced code blocks."""
    inside = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            inside = not inside
            continue
        if not inside:
            yield number, line


def fence_report(text: str) -> tuple[int, int]:
    fences = [l for l in text.splitlines() if l.lstrip().startswith("```")]
    mermaid = [l for l in fences if l.lstrip().startswith("```mermaid")]
    return len(fences), len(mermaid)


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.infos: list[str] = []

    def check(self, module: str, ok: bool, what: str, detail: str = "") -> bool:
        if not ok:
            self.failures.append(f"{module}: {what}{(' — ' + detail) if detail else ''}")
        return ok

    def info(self, message: str) -> None:
        self.infos.append(message)


def check_module(module_dir: Path, report: Report, min_chars: int, exercises: int | None,
                 banned: list[str]) -> None:
    name = module_dir.name
    present = {p.name for p in module_dir.iterdir() if p.is_file()}
    missing = [f for f in REQUIRED if f not in present]
    report.check(name, not missing, "missing required file(s)", ", ".join(missing))
    extra = sorted(present - set(REQUIRED))
    if extra:
        report.info(f"{name}: extra file(s) — {', '.join(extra)} (allowed, e.g. Dockerfile.example)")

    explanation = module_dir / "explanation.md"
    if explanation.exists():
        text = explanation.read_text(encoding="utf-8")
        report.check(name, len(text) >= min_chars, "explanation.md below the depth floor",
                     f"{len(text)} < {min_chars} characters")

    ex_path, lab_path = module_dir / "exercise.md", module_dir / "lab.py"
    if ex_path.exists() and lab_path.exists():
        heads = len(EX_HEAD.findall(ex_path.read_text(encoding="utf-8")))
        lab = lab_path.read_text(encoding="utf-8")
        defs = len(DEF_MAIN.findall(lab))
        report.check(name, heads == defs, "exercise headings and lab functions disagree",
                     f"exercise.md={heads} lab.py={defs}")
        if exercises is not None:
            report.check(name, defs == exercises, "lab function count differs from --exercises",
                         f"{defs} != {exercises}")
        helpers = DEF_HELP.findall(lab)
        if helpers:
            report.check(name, False, "helper named exercise_N_* inflates the exercise count",
                         ", ".join(h.strip() for h in helpers))

    if explanation.exists():
        text = explanation.read_text(encoding="utf-8")
        fences, mermaid = fence_report(text)
        report.check(name, fences % 2 == 0, "unbalanced code fence in explanation.md",
                     f"{fences} fence lines")
        report.check(name, mermaid >= 2, "fewer than two Mermaid figures in explanation.md",
                     f"{mermaid} found")
        figures, walks = len(FIG.findall(text)), text.count(WALK)
        report.check(name, figures == walks, "figure captions and walkthroughs disagree",
                     f"Figure N={figures} walkthroughs={walks}")

    for path in sorted(module_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        lines = list(prose_lines(text))
        for particle in banned:
            hits = [n for n, l in lines if particle in l]
            if hits:
                report.check(name, False, f"banned particle '{particle}' in prose",
                             f"{path.name} line(s) {hits[:5]}")
        for kind, lo, hi in FOREIGN:
            hits = [n for n, l in lines if any(lo <= ord(c) <= hi for c in l)]
            if hits:
                report.check(name, False, f"{kind} glyph in prose", f"{path.name} line(s) {hits[:5]}")
        hits = [n for n, l in lines if any(EMOJI[0] <= ord(c) <= EMOJI[1] for c in l)]
        if hits:
            report.check(name, False, "emoji in prose", f"{path.name} line(s) {hits[:5]}")
        for ref in sorted(set(PATH_RE.findall(text))):
            if ref.startswith(SOURCE_PREFIXES):
                continue
            candidates = [path.parent / ref, module_dir / ref, path.parent.parent / ref]
            if not any(c.exists() for c in candidates):
                report.info(f"{name}: {path.name} cites '{ref}' — not in this repo (fine if it is a source file)")


def check_lab(repo: Path, module_dir: Path, report: Report, runs: int) -> None:
    lab = module_dir / "lab.py"
    if not lab.exists():
        return
    name = module_dir.name
    env = {**os.environ, "PYTHONHASHSEED": "random"}
    outputs: list[tuple[int, str]] = []
    for _ in range(max(1, runs)):
        proc = subprocess.run([sys.executable, str(lab)], cwd=str(repo), capture_output=True,
                              text=True, env=env)
        outputs.append((proc.returncode, proc.stdout))
    code, first = outputs[0]
    report.check(name, code == 0, "lab.py exited non-zero", f"exit {code}")
    report.check(name, bool(PASS_RE.search(first)), "lab.py printed no pass line",
                 PASS_RE.pattern)
    for other_code, other in outputs[1:]:
        if other != first:
            a = first.splitlines()
            b = other.splitlines()
            for i, (x, y) in enumerate(zip(a, b)):
                if x != y:
                    report.check(name, False, "lab.py stdout is not stable across runs",
                                 f"line {i + 1}: {x.strip()[:60]!r} vs {y.strip()[:60]!r}")
                    break
            else:
                report.check(name, False, "lab.py stdout length differs across runs", "")
            break


SOURCE_PREFIXES = ("phases/", "code/", "docs/", "src/", "docker/", "assets/", "scripts/",
                   "outputs/", "i18n/", "http", "www.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a course repo with per-module labs.")
    parser.add_argument("--repo", default=".", help="course repository root")
    parser.add_argument("--modules", default=None, help="comma-separated folder prefixes, e.g. 01,03")
    parser.add_argument("--min-chars", type=int, default=5000, dest="min_chars")
    parser.add_argument("--exercises", type=int, default=6, help="expected exercises per module")
    parser.add_argument("--runs", type=int, default=3, help="lab runs compared for stability")
    parser.add_argument("--no-labs", action="store_true", help="skip executing lab.py")
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    modules_root = repo / "modules"
    if not modules_root.is_dir():
        print(f"no modules/ directory under {repo}")
        return 1

    wanted = None if not args.modules else tuple(p.strip() for p in args.modules.split(",") if p.strip())
    module_dirs = sorted(d for d in modules_root.iterdir() if d.is_dir()
                         and (wanted is None or d.name.startswith(wanted)))
    if not module_dirs:
        print("no module directories matched")
        return 1

    report = Report()
    print(f"repo     : {repo}")
    print(f"modules  : {len(module_dirs)}")
    print("-" * 78)
    for module_dir in module_dirs:
        check_module(module_dir, report, args.min_chars, args.exercises, BANNED)
        if not args.no_labs:
            check_lab(repo, module_dir, report, args.runs)
        print(f"checked  : {module_dir.name}")

    print("-" * 78)
    if report.infos:
        print(f"info ({len(report.infos)}):")
        for line in report.infos:
            print(f"  - {line}")
    if report.failures:
        print(f"FAIL ({len(report.failures)}):")
        for line in report.failures:
            print(f"  - {line}")
        print("\n[FAILURE] fix the items above before committing.")
        return 1
    print("[SUCCESS] every module passed: file set, depth, exercise parity, figures,\n"
          "          register, and byte-stable lab runs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
