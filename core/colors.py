from __future__ import annotations

from typing import Dict, Tuple

Color = Tuple[int, int, int]

COLORS: Dict[str, Color] = {
    "R": (255, 0, 0),
    "G": (0, 255, 0),
    "B": (0, 0, 255),
    "C": (0, 255, 255),
    "M": (255, 0, 255),
    "Y": (255, 255, 0),
    "K": (0, 0, 0),
    "W": (255, 255, 255),
}

COLOR_TO_BITS: Dict[str, str] = {
    "R": "000",
    "G": "001",
    "B": "010",
    "C": "011",
    "M": "100",
    "Y": "101",
    "K": "110",
    "W": "111",
}

BITS_TO_COLOR: Dict[str, str] = {value: key for key, value in COLOR_TO_BITS.items()}

TARGET_COLORS: Dict[str, Tuple[int, int, int]] = COLORS


def nearest_color(rgb: Tuple[int, int, int] | list[int]) -> str:
    """Return the nearest palette color for an RGB triplet."""
    rgb_values = tuple(rgb)
    best_name = "W"
    best_distance = float("inf")

    for name, target in TARGET_COLORS.items():
        distance = sum((a - b) ** 2 for a, b in zip(rgb_values, target)) ** 0.5
        if distance < best_distance:
            best_distance = distance
            best_name = name

    return best_name
