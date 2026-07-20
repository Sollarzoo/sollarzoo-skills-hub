"""Daily-report skill helpers (P3): theme slugify, find existing, session-by-PS split."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional


_THEME_REPLACE_RE = re.compile(r"\s+")
_THEME_STRIP_RE = re.compile(r"[^\w一-鿿\-]+", flags=re.UNICODE)


def slugify_theme(theme: str) -> str:
    """Convert a free-form Chinese/English theme into a filesystem-safe slug.

    - Strips leading/trailing whitespace
    - Collapses internal whitespace to '-'
    - Removes special chars except [-\\w\\u4e00-\\u9fff]
    - Truncates to 40 chars
    - Strips leading/trailing dashes (e.g. ' -P3' → 'P3')
    - Empty → 'untitled'
    """
    s = theme.strip()
    s = _THEME_REPLACE_RE.sub("-", s)
    s = _THEME_STRIP_RE.sub("", s)
    s = s[:40]
    s = s.strip("-")
    return s or "untitled"


def find_existing_report_for_date(daily_dir: Path, date: str) -> Optional[Path]:
    """Find a previously-written report for the given date in daily_dir.

    Search order:
    1. `<date>-*.md` (v5.1+ themed filenames). Multiple matches → first alphabetically.
    2. `<date>.md` (pre-v5.1 legacy, no theme suffix). Returned as a fallback.

    Note: legacy pre-v5.1 reports are detected, but incremental writes will create
    themed `<date>-<theme>.md` going forward — the agent should manually `git mv`
    the legacy file if it wants to keep the same physical filename for the day.

    Returns Path or None.
    """
    daily_dir = Path(daily_dir)
    if not daily_dir.exists():
        return None
    matches = sorted(daily_dir.glob(f"{date}-*.md"))
    if matches:
        return matches[0]
    legacy = daily_dir / f"{date}.md"
    if legacy.exists():
        return legacy
    return None


def split_session_by_problem_space(entries: list[dict]) -> list[dict]:
    """Group entries by problem_space, preserving first-seen order.

    Each entry: {'problem_space': str|None, 'task_excerpt': str}
    Returns: list of {'problem_space': str|None, 'task_excerpt': '<concat>'}
    """
    order: list = []
    seen: dict = {}
    for e in entries:
        ps = e.get("problem_space")
        if ps not in seen:
            seen[ps] = {"problem_space": ps, "task_excerpt": e.get("task_excerpt", "")}
            order.append(ps)
        else:
            existing = seen[ps]["task_excerpt"]
            new = e.get("task_excerpt", "")
            seen[ps]["task_excerpt"] = (existing + "\n\n" + new) if existing else new
    return [seen[ps] for ps in order]
