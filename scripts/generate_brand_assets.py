"""
Genera PNG raster assets de marca desde primitives PIL.

Los SVG vectoriales son la fuente canónica para la web; los PNG son
fallbacks necesarios (favicon en browsers viejos, Apple touch icon,
LinkedIn profile picture, Open Graph share image).

Uso:
    python -m scripts.generate_brand_assets

Genera:
    assets/brand/favicon-16.png
    assets/brand/favicon-32.png
    assets/brand/favicon-48.png
    assets/brand/apple-touch-icon.png   (180x180)
    assets/brand/logo-square.png        (400x400, LinkedIn profile)
    assets/brand/og-default.png         (1200x630, Open Graph share)
"""
from __future__ import annotations
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "assets" / "brand"
BRAND.mkdir(parents=True, exist_ok=True)

# Fuentes locales descargadas en /tmp
FRAUNCES = Path("/tmp/Fraunces.ttf")
INTER = Path("/tmp/Inter.ttf")

# Paleta (coincide con assets/radar.css)
NAVY = (13, 27, 46)         # #0d1b2e fondo principal
CREAM = (250, 248, 244)     # #faf8f4 texto principal
ACCENT_GOLD = (201, 168, 76)# #c9a84c acento dorado
TEXT_MID = (61, 67, 81)     # #3d4351 cuerpo secundario


def _font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def _rounded_square(size: int, radius: int, fill: tuple) -> Image.Image:
    """Cuadrado con esquinas redondeadas. Anti-aliased."""
    scale = 4
    big = Image.new("RGBA", (size * scale, size * scale), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    d.rounded_rectangle(
        [(0, 0), (size * scale - 1, size * scale - 1)],
        radius=radius * scale,
        fill=fill + (255,),
    )
    return big.resize((size, size), Image.LANCZOS)


def _draw_radar_arc(draw: ImageDraw.ImageDraw, cx: int, cy: int, base_r: int,
                    color: tuple, width: int = 2):
    """Dibuja un radar concéntrico tipo onda con un punto central."""
    # Círculos concéntricos
    for i, r in enumerate([base_r * 0.45, base_r * 0.85, base_r * 1.25]):
        alpha = int(255 * (1 - i * 0.25))
        # PIL draw no acepta alpha por color en ellipse, así que dibujamos
        # con color sólido y ya se gestiona por capas si quisiéramos.
        draw.ellipse(
            [(cx - r, cy - r), (cx + r, cy + r)],
            outline=color, width=width,
        )
    # Punto central
    dot_r = max(2, base_r * 0.15)
    draw.ellipse(
        [(cx - dot_r, cy - dot_r), (cx + dot_r, cy + dot_r)],
        fill=color,
    )


def make_favicon(size: int) -> Image.Image:
    """Favicon F sobre cuadrado navy redondeado con radar acento dorado."""
    radius = max(2, int(size * 0.16))
    img = _rounded_square(size, radius, NAVY)
    draw = ImageDraw.Draw(img)

    # Letra F en Fraunces, centrada
    # Tamaño relativo: ~70% del lado para máxima legibilidad
    font_size = int(size * 0.72)
    font = _font(FRAUNCES, font_size)
    # Activar variación (Bold/Black) si la fuente es variable
    try:
        font.set_variation_by_axes([900])  # weight axis to 900 (Black)
    except Exception:
        pass

    text = "F"
    # Bbox para centrar bien (Fraunces tiene cierto descender en la "F")
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size - tw) / 2 - bbox[0]
    ty = (size - th) / 2 - bbox[1] * 1.0
    # Ajuste fino: subir ligeramente la letra
    ty -= size * 0.02
    draw.text((tx, ty), text, font=font, fill=CREAM)

    # Radar acento dorado, esquina inferior derecha
    if size >= 32:  # solo si hay espacio
        radar_cx = int(size * 0.78)
        radar_cy = int(size * 0.78)
        radar_r = int(size * 0.10)
        # Para size pequeños, simplificar: solo un círculo + punto
        if size <= 48:
            stroke = max(1, int(size * 0.045))
            draw.ellipse(
                [(radar_cx - radar_r, radar_cy - radar_r),
                 (radar_cx + radar_r, radar_cy + radar_r)],
                outline=ACCENT_GOLD, width=stroke,
            )
            dot_r = max(1, int(size * 0.04))
            draw.ellipse(
                [(radar_cx - dot_r, radar_cy - dot_r),
                 (radar_cx + dot_r, radar_cy + dot_r)],
                fill=ACCENT_GOLD,
            )
        else:
            _draw_radar_arc(draw, radar_cx, radar_cy, radar_r,
                            ACCENT_GOLD, width=max(2, int(size * 0.025)))
    return img


