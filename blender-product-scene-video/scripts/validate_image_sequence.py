#!/usr/bin/env python3
"""Validate numbered JPEG/PNG frames without third-party dependencies."""

from __future__ import annotations

import argparse
import re
import struct
from collections import Counter
from pathlib import Path


FRAME_RE = re.compile(r"(\d+)(?=\.(?:jpe?g|png)$)", re.IGNORECASE)


def image_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        head = handle.read(24)
        if head.startswith(b"\x89PNG\r\n\x1a\n"):
            return struct.unpack(">II", head[16:24])
        if head[:2] != b"\xff\xd8":
            raise ValueError("unsupported image signature")
        handle.seek(2)
        while True:
            marker_start = handle.read(1)
            if not marker_start:
                raise ValueError("JPEG size marker not found")
            if marker_start != b"\xff":
                continue
            marker = handle.read(1)
            while marker == b"\xff":
                marker = handle.read(1)
            if marker in {bytes([value]) for value in range(0xC0, 0xC4)} | {
                bytes([value]) for value in range(0xC5, 0xC8)
            } | {bytes([value]) for value in range(0xC9, 0xCC)} | {
                bytes([value]) for value in range(0xCD, 0xD0)
            }:
                handle.read(3)
                height, width = struct.unpack(">HH", handle.read(4))
                return width, height
            length_raw = handle.read(2)
            if len(length_raw) != 2:
                raise ValueError("truncated JPEG")
            length = struct.unpack(">H", length_raw)[0]
            handle.seek(length - 2, 1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("frames_dir", type=Path)
    parser.add_argument("--expected-count", type=int)
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    args = parser.parse_args()

    files = sorted(
        path for path in args.frames_dir.expanduser().glob("*")
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )
    errors: list[str] = []
    indexed: list[tuple[int, Path]] = []
    for path in files:
        match = FRAME_RE.search(path.name)
        if not match:
            errors.append(f"missing numeric frame suffix: {path.name}")
            continue
        indexed.append((int(match.group(1)), path))

    numbers = [number for number, _ in indexed]
    duplicates = sorted(number for number, count in Counter(numbers).items() if count > 1)
    if duplicates:
        errors.append(f"duplicate frame numbers: {duplicates[:20]}")
    if args.expected_count is not None and len(files) != args.expected_count:
        errors.append(f"count {len(files)} != expected {args.expected_count}")

    if args.start is not None or args.end is not None:
        start = args.start if args.start is not None else min(numbers, default=0)
        end = args.end if args.end is not None else max(numbers, default=-1)
        missing = sorted(set(range(start, end + 1)) - set(numbers))
        if missing:
            errors.append(f"missing frames: {missing[:20]}{'...' if len(missing) > 20 else ''}")
    elif numbers:
        missing = sorted(set(range(min(numbers), max(numbers) + 1)) - set(numbers))
        if missing:
            errors.append(f"internal gaps: {missing[:20]}{'...' if len(missing) > 20 else ''}")

    expected_size = None
    if args.width is not None and args.height is not None:
        expected_size = (args.width, args.height)
    sample_paths = [path for _, path in indexed]
    if len(sample_paths) > 12:
        positions = {round(i * (len(sample_paths) - 1) / 11) for i in range(12)}
        sample_paths = [sample_paths[i] for i in sorted(positions)]
    observed_sizes: set[tuple[int, int]] = set()
    for path in sample_paths:
        try:
            size = image_size(path)
            observed_sizes.add(size)
            if expected_size and size != expected_size:
                errors.append(f"{path.name}: size {size} != expected {expected_size}")
        except ValueError as exc:
            errors.append(f"{path.name}: {exc}")

    print(
        f"frames={len(files)} range="
        f"{min(numbers, default='n/a')}-{max(numbers, default='n/a')} "
        f"sizes={sorted(observed_sizes)}"
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: image sequence is continuous and valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
