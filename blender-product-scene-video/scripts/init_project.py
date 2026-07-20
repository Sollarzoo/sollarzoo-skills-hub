#!/usr/bin/env python3
"""Initialize a versionable Blender product-scene workspace."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DIRECTORIES = (
    "assets/models",
    "assets/textures",
    "assets/screen-recordings",
    "assets/references",
    "Blender/backups",
    "previews",
    "exports/frames",
    "exports/videos",
    "logs",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--name", required=True, help="Stable scene slug, e.g. SC01-phone-diary")
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--duration", type=float, default=5.0, help="Seconds")
    args = parser.parse_args()

    if args.width <= 0 or args.height <= 0 or args.fps <= 0 or args.duration <= 0:
        parser.error("width, height, fps, and duration must be positive")

    root = args.project_dir.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    for relative in DIRECTORIES:
        (root / relative).mkdir(parents=True, exist_ok=True)

    total_frames = round(args.duration * args.fps)
    manifest = {
        "scene": args.name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_assets_are_immutable": True,
        "output": {
            "width": args.width,
            "height": args.height,
            "fps": args.fps,
            "duration_seconds": args.duration,
            "frame_start": 1,
            "frame_end": total_frames,
            "expected_frame_count": total_frames,
        },
        "status": "initialized",
    }
    manifest_path = root / "scene_manifest.json"
    if manifest_path.exists():
        raise SystemExit(f"Refusing to overwrite existing manifest: {manifest_path}")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
