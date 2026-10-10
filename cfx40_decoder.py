from __future__ import annotations

import os
import struct
from pathlib import Path

import cv2
import numpy as np

from core.colors import COLOR_TO_BITS, TARGET_COLORS
from core.layout import COLUMNS, DATA_START_X, DATA_START_Y, X_STEP, Y_STEP

PROJECT_ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = PROJECT_ROOT.parent
MAGIC = b"CFX40"


def resolve_path(path_value: str) -> Path:
    candidate = Path(path_value).expanduser()
    if candidate.is_absolute():
        return candidate

    candidates = [
        Path.cwd() / candidate,
        PROJECT_ROOT / candidate,
        WORKSPACE_ROOT / candidate,
    ]
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


def nearest_color(rgb: tuple[int, int, int] | list[int]) -> str:
    color_values = np.array(rgb, dtype=float)
    best_name = "W"
    best_distance = float("inf")
    for name, target in TARGET_COLORS.items():
        target_values = np.array(target, dtype=float)
        distance = np.linalg.norm(color_values - target_values)
        if distance < best_distance:
            best_distance = distance
            best_name = name
    return best_name


def sample_color(image_rgb: np.ndarray, cx: float, cy: float, width: int, height: int) -> str | None:
    radius = 4
    x1 = max(0, int(cx - radius))
    x2 = min(width, int(cx + radius + 1))
    y1 = max(0, int(cy - radius))
    y2 = min(height, int(cy + radius + 1))
    region = image_rgb[y1:y2, x1:x2]
    if region.size == 0:
        return None
    average = np.mean(region.reshape(-1, 3), axis=0)
    return nearest_color(tuple(int(v) for v in average))


def decode_image(image_path: str, output_dir: str | None = None) -> str:
    image_file = resolve_path(image_path)
    if not image_file.exists():
        raise FileNotFoundError(f"File not found: {image_file}")

    image = cv2.imread(str(image_file))
    if image is None:
        raise ValueError(f"Could not open image: {image_path}")

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width = image.shape[:2]

    color_sequence: list[str] = []
    max_rows = int((height - DATA_START_Y) / Y_STEP) + 1

    for row in range(max_rows):
        for col in range(COLUMNS):
            x = DATA_START_X + col * X_STEP
            y = DATA_START_Y + row * Y_STEP
            if row % 2 == 1:
                x += X_STEP / 2
            if x < 0 or x >= width or y < 0 or y >= height:
                continue
            color = sample_color(image_rgb, x, y, width, height)
            if color is not None:
                color_sequence.append(color)

    binary = "".join(COLOR_TO_BITS[color] for color in color_sequence)
    binary = binary[: len(binary) - (len(binary) % 8)]

    raw = bytearray(int(binary[i:i + 8], 2) for i in range(0, len(binary), 8))
    header_index = raw.find(MAGIC)
    if header_index == -1:
        raise ValueError("CFX40 magic header not found. The geometry/color sampling is still incorrect.")

    position = header_index + len(MAGIC)
    version = raw[position]
    position += 1
    file_size = struct.unpack(">Q", raw[position:position + 8])[0]
    position += 8
    name_length = struct.unpack(">H", raw[position:position + 2])[0]
    position += 2
    file_name = raw[position:position + name_length].decode("utf-8")
    position += name_length
    file_data = raw[position:position + file_size]

    target_dir = Path(output_dir).expanduser() if output_dir else PROJECT_ROOT / "output"
    if not target_dir.is_absolute():
        target_dir = PROJECT_ROOT / target_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    out_path = str(target_dir / file_name)
    with open(out_path, "wb") as handle:
        handle.write(file_data)

    print("CFX-40 Decoder")
    print(f"Image: {image_path}")
    print(f"Detected cells: {len(color_sequence)}")
    print(f"Header found at: {header_index}")
    print(f"Recovered file: {file_name}")
    print(f"Recovered size: {len(file_data)} bytes")
    print(f"Output: {out_path}")
    return out_path


if __name__ == "__main__":
    image_input = input("Enter CFX-40 image: ").strip()
    decode_image(image_input)
