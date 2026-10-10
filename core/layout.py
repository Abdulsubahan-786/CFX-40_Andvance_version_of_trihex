from __future__ import annotations

import math
from typing import Tuple

HEX_RADIUS = 12
COLUMNS = 100
DATA_OFFSET = 90
DATA_START_X = 180
DATA_START_Y = 180

X_STEP = HEX_RADIUS * 1.5
Y_STEP = HEX_RADIUS * math.sqrt(3)

FINDER_TL = (60, 60)
FINDER_TR = (DATA_START_X + (COLUMNS - 1) * X_STEP, 60)
FINDER_BL = (60, DATA_START_Y + 100 * Y_STEP)


def compute_rows(data_cells: int) -> int:
    return math.ceil(data_cells / COLUMNS)


def cell_position(row: int, col: int) -> Tuple[float, float]:
    x = DATA_START_X + col * X_STEP
    y = DATA_START_Y + row * Y_STEP
    if row % 2 == 1:
        x += X_STEP / 2
    return x, y


def image_size_for(rows: int) -> Tuple[int, int]:
    max_x = max(FINDER_TR[0], DATA_START_X + (COLUMNS - 1) * X_STEP)
    max_y = max(FINDER_BL[1], DATA_START_Y + (rows - 1) * Y_STEP)
    return int(max_x + 120), int(max_y + 120)
