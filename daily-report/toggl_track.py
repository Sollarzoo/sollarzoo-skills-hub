"""Safe Toggl Track API v9 client for the daily-report skill.

Credentials are read without shell evaluation and never included in stdout,
exceptions, or the JSON result.
"""

from __future__ import annotations

import argparse
import base64
import getpass
import json
import os
import subprocess
import sys
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


API_BASE = "https://api.track.toggl.com/api/v9"
KEYCHAIN_SERVICE = "pal-daily-report-toggl-track"
TOKEN_KEYS = ("TOGGL_TRACK_API_TOKEN", "TOGGL_API_TOKEN")


class TogglTrackError(RuntimeError):
    """A sanitized Toggl Track failure safe to show to the user."""


def _token_from_dotenv(path: Path) -> str:
    if not path.is_file():
        return ""
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.removeprefix("export ").strip()
        if key not in TOKEN_KEYS:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        return value.strip()
    return ""


def load_api_token(dotenv_path: Path | None = None) -> str:
    """Load a token from env, .env, or Keychain without shell interpolation."""
    for key in TOKEN_KEYS:
        token = os.environ.get(key, "").strip()
        if token:
            return token

    token = _token_from_dotenv(dotenv_path or Path.cwd() / ".env")
    if token:
        return token

    if sys.platform == "darwin":
        result = subprocess.run(
            [
                "security",
                "find-generic-password",
                "-a",
                getpass.getuser(),
                "-s",
                KEYCHAIN_SERVICE,
                "-w",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        token = result.stdout.strip()
        if result.returncode == 0 and token:
            return token

    raise TogglTrackError(
        "未找到 Toggl Track API Token；请设置 TOGGL_TRACK_API_TOKEN / "
        "TOGGL_API_TOKEN，或写入 macOS Keychain"
    )


def day_bounds_utc(day: date, timezone_name: str) -> tuple[str, str]:
    """Return local-day boundaries converted to RFC3339 UTC timestamps."""
    zone = ZoneInfo(timezone_name)
    start = datetime.combine(day, time.min, tzinfo=zone)
    end = datetime.combine(day, time.max, tzinfo=zone)
    return (
        start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        end.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
    )


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def effective_duration_seconds(
    entry: dict[str, Any], now: datetime | None = None
) -> int:
    """Return stopped or running duration, never below zero."""
    duration = int(entry.get("duration") or 0)
    if duration >= 0:
        return duration

    start_value = entry.get("start")
    if not start_value:
        return 0
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    return max(0, int((current - _parse_datetime(start_value)).total_seconds()))


def summarize_entries(
    entries: Iterable[dict[str, Any]], now: datetime | None = None
) -> dict[str, Any]:
    """Build a reviewable, secret-free daily summary."""
    items: list[dict[str, Any]] = []
    total_seconds = 0
    running_count = 0

    for entry in entries:
        seconds = effective_duration_seconds(entry, now=now)
        running = int(entry.get("duration") or 0) < 0
        total_seconds += seconds
        running_count += int(running)
        items.append(
            {
                "description": entry.get("description") or "(无描述)",
                "project_id": entry.get("project_id"),
                "tags": entry.get("tags") or [],
                "start": entry.get("start"),
                "stop": entry.get("stop"),
                "running": running,
                "hours": round(seconds / 3600, 2),
            }
        )

    return {
        "entry_count": len(items),
        "running_count": running_count,
        "total_hours": round(total_seconds / 3600, 2),
        "entries": items,
    }


def fetch_time_entries(
    day: date, timezone_name: str, token: str
) -> list[dict[str, Any]]:
    """Fetch one local day from Toggl Track API v9."""
    start_date, end_date = day_bounds_utc(day, timezone_name)
    query = urlencode(
        {"start_date": start_date, "end_date": end_date, "meta": "true"}
    )
    credentials = base64.b64encode(f"{token}:api_token".encode()).decode()
    request = Request(
        f"{API_BASE}/me/time_entries?{query}",
        headers={
            "Authorization": f"Basic {credentials}",
            "Accept": "application/json",
            "User-Agent": "PAL-daily-report/5.3",
        },
    )
    try:
        with urlopen(request, timeout=20) as response:
            payload = json.load(response)
    except HTTPError as exc:
        if exc.code in (401, 403):
            raise TogglTrackError(
                f"Toggl Track 认证失败（HTTP {exc.code}），请重新生成 API Token"
            ) from None
        raise TogglTrackError(f"Toggl Track API 返回 HTTP {exc.code}") from None
    except URLError as exc:
        raise TogglTrackError(
            f"无法连接 Toggl Track API：{type(exc.reason).__name__}"
        ) from None

    if not isinstance(payload, list):
        raise TogglTrackError("Toggl Track API 返回了非预期的数据结构")
    if len(payload) >= 1000:
        raise TogglTrackError("当日记录达到 API 1000 条上限，停止自动汇总")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize one Toggl Track day")
    parser.add_argument("--date", required=True, help="Local date, YYYY-MM-DD")
    parser.add_argument("--timezone", default="Asia/Shanghai")
    parser.add_argument("--dotenv", type=Path, default=Path.cwd() / ".env")
    args = parser.parse_args()

    try:
        target_date = date.fromisoformat(args.date)
        token = load_api_token(args.dotenv)
        entries = fetch_time_entries(target_date, args.timezone, token)
        print(
            json.dumps(
                {
                    "ok": True,
                    "date": args.date,
                    "timezone": args.timezone,
                    "data": summarize_entries(entries),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except (ValueError, TogglTrackError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
