#!/usr/bin/env python3
"""Draw simple OATutor home-screen icons. No third-party image library."""

import os
import struct
import zlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public", "icons"))

# 5x7 bitmaps
GLYPHS = {
    "O": [
        "01110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ],
    "A": [
        "01110",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001",
    ],
}


def write_png(path, width, height, pixels):
    raw = bytearray()
    for y in range(height):
        raw.append(0)
        raw.extend(pixels[y * width : (y + 1) * width])
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")
    with open(path, "wb") as handle:
        handle.write(png)


def draw(size, maskable=False):
    navy = (31, 75, 110)
    white = (255, 255, 255)
    pixels = bytearray()
    # Keep the mark inside the center 60% so a maskable crop still shows it.
    margin = int(size * (0.22 if maskable else 0.12))
    for y in range(size):
        for x in range(size):
            pixels.extend(navy)
    glyph_h = 7
    glyph_w = 5
    gap = 1
    text_w = glyph_w * 2 + gap
    scale = max(1, int((size - margin * 2) / (text_w + 2)))
    origin_x = (size - text_w * scale) // 2
    origin_y = (size - glyph_h * scale) // 2
    for index, letter in enumerate("OA"):
        glyph = GLYPHS[letter]
        gx = origin_x + index * (glyph_w + gap) * scale
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                if bit != "1":
                    continue
                for dy in range(scale):
                    for dx in range(scale):
                        px = gx + col * scale + dx
                        py = origin_y + row * scale + dy
                        if 0 <= px < size and 0 <= py < size:
                            start = (py * size + px) * 3
                            pixels[start:start + 3] = bytes(white)
    return pixels


def main():
    os.makedirs(ROOT, exist_ok=True)
    for size, name, maskable in (
        (180, "icon-180.png", False),
        (192, "icon-192.png", False),
        (512, "icon-512.png", False),
        (512, "icon-512-maskable.png", True),
    ):
        write_png(os.path.join(ROOT, name), size, size, draw(size, maskable))
        print(name)


if __name__ == "__main__":
    main()