def make_apple_touch_icon() -> Image.Image:
    """180x180 Apple touch icon (sin esquinas redondeadas; iOS las añade)."""
    size = 180
    img = Image.new("RGBA", (size, size), NAVY + (255,))
    draw = ImageDraw.Draw(img)

    # F grande
    font = _font(FRAUNCES, 130)
    try:
        font.set_variation_by_axes([900])
    except Exception:
        pass
    text = "F"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size - tw) / 2 - bbox[0]
    ty = (size - th) / 2 - bbox[1]
    ty -= 6
    draw.text((tx, ty), text, font=font, fill=CREAM)

    # Radar
    _draw_radar_arc(draw, 142, 142, 20, ACCENT_GOLD, width=3)
    return img


def make_logo_square() -> Image.Image:
    """400x400 logo cuadrado para LinkedIn / avatar redes."""
    size = 400
    img = Image.new("RGBA", (size, size), NAVY + (255,))
    draw = ImageDraw.Draw(img)

    # F grande
    font_big = _font(FRAUNCES, 280)
    try:
        font_big.set_variation_by_axes([900])
    except Exception:
        pass
    text = "F"
    bbox = draw.textbbox((0, 0), text, font=font_big)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size - tw) / 2 - bbox[0]
    # Centrar ligeramente arriba del centro real (para dejar espacio al wordmark)
    ty = 60 - bbox[1]
    draw.text((tx, ty), text, font=font_big, fill=CREAM)

    # Radar a la derecha
    _draw_radar_arc(draw, 320, 250, 28, ACCENT_GOLD, width=4)

    # Wordmark abajo
    font_brand = _font(FRAUNCES, 26)
    try:
        font_brand.set_variation_by_axes([700])
    except Exception:
        pass
    brand_text = "The Fleet Radar"
    bbox = draw.textbbox((0, 0), brand_text, font=font_brand)
    bw = bbox[2] - bbox[0]
    draw.text(((size - bw) / 2 - bbox[0], 330), brand_text,
              font=font_brand, fill=CREAM)

    font_sub = _font(INTER, 13)
    try:
        font_sub.set_variation_by_axes([600])
    except Exception:
        pass
    sub_text = "B Y · P U L P O"
    bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
    sw = bbox[2] - bbox[0]
    draw.text(((size - sw) / 2 - bbox[0], 365), sub_text,
              font=font_sub, fill=ACCENT_GOLD)

    return img


