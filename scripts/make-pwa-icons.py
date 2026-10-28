#!/usr/bin/env python3
"""Draw real OATutor home-screen icons as valid RGB PNGs.

The previous writer sliced each row as `width` bytes instead of `width * 3`,
so the files were truncated and compressed to a few hundred bytes.
"""

import os
import struct
import zlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public", "icons"))
FAVICON = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public", "favicon.png"))

NAVY = (31, 75, 110)
AMBER = (239, 159, 39)
WHITE = (255, 255, 255)
INK = (22, 48, 72)

# 5x7
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


def write_png(path, width, height, rgb):
    if len(rgb) != width * height * 3:
        raise ValueError(f"{path}: expected {width * height * 3} bytes, got {len(rgb)}")
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        raw.extend(rgb[y * stride : (y + 1) * stride])

    def chunk(tag, data):
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )
    with open(path, "wb") as handle:
        handle.write(png)


def blank(size, color):
    pixel = bytes(color)
    return bytearray(pixel * (size * size))


def set_px(buf, size, x, y, color):
    if 0 <= x < size and 0 <= y < size:
        i = (y * size + x) * 3
        buf[i : i + 3] = bytes(color)


def fill_circle(buf, size, cx, cy, radius, color):
    r2 = radius * radius
    x0 = max(0, int(cx - radius))
    x1 = min(size - 1, int(cx + radius))
    y0 = max(0, int(cy - radius))
    y1 = min(size - 1, int(cy + radius))
    for y in range(y0, y1 + 1):
        dy = y + 0.5 - cy
        for x in range(x0, x1 + 1):
            dx = x + 0.5 - cx
            if dx * dx + dy * dy <= r2:
                set_px(buf, size, x, y, color)


def draw_oa(buf, size, color, scale, origin_x, origin_y):
    glyph_w = 5
    gap = 1
    for index, letter in enumerate("OA"):
        glyph = GLYPHS[letter]
        gx = origin_x + index * (glyph_w + gap) * scale
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                if bit != "1":
                    continue
                for dy in range(scale):
                    for dx in range(scale):
                        set_px(buf, size, gx + col * scale + dx, origin_y + row * scale + dy, color)


def draw(size, maskable=False):
    buf = blank(size, NAVY)
    cx = cy = size / 2
    # Maskable icons are cropped to the center 80%. Keep the mark inside that.
    radius = size * (0.34 if maskable else 0.42)
    fill_circle(buf, size, cx, cy, radius, AMBER)
    fill_circle(buf, size, cx, cy, radius * 0.86, INK)

    glyph_w = 5
    gap = 1
    text_cols = glyph_w * 2 + gap
    scale = max(2, int(radius * 1.15 / text_cols))
    text_w = text_cols * scale
    text_h = 7 * scale
    draw_oa(
        buf,
        size,
        WHITE,
        scale,
        int(cx - text_w / 2),
        int(cy - text_h / 2),
    )
    return buf


def read_ihdr(path):
    with open(path, "rb") as handle:
        sig = handle.read(8)
        if sig != b"\x89PNG\r\n\x1a\n":
            raise ValueError(path + " is not a PNG")
        length = struct.unpack(">I", handle.read(4))[0]
        tag = handle.read(4)
        data = handle.read(length)
        if tag != b"IHDR":
            raise ValueError(path + " missing IHDR")
        width, height, bit_depth, color_type = struct.unpack(">IIBB", data[:10])
        return width, height, bit_depth, color_type, os.path.getsize(path)


def main():
    os.makedirs(ROOT, exist_ok=True)
    outputs = [
        (180, os.path.join(ROOT, "icon-180.png"), False),
        (192, os.path.join(ROOT, "icon-192.png"), False),
        (512, os.path.join(ROOT, "icon-512.png"), False),
        (512, os.path.join(ROOT, "icon-512-maskable.png"), True),
        (64, FAVICON, False),
    ]
    for size, path, maskable in outputs:
        write_png(path, size, size, draw(size, maskable))
        width, height, bit_depth, color_type, nbytes = read_ihdr(path)
        if (width, height, bit_depth, color_type) != (size, size, 8, 2):
            raise SystemExit(f"bad header for {path}: {width}x{height} depth {bit_depth} type {color_type}")
        print(f"{os.path.basename(path)} {width}x{height} {nbytes} bytes")


if __name__ == "__main__":
    main()
