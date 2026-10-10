from __future__ import annotations

RADIX40_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ .-_*"


def encode_radix40(text: str) -> list[int]:
    """Encode a short ASCII text string into a list of Radix-40 values."""
    values: list[int] = []
    for char in text.upper():
        try:
            values.append(RADIX40_CHARS.index(char))
        except ValueError:
            values.append(RADIX40_CHARS.index("_"))

    if not values:
        return []

    encoded: list[int] = []
    for i in range(0, len(values), 3):
        block = values[i : i + 3]
        while len(block) < 3:
            block.append(0)
        encoded.append(block[0])
        encoded.append(block[1])
        encoded.append(block[2])
    return encoded


def decode_radix40(values: list[int]) -> str:
    """Decode a Radix-40 list back into ASCII text."""
    chars: list[str] = []
    for index in range(0, len(values), 3):
        values_slice = values[index : index + 3]
        if len(values_slice) < 3:
            values_slice = values_slice + [0] * (3 - len(values_slice))
        for value in values_slice:
            if value < 0 or value >= len(RADIX40_CHARS):
                value = 0
            chars.append(RADIX40_CHARS[value])
    return "".join(chars).strip()