def make_og_default() -> Image.Image:
    """1200x630 Open Graph image. Reemplaza al og-default.png genérico."""
    w, h = 1200, 630
    img = Image.new("RGBA", (w, h), NAVY + (255,))
    draw = ImageDraw.Draw(img)

    # Grid sutil de fondo
    grid_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    grid_draw = ImageDraw.Draw(grid_layer)
    for x in range(0, w, 80):
        grid_draw.line([(x, 0), (x, h)], fill=(255, 255, 255, 8), width=1)
    for y in range(0, h, 80):
        grid_draw.line([(0, y), (w, y)], fill=(255, 255, 255, 8), width=1)
    img = Image.alpha_composite(img, grid_layer)
    draw = ImageDraw.Draw(img)

    # Bloque F (izquierda)
    block_size = 320
    block_x = 88
    block_y = (h - block_size) // 2
    block = _rounded_square(block_size, 22, NAVY)
    # Borde dorado
    block_draw = ImageDraw.Draw(block)
    block_draw.rounded_rectangle(
        [(2, 2), (block_size - 3, block_size - 3)],
        radius=22, outline=ACCENT_GOLD, width=3,
    )
    # F dentro del bloque
    font_f = _font(FRAUNCES, 220)
    try:
        font_f.set_variation_by_axes([900])
    except Exception:
        pass
    bbox = block_draw.textbbox((0, 0), "F", font=font_f)
    fw = bbox[2] - bbox[0]
    fh = bbox[3] - bbox[1]
    block_draw.text(
        ((block_size - fw) / 2 - bbox[0], (block_size - fh) / 2 - bbox[1] - 10),
        "F", font=font_f, fill=CREAM,
    )
    # Radar mini dentro del bloque
    _draw_radar_arc(block_draw, block_size - 50, block_size - 50, 22,
                    ACCENT_GOLD, width=3)

    img.paste(block, (block_x, block_y), block)

    # Wordmark + tagline (derecha)
    text_x = block_x + block_size + 64

    # Eyebrow
    font_eye = _font(INTER, 18)
    try:
        font_eye.set_variation_by_axes([600])
    except Exception:
        pass
    draw.text((text_x, 195), "P U B L I C A C I Ó N   S E M A N A L",
              font=font_eye, fill=ACCENT_GOLD)

    # Brand
    font_brand = _font(FRAUNCES, 76)
    try:
        font_brand.set_variation_by_axes([800])
    except Exception:
        pass
    draw.text((text_x, 225), "The Fleet Radar",
              font=font_brand, fill=CREAM)

    # Tagline
    font_tag = _font(INTER, 22)
    try:
        font_tag.set_variation_by_axes([400])
    except Exception:
        pass
    draw.text((text_x, 340), "Inteligencia semanal de gestión",
              font=font_tag, fill=(250, 248, 244, 178))
    draw.text((text_x, 372), "de flotas en MX, ES, LatAm, USA y EU.",
              font=font_tag, fill=(250, 248, 244, 178))

    # Footer brand
    font_foot = _font(INTER, 14)
    try:
        font_foot.set_variation_by_axes([700])
    except Exception:
        pass
    draw.text((text_x, 435), "B Y · P U L P O",
              font=font_foot, fill=ACCENT_GOLD)

    return img


# ─── Run ───

def main():
    print(f"Fuentes cargadas: Fraunces={FRAUNCES.exists()}, Inter={INTER.exists()}")

    print("\nGenerando favicons…")
    for size in [16, 32, 48]:
        img = make_favicon(size)
        out = BRAND / f"favicon-{size}.png"
        img.save(out, "PNG", optimize=True)
        print(f"  ✓ {out.relative_to(ROOT)}  ({size}x{size})")

    print("\nGenerando Apple touch icon…")
    img = make_apple_touch_icon()
    out = BRAND / "apple-touch-icon.png"
    img.save(out, "PNG", optimize=True)
    print(f"  ✓ {out.relative_to(ROOT)}  (180x180)")

    print("\nGenerando logo cuadrado (LinkedIn)…")
    img = make_logo_square()
    out = BRAND / "logo-square.png"
    img.save(out, "PNG", optimize=True)
    print(f"  ✓ {out.relative_to(ROOT)}  (400x400)")

    print("\nGenerando OG default (1200x630)…")
    img = make_og_default()
    out = BRAND / "og-default.png"
    img.save(out, "PNG", optimize=True)
    print(f"  ✓ {out.relative_to(ROOT)}  (1200x630)")

    # Sobrescribir el og-default.png antiguo en raíz también
    out_root = ROOT / "og-default.png"
    img.save(out_root, "PNG", optimize=True)
    print(f"  ✓ {out_root.relative_to(ROOT)}  (1200x630, raíz para compat)")

    print("\n✅ Brand assets generados.")


if __name__ == "__main__":
    sys.exit(main() or 0)
