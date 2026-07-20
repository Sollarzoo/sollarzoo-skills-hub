"""Tests for the daily-report Toggl Track client."""

import sys
from datetime import date, datetime, timezone
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))

from toggl_track import (
    _token_from_dotenv,
    day_bounds_utc,
    effective_duration_seconds,
    summarize_entries,
)


def test_dotenv_supports_compatibility_key_without_evaluation(tmp_path):
    dotenv = tmp_path / ".env"
    dotenv.write_text("TOGGL_API_TOKEN='safe-token'\nOTHER=$(whoami)\n")
    assert _token_from_dotenv(dotenv) == "safe-token"


def test_day_bounds_use_requested_timezone():
    start, end = day_bounds_utc(date(2026, 7, 20), "Asia/Shanghai")
    assert start == "2026-07-19T16:00:00Z"
    assert end.startswith("2026-07-20T15:59:59.")


def test_stopped_entry_uses_duration():
    assert effective_duration_seconds({"duration": 5400}) == 5400


def test_running_entry_uses_start_time():
    now = datetime(2026, 7, 20, 12, 0, tzinfo=timezone.utc)
    entry = {"duration": -1, "start": "2026-07-20T10:30:00Z"}
    assert effective_duration_seconds(entry, now=now) == 5400


def test_summary_contains_no_credentials_and_sums_hours():
    now = datetime(2026, 7, 20, 12, 0, tzinfo=timezone.utc)
    summary = summarize_entries(
        [
            {
                "description": "故事板",
                "duration": 3600,
                "start": "2026-07-20T08:00:00Z",
                "stop": "2026-07-20T09:00:00Z",
            },
            {
                "description": "Blender",
                "duration": -1,
                "start": "2026-07-20T10:00:00Z",
                "stop": None,
            },
        ],
        now=now,
    )
    assert summary["entry_count"] == 2
    assert summary["running_count"] == 1
    assert summary["total_hours"] == 3.0
    assert "token" not in repr(summary).lower()
