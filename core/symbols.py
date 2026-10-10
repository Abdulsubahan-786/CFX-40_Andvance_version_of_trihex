from __future__ import annotations

from .colors import BITS_TO_COLOR, COLOR_TO_BITS


def bits_to_symbol(bits: str) -> str:
    return BITS_TO_COLOR[bits]


def symbol_to_bits(symbol: str) -> str:
    return COLOR_TO_BITS[symbol]


def sequence_to_binary(color_sequence: list[str]) -> str:
    return "".join(COLOR_TO_BITS[color] for color in color_sequence)


def binary_to_sequence(binary: str) -> list[str]:
    if len(binary) % 3 != 0:
        binary = binary[: len(binary) - (len(binary) % 3)]
    return [BITS_TO_COLOR[binary[i : i + 3]] for i in range(0, len(binary), 3)]
