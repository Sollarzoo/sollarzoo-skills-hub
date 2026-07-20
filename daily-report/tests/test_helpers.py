"""Tests for daily-report skill helpers."""
import sys
from pathlib import Path
import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))
from helpers import slugify_theme, find_existing_report_for_date, split_session_by_problem_space


def test_slugify_theme_chinese():
    assert slugify_theme("引导页流程重构") == "引导页流程重构"


def test_slugify_theme_strips_spaces():
    assert slugify_theme("  P1 验证 跑通 ") == "P1-验证-跑通"


def test_slugify_theme_rejects_special_chars():
    s = slugify_theme("hello/world: test")
    assert "/" not in s and ":" not in s


def test_slugify_theme_empty_falls_back():
    assert slugify_theme("") == "untitled"


def test_slugify_theme_truncates_to_40():
    long = "abc" * 30
    assert len(slugify_theme(long)) <= 40


def test_find_existing_report_no_match(tmp_path):
    (tmp_path / "docs" / "daily").mkdir(parents=True)
    out = find_existing_report_for_date(tmp_path / "docs" / "daily", "2026-05-17")
    assert out is None


def test_find_existing_report_finds_themed(tmp_path):
    d = tmp_path / "docs" / "daily"
    d.mkdir(parents=True)
    target = d / "2026-05-17-引导页重构.md"
    target.write_text("# 日报\n")
    out = find_existing_report_for_date(d, "2026-05-17")
    assert out == target


def test_find_existing_report_ignores_other_dates(tmp_path):
    d = tmp_path / "docs" / "daily"
    d.mkdir(parents=True)
    (d / "2026-05-16-旧主题.md").write_text("old")
    out = find_existing_report_for_date(d, "2026-05-17")
    assert out is None


def test_split_session_single_ps():
    out = split_session_by_problem_space([
        {"problem_space": "ps-a", "task_excerpt": "做了 X"},
    ])
    assert len(out) == 1
    assert out[0]["problem_space"] == "ps-a"


def test_split_session_multiple_ps_in_order():
    out = split_session_by_problem_space([
        {"problem_space": "ps-a", "task_excerpt": "X"},
        {"problem_space": "ps-a", "task_excerpt": "Y"},
        {"problem_space": "ps-b", "task_excerpt": "Z"},
    ])
    assert len(out) == 2
    assert out[0]["problem_space"] == "ps-a"
    assert "X" in out[0]["task_excerpt"] and "Y" in out[0]["task_excerpt"]
    assert out[1]["problem_space"] == "ps-b"


def test_split_session_no_ps_returns_unassigned():
    out = split_session_by_problem_space([
        {"problem_space": None, "task_excerpt": "miscellaneous"},
    ])
    assert len(out) == 1
    assert out[0]["problem_space"] is None


def test_find_existing_report_finds_legacy_plain(tmp_path):
    """Pre-v5.1 plain <date>.md (no theme) is also detected."""
    d = tmp_path / "docs" / "daily"
    d.mkdir(parents=True)
    legacy = d / "2026-05-17.md"
    legacy.write_text("# 旧日报\n")
    out = find_existing_report_for_date(d, "2026-05-17")
    assert out == legacy


def test_find_existing_report_prefers_themed_over_legacy(tmp_path):
    """If both themed and plain exist for same date, themed wins."""
    d = tmp_path / "docs" / "daily"
    d.mkdir(parents=True)
    (d / "2026-05-17.md").write_text("legacy")
    themed = d / "2026-05-17-新主题.md"
    themed.write_text("new")
    out = find_existing_report_for_date(d, "2026-05-17")
    assert out == themed


def test_slugify_theme_strips_leading_trailing_dashes():
    assert slugify_theme(" -P3") == "P3"
    assert slugify_theme("-P3-") == "P3"
    assert slugify_theme("---") == "untitled"
