"""Build the social carousel for the AFL competitive-balance article.

The published article charts are treated as immutable source assets. This
script places the selected charts, without cropping or distortion, into a
consistent 4:5 social-media layout and adds a summary slide.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "images" / "afl-competitive-balance"
OUTPUT_DIR = SOURCE_DIR / "carousel"

WIDTH = 1080
HEIGHT = 1350
BACKGROUND = "#F8FAFC"
NAVY = "#0F172A"
SLATE = "#52627A"
TEAL = "#21839B"
TEAL_DARK = "#176B7D"
TEAL_PALE = "#D7EDF2"
PURPLE = "#7C3AED"
PURPLE_PALE = "#EDE4FF"
AMBER = "#DF7A00"
WHITE = "#FFFFFF"
RULE = "#D9E2EC"

FONT_DIR = Path("C:/Windows/Fonts")
FONT_REGULAR = FONT_DIR / "segoeui.ttf"
FONT_SEMIBOLD = FONT_DIR / "seguisb.ttf"
FONT_BOLD = FONT_DIR / "segoeuib.ttf"


@dataclass(frozen=True)
class ChartSlide:
    filename: str
    section: str
    headline: str
    takeaway: str | None
    accent: str


SLIDES = (
    ChartSlide(
        "team-strength-spread.png",
        "EVENNESS",
        "The competition tightened in the 1990s, but the spread widened again in the 2000s.",
        "The AFL was at its most even between 1995 and 2008, but since then the spread between the top and bottom teams within each season has opened up.",
        TEAL,
    ),
    ChartSlide(
        "top-bottom-strength-gaps.png",
        "EVENNESS",
        "Recent seasons look close among leading teams while the weakest sides sit further from the middle.",
        None,
        TEAL,
    ),
    ChartSlide(
        "team-strength-persistence.png",
        "MOBILITY",
        "Team performance is now more consistent across seasons.",
        "Team strength is more strongly correlated across one-, two- and three-season intervals in 2008–2026, signalling lower mobility.",
        PURPLE,
    ),
    ChartSlide(
        "team-strength-tercile-transitions.png",
        "MOBILITY",
        "Moving between tiers\nhas become harder.",
        None,
        PURPLE,
    ),
    ChartSlide(
        "team-strength-retention.png",
        "MOBILITY",
        "Top teams are staying up for longer, bottom teams are staying down for longer.",
        "Since around 2000, top and bottom teams have become increasingly likely to stay in their tier.",
        PURPLE,
    ),
    ChartSlide(
        "premiership-grand-final-concentration.png",
        "OUTCOMES",
        "The AFL is still more even than the old VFL.",
        "In the 1970s and 1980s, VFL premierships were dominated by a few teams. Overall, the AFL era has been more even.",
        AMBER,
    )
)

TOTAL_SLIDES = len(SLIDES) + 1


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.exists():
        raise FileNotFoundError(f"Required font not found: {path}")
    return ImageFont.truetype(str(path), size=size)


def rounded_rectangle(
    image: Image.Image,
    box: tuple[int, int, int, int],
    *,
    radius: int,
    fill: str,
    shadow: bool = False,
) -> None:
    if shadow:
        layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        layer_draw = ImageDraw.Draw(layer)
        x0, y0, x1, y1 = box
        layer_draw.rounded_rectangle(
            (x0 + 2, y0 + 10, x1 + 2, y1 + 10),
            radius=radius,
            fill=(15, 23, 42, 35),
        )
        layer = layer.filter(ImageFilter.GaussianBlur(12))
        image.alpha_composite(layer)
    ImageDraw.Draw(image).rounded_rectangle(box, radius=radius, fill=fill)


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    selected_font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if draw.textbbox((0, 0), candidate, font=selected_font)[2] <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_lines(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    lines: Iterable[str],
    *,
    selected_font: ImageFont.FreeTypeFont,
    fill: str,
    spacing: int,
) -> int:
    x, y = xy
    ascent, descent = selected_font.getmetrics()
    line_height = ascent + descent
    for line in lines:
        draw.text((x, y), line, font=selected_font, fill=fill)
        y += line_height + spacing
    return y


def draw_footer(draw: ImageDraw.ImageDraw, number: int) -> None:
    draw.line((58, 1291, WIDTH - 58, 1291), fill=RULE, width=2)
    footer_font = font(FONT_REGULAR, 22)
    draw.text((58, 1306), "nealhughes.net  •  AFL competitive balance", font=footer_font, fill=SLATE)
    number_text = f"{number:02d} / {TOTAL_SLIDES:02d}"
    box = draw.textbbox((0, 0), number_text, font=footer_font)
    draw.text((WIDTH - 58 - (box[2] - box[0]), 1306), number_text, font=footer_font, fill=SLATE)


def draw_brand_mark(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw.rounded_rectangle((x, y, x + 72, y + 12), radius=6, fill=TEAL)
    draw.rounded_rectangle((x + 80, y, x + 132, y + 12), radius=6, fill=PURPLE)
    draw.rounded_rectangle((x + 140, y, x + 174, y + 12), radius=6, fill=AMBER)


def make_cover() -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)

    # Subtle visual echo of a ranked distribution.
    draw.ellipse((705, -145, 1220, 370), fill="#17233B")
    draw.ellipse((820, -20, 1135, 295), outline=TEAL, width=7)
    for index, bar_height in enumerate((80, 145, 215, 295, 385)):
        x0 = 675 + index * 68
        draw.rounded_rectangle(
            (x0, 1000 - bar_height, x0 + 42, 1000),
            radius=21,
            fill=(TEAL, PURPLE, TEAL, AMBER, PURPLE)[index],
        )

    draw_brand_mark(draw, 72, 72)
    kicker = font(FONT_SEMIBOLD, 27)
    draw.text((72, 130), "AFL DATA  •  1990–2026", font=kicker, fill="#9FB0C8")

    title_font = font(FONT_BOLD, 79)
    title_lines = ["More even", "than ever?"]
    draw_lines(draw, (72, 230), title_lines, selected_font=title_font, fill=WHITE, spacing=0)

    subtitle_font = font(FONT_REGULAR, 37)
    subtitle = "Competitive balance in the AFL"
    draw.text((75, 445), subtitle, font=subtitle_font, fill="#D8E1EC")

    statement_font = font(FONT_REGULAR, 31)
    statement_lines = wrap_text(
        draw,
        "What 37 seasons of data say about evenness, mobility and repeat success.",
        statement_font,
        620,
    )
    draw_lines(draw, (75, 570), statement_lines, selected_font=statement_font, fill="#9FB0C8", spacing=12)

    draw.rounded_rectangle((72, 1090, 414, 1166), radius=38, fill=WHITE)
    swipe_font = font(FONT_SEMIBOLD, 25)
    draw.text((104, 1111), "SWIPE TO EXPLORE  →", font=swipe_font, fill=NAVY)

    small = font(FONT_REGULAR, 22)
    draw.text((72, 1276), "nealhughes.net", font=small, fill="#8293AA")
    cover_number = f"01 / {TOTAL_SLIDES:02d}"
    cover_box = draw.textbbox((0, 0), cover_number, font=small)
    draw.text((WIDTH - 72 - (cover_box[2] - cover_box[0]), 1276), cover_number, font=small, fill="#8293AA")
    return image.convert("RGB")


def fit_chart(source: Image.Image, max_width: int, max_height: int) -> Image.Image:
    image = source.convert("RGB")
    scale = min(max_width / image.width, max_height / image.height)
    size = (round(image.width * scale), round(image.height * scale))
    return image.resize(size, Image.Resampling.LANCZOS)


def make_chart_slide(spec: ChartSlide, number: int) -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)

    # Editorial header.
    draw.rounded_rectangle((58, 49, 116, 107), radius=29, fill=spec.accent)
    number_font = font(FONT_BOLD, 25)
    number_text = f"{number:02d}"
    number_box = draw.textbbox((0, 0), number_text, font=number_font)
    draw.text(
        (87 - (number_box[2] - number_box[0]) / 2, 60),
        number_text,
        font=number_font,
        fill=WHITE,
    )
    section_font = font(FONT_SEMIBOLD, 23)
    draw.text((137, 64), spec.section, font=section_font, fill=spec.accent)

    headline_font = font(FONT_BOLD, 45)
    headline_lines = wrap_text(draw, spec.headline, headline_font, 900)
    headline_bottom = draw_lines(
        draw,
        (58, 122),
        headline_lines,
        selected_font=headline_font,
        fill=NAVY,
        spacing=-3,
    )

    source_path = SOURCE_DIR / spec.filename
    if not source_path.exists():
        raise FileNotFoundError(f"Source chart not found: {source_path}")

    with Image.open(source_path) as source:
        is_tall = source.height / source.width > 0.82
        chart_top = max(258, headline_bottom + 18)
        chart_max_height = 950 if is_tall else 650
        chart = fit_chart(source, 1020, chart_max_height)

    chart_x = (WIDTH - chart.width) // 2
    chart_y = chart_top
    image.paste(chart, (chart_x, chart_y))
    chart_bottom = chart_y + chart.height

    # The dense transition matrices need the full vertical area.  Wider charts
    # get a concise interpretation card underneath.
    if spec.takeaway:
        card_top = max(chart_bottom + 22, 955)
        card_bottom = min(card_top + 198, 1255)
        if card_bottom - card_top >= 130:
            rounded_rectangle(
                image,
                (58, card_top, WIDTH - 58, card_bottom),
                radius=28,
                fill=WHITE,
                shadow=True,
            )
            draw = ImageDraw.Draw(image)
            draw.rounded_rectangle((82, card_top + 30, 94, card_bottom - 30), radius=6, fill=spec.accent)
            label_font = font(FONT_SEMIBOLD, 18)
            draw.text((118, card_top + 27), "WHAT THE CHART SHOWS", font=label_font, fill=spec.accent)
            body_font = font(FONT_REGULAR, 25)
            body_lines = wrap_text(draw, spec.takeaway, body_font, 825)
            draw_lines(
                draw,
                (118, card_top + 61),
                body_lines,
                selected_font=body_font,
                fill=NAVY,
                spacing=3,
            )

    draw = ImageDraw.Draw(image)
    draw_footer(draw, number)
    return image.convert("RGB")


def draw_summary_card(
    image: Image.Image,
    top: int,
    number: str,
    title: str,
    body: str,
    accent: str,
) -> None:
    rounded_rectangle(image, (58, top, WIDTH - 58, top + 226), radius=30, fill=WHITE, shadow=True)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((86, top + 40, 144, top + 98), radius=29, fill=accent)
    badge_font = font(FONT_BOLD, 24)
    badge_box = draw.textbbox((0, 0), number, font=badge_font)
    draw.text(
        (115 - (badge_box[2] - badge_box[0]) / 2, top + 49),
        number,
        font=badge_font,
        fill=WHITE,
    )
    title_font = font(FONT_BOLD, 32)
    draw.text((174, top + 36), title, font=title_font, fill=NAVY)
    body_font = font(FONT_REGULAR, 26)
    body_lines = wrap_text(draw, body, body_font, 780)
    draw_lines(draw, (174, top + 87), body_lines, selected_font=body_font, fill=SLATE, spacing=4)


def make_summary() -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw_brand_mark(draw, 58, 54)
    kicker_font = font(FONT_SEMIBOLD, 22)
    draw.text((58, 95), "THE BIG PICTURE", font=kicker_font, fill=TEAL_DARK)
    heading_font = font(FONT_BOLD, 54)
    draw.text((58, 132), "Three things to take away", font=heading_font, fill=NAVY)

    draw_summary_card(
        image,
        250,
        "1",
        "More even at the top",
        "Leading teams are closer together, while the weakest teams sit further from the middle.",
        TEAL,
    )
    draw_summary_card(
        image,
        503,
        "2",
        "Less movement between tiers",
        "Team strength persists for longer; top and bottom teams have both become stickier.",
        PURPLE,
    )
    draw_summary_card(
        image,
        756,
        "3",
        "Still better than the old VFL",
        "Balance remains much stronger than in the 1970s and 1980s, despite slipping since 2008.",
        AMBER,
    )

    draw.rounded_rectangle((58, 1044, WIDTH - 58, 1215), radius=32, fill=NAVY)
    cta_font = font(FONT_BOLD, 29)
    draw.text((91, 1080), "Read the full analysis", font=cta_font, fill=WHITE)
    url_font = font(FONT_REGULAR, 26)
    draw.text((91, 1131), "nealhughes.net/afl-balance/", font=url_font, fill="#A9D7E1")
    arrow_font = font(FONT_BOLD, 42)
    draw.text((WIDTH - 127, 1091), "→", font=arrow_font, fill=WHITE)

    draw_footer(draw, TOTAL_SLIDES)
    return image.convert("RGB")


def validate_sources() -> None:
    missing = [slide.filename for slide in SLIDES if not (SOURCE_DIR / slide.filename).exists()]
    if missing:
        raise FileNotFoundError("Missing source chart(s): " + ", ".join(missing))


def save_outputs(slides: list[Image.Image]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_file in OUTPUT_DIR.glob("slide-*.png"):
        old_file.unlink()

    for index, slide in enumerate(slides, start=1):
        slide.save(OUTPUT_DIR / f"slide-{index:02d}.png", format="PNG", optimize=True)

    slides[0].save(
        OUTPUT_DIR / "afl-competitive-balance-carousel.pdf",
        format="PDF",
        save_all=True,
        append_images=slides[1:],
        resolution=144,
    )


def main() -> None:
    validate_sources()
    rendered = [make_chart_slide(spec, index) for index, spec in enumerate(SLIDES, start=1)]
    rendered.append(make_summary())
    save_outputs(rendered)
    print(f"Created {len(rendered)} slides in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
