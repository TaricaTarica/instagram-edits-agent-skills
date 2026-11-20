#!/usr/bin/env python3
"""Draw Instagram Reels UI safe zones on a frame so collisions are easy to spot.

Usage: python3 safe_zone_overlay.py <frame.png|jpg> <out.png>

Zones are defined at 1080x1920 and scaled to the frame's size. Requires Pillow.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

REFERENCE_WIDTH = 1080
REFERENCE_HEIGHT = 1920
EXPECTED_ASPECT = 9 / 16
ASPECT_TOLERANCE = 0.02


class ZoneKind(Enum):
    BLOCKED = "blocked"
    CAUTION = "caution"


@dataclass(frozen=True)
class Zone:
    label: str
    kind: ZoneKind
    left: int
    top: int
    right: int
    bottom: int


REELS_ZONES: tuple[Zone, ...] = (
    Zone("header", ZoneKind.BLOCKED, 0, 0, 1080, 210),
    Zone("action rail", ZoneKind.BLOCKED, 980, 210, 1080, 1580),
    Zone("caption + audio + buttons", ZoneKind.BLOCKED, 0, 1580, 1080, 1920),
    Zone("long caption expands", ZoneKind.CAUTION, 0, 1500, 1080, 1580),
)

ZONE_COLORS = {
    ZoneKind.BLOCKED: (255, 40, 40, 90),
    ZoneKind.CAUTION: (255, 200, 0, 70),
}


@dataclass(frozen=True)
class Result:
    ok: bool
    message: str


def scale_zone(zone: Zone, width: int, height: int) -> tuple[int, int, int, int]:
    sx = width / REFERENCE_WIDTH
    sy = height / REFERENCE_HEIGHT
    return (round(zone.left * sx), round(zone.top * sy), round(zone.right * sx), round(zone.bottom * sy))


def is_vertical_reel(width: int, height: int) -> bool:
    return abs(width / height - EXPECTED_ASPECT) <= ASPECT_TOLERANCE


def draw_overlay(source: Path, target: Path) -> Result:
    try:
        from PIL import Image, ImageDraw
    except ImportError as error:
        return Result(False, f"Pillow unavailable ({error}); install with: python3 -m pip install pillow")

    if not source.is_file():
        return Result(False, f"frame not found: {source}")

    frame = Image.open(source).convert("RGBA")
    width, height = frame.size
    if not is_vertical_reel(width, height):
        return Result(False, f"frame is {width}x{height}, not 9:16; zones would be wrong")

    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for zone in REELS_ZONES:
        box = scale_zone(zone, width, height)
        draw.rectangle(box, fill=ZONE_COLORS[zone.kind], outline=(255, 255, 255, 160))
        draw.text((box[0] + 8, box[1] + 6), zone.label, fill=(255, 255, 255, 230))

    Image.alpha_composite(frame, layer).convert("RGB").save(target)
    return Result(True, f"overlay written: {target}")


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__.strip())
        return 2

    result = draw_overlay(Path(argv[1]), Path(argv[2]))
    print(result.message)
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
