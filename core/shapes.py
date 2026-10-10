from __future__ import annotations

import math
from typing import Iterable, List, Tuple

from PIL import ImageDraw

from .colors import COLORS

Point = Tuple[float, float]


def hex_points(cx: float, cy: float, radius: float) -> List[Point]:
    points: List[Point] = []
    for angle in range(0, 360, 60):
        radians = math.radians(angle)
        points.append((cx + radius * math.cos(radians), cy + radius * math.sin(radians)))
    return points


def draw_hex(draw: ImageDraw.ImageDraw, cx: float, cy: float, radius: float, color_name: str) -> None:
    draw.polygon(hex_points(cx, cy, radius), fill=COLORS[color_name])


def draw_finder(draw: ImageDraw.ImageDraw, cx: float, cy: float, radius: float) -> None:
    """Draw the unique CFX-40 finder pattern."""
    positions = [
        (0, -2, "K"),
        (-1, -1, "W"),
        (0, -1, "K"),
        (1, -1, "W"),
        (-2, 0, "K"),
        (-1, 0, "W"),
        (0, 0, "K"),
        (1, 0, "W"),
        (2, 0, "K"),
        (-1, 1, "W"),
        (0, 1, "K"),
        (1, 1, "W"),
        (0, 2, "K"),
    ]

    x_step = radius * 1.5
    y_step = radius * math.sqrt(3)

    for dx, dy, color_name in positions:
        draw_hex(draw, cx + dx * x_step, cy + dy * y_step, radius, color_name)
