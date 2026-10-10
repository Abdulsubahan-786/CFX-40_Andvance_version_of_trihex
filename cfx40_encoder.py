from __future__ import annotations

import os
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from core.colors import COLORS, BITS_TO_COLOR
from core.layout import COLUMNS, DATA_START_X, DATA_START_Y, HEX_RADIUS, X_STEP, Y_STEP, compute_rows, image_size_for
from core.shapes import draw_finder, draw_hex

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


def build_payload(file_path: str) -> tuple[bytes, str, int, int]:
    with open(file_path, "rb") as handle:
        file_data = handle.read()

    file_size = len(file_data)
    file_name = os.path.basename(file_path)
    name_bytes = file_name.encode("utf-8")

    payload = (
        MAGIC +
        struct.pack(">B", 1) +
        struct.pack(">Q", file_size) +
        struct.pack(">H", len(name_bytes)) +
        name_bytes +
        file_data
    )
    return payload, file_name, file_size, len(name_bytes)


def encode_file(file_path: str, output_path: str | None = None) -> str:
    source_path = resolve_path(file_path)
    if not source_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    payload, file_name, file_size, _ = build_payload(str(source_path))
    binary = "".join(f"{byte:08b}" for byte in payload)
    padding = (3 - len(binary) % 3) % 3
    binary += "0" * padding

    sequence = [BITS_TO_COLOR[binary[i:i + 3]] for i in range(0, len(binary), 3)]
    data_cells = len(sequence)
    rows = compute_rows(data_cells)

    width, height = image_size_for(rows)
    image = Image.new("RGB", (width, height), COLORS["W"])
    draw = ImageDraw.Draw(image)

    finder_positions = [(60, 60), (DATA_START_X + (COLUMNS - 1) * X_STEP, 60), (60, DATA_START_Y + (rows - 1) * Y_STEP)]
    for fx, fy in finder_positions:
        draw_finder(draw, fx, fy, HEX_RADIUS)

    index = 0
    for row in range(rows):
        for col in range(COLUMNS):
            if index >= data_cells:
                break
            x, y = DATA_START_X + col * X_STEP, DATA_START_Y + row * Y_STEP
            if row % 2 == 1:
                x += X_STEP / 2
            draw_hex(draw, x, y, HEX_RADIUS, sequence[index])
            index += 1

    metadata = f"CFX40 | ROWS={rows} | COLS={COLUMNS} | CELLS={data_cells}"
    draw.text((20, height - 35), metadata, fill=COLORS["K"])

    resolved_output = Path(output_path).expanduser() if output_path else PROJECT_ROOT / "output" / f"cfx40_{os.path.basename(file_name)}.png"
    if not resolved_output.is_absolute():
        resolved_output = PROJECT_ROOT / resolved_output
    output_dir = resolved_output.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    image.save(str(resolved_output), "PNG")

    target = str(resolved_output)

    print("CFX-40 Encoder")
    print(f"Input: {file_name}")
    print(f"File size: {file_size} bytes")
    print(f"Data cells: {data_cells}")
    print(f"Rows: {rows}")
    print(f"Output: {target}")
    return target


if __name__ == "__main__":
    target_path = input("Enter file to encode: ").strip()
    encode_file(target_path)
