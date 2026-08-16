#!/usr/bin/env python3
"""Convert a publisher rulebook PDF to retrieval-oriented Markdown.

Use this for any game whose authorized rules live in a local PDF. Output is
plain Markdown with page markers, heading fonts, and exact wording. It does
not summarize, spell-repair, or drop repeated content. Missing glyphs and
unnamed icons become [UNCLEAR].

Extracts stay gitignored. Typical layout:

    data/games/<slug>/rulebooks/<name>.md

Setup:

    pip install -e ".[pdf]"

Examples:

    python scripts/pdf_to_rules_md.py rules.pdf -o data/games/too-many-bones/rulebooks/tmb-undertow-rulebook-v2.1.md
    python scripts/pdf_to_rules_md.py rules.pdf --title "Game Name Rulebook" -o out.md
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import pymupdf
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "pymupdf is required. Install with: pip install -e '.[pdf]'"
    ) from exc

HEADING_FONT_RE = re.compile(
    r"(Hea|Heavy|Black|Bold|Bentwood|Display|Titl|Condensed)",
    re.I,
)
BODY_FONT_RE = re.compile(r"(Reg|Roman|Book|Minion|Light|Obl|Italic|It$)", re.I)
ICON_NAMES = {
    "atk": "[ATK]",
    "def": "[DEF]",
    "dex": "[Dex]",
    "hp": "[HP]",
    "dmg": "[Dmg]",
    "ini": "[Ini]",
    "bp": "[BP]",
    "true dmg": "[True Dmg]",
}
NEW_ENTRY_RE = re.compile(
    r"^\*?\*?[A-Za-z][A-Za-z0-9 #’'\-/]*\*?\*? [–—-] "
)
PAGE_NUM_RE = re.compile(r"^\d{1,3}$")


@dataclass
class Span:
    x0: float
    y0: float
    x1: float
    y1: float
    text: str
    font: str
    size: float


@dataclass
class Line:
    spans: list[Span]
    x0: float
    y0: float
    x1: float
    y1: float
    column: str  # "full", "left", "right"


def _flags_no_images() -> int:
    flags = pymupdf.TEXTFLAGS_DICT
    flags &= ~pymupdf.TEXT_PRESERVE_IMAGES
    return flags


def _collapse_outline_spans(spans: list[Span]) -> list[Span]:
    """Keep one copy of stacked outline/stroke glyphs at the same box.

    This is a rendering artifact, not repeated rules text.
    """
    if not spans:
        return []
    spans = sorted(spans, key=lambda s: (round(s.y0, 1), s.x0, -len(s.text)))
    kept: list[Span] = []
    for span in spans:
        duplicate = False
        for prev in kept:
            same_box = (
                abs(span.x0 - prev.x0) < 1.8
                and abs(span.y0 - prev.y0) < 1.8
                and abs(span.x1 - prev.x1) < 2.5
                and abs(span.y1 - prev.y1) < 2.5
            )
            if same_box:
                duplicate = True
                break
            nested = (
                span.x0 >= prev.x0 - 1.2
                and span.x1 <= prev.x1 + 1.2
                and abs(span.y0 - prev.y0) < 2.0
                and span.text
                and span.text in prev.text
            )
            if nested:
                duplicate = True
                break
        if not duplicate:
            kept.append(span)
    return kept


def _page_lines(page: pymupdf.Page) -> list[Line]:
    data = page.get_text("dict", flags=_flags_no_images())
    raw_lines: list[list[Span]] = []
    for block in data.get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            spans = [
                Span(
                    x0=float(s["bbox"][0]),
                    y0=float(s["bbox"][1]),
                    x1=float(s["bbox"][2]),
                    y1=float(s["bbox"][3]),
                    text=s.get("text") or "",
                    font=s.get("font") or "",
                    size=float(s.get("size") or 0),
                )
                for s in line.get("spans", [])
                if (s.get("text") or "") != ""
            ]
            spans = _collapse_outline_spans(spans)
            if spans:
                raw_lines.append(spans)

    page_w = float(page.rect.width)
    mid = page_w / 2.0
    measured: list[Line] = []
    for spans in raw_lines:
        x0 = min(s.x0 for s in spans)
        y0 = min(s.y0 for s in spans)
        x1 = max(s.x1 for s in spans)
        y1 = max(s.y1 for s in spans)
        measured.append(Line(spans=spans, x0=x0, y0=y0, x1=x1, y1=y1, column="full"))

    if not measured:
        return []

    left_n = sum(1 for ln in measured if (ln.x0 + ln.x1) / 2.0 < mid - 18)
    right_n = sum(1 for ln in measured if (ln.x0 + ln.x1) / 2.0 > mid + 18)
    two_col = left_n >= 4 and right_n >= 4

    if two_col:
        for ln in measured:
            width = ln.x1 - ln.x0
            center = (ln.x0 + ln.x1) / 2.0
            if width > page_w * 0.62:
                ln.column = "full"
            elif center < mid:
                ln.column = "left"
            else:
                ln.column = "right"

    return _reading_order(_merge_baseline_lines(measured))


def _merge_baseline_lines(lines: list[Line]) -> list[Line]:
    """Join fragments that share a baseline so icons do not split a sentence."""
    if not lines:
        return []
    ordered = sorted(lines, key=lambda ln: (ln.y0, ln.x0))
    groups: list[list[Line]] = []
    for ln in ordered:
        if groups:
            prev = groups[-1][-1]
            same_band = abs(ln.y0 - prev.y0) <= 3.2
            gutter = ln.x0 - prev.x1 > 18.0
            if same_band and not gutter:
                groups[-1].append(ln)
                continue
        groups.append([ln])
    merged: list[Line] = []
    for group in groups:
        spans = _collapse_outline_spans([span for ln in group for span in ln.spans])
        merged.append(
            Line(
                spans=spans,
                x0=min(ln.x0 for ln in group),
                y0=min(ln.y0 for ln in group),
                x1=max(ln.x1 for ln in group),
                y1=max(ln.y1 for ln in group),
                column=group[0].column
                if len({ln.column for ln in group}) == 1
                else "full",
            )
        )
    return merged


def _reading_order(lines: list[Line]) -> list[Line]:
    if not lines:
        return []
    if all(ln.column == "full" for ln in lines):
        return sorted(lines, key=lambda ln: (ln.y0, ln.x0))

    ordered: list[Line] = []
    left: list[Line] = []
    right: list[Line] = []

    def flush() -> None:
        left.sort(key=lambda ln: (ln.y0, ln.x0))
        right.sort(key=lambda ln: (ln.y0, ln.x0))
        ordered.extend(left)
        ordered.extend(right)
        left.clear()
        right.clear()

    for ln in sorted(lines, key=lambda ln: (ln.y0, ln.x0)):
        if ln.column == "full":
            flush()
            ordered.append(ln)
        elif ln.column == "left":
            left.append(ln)
        else:
            right.append(ln)
    flush()
    return ordered


def _icon_token(left: str, right: str) -> str:
    window = (left[-40:] + " " + right[:20]).lower()
    if "true dmg" in window:
        return ICON_NAMES["true dmg"]
    words = re.findall(r"[A-Za-z]+", left.lower())
    if words:
        last = words[-1]
        if last in ICON_NAMES:
            return ICON_NAMES[last]
    return "[UNCLEAR]"


def _join_spans(spans: list[Span]) -> str:
    spans = sorted(spans, key=lambda s: s.x0)
    parts: list[str] = []
    prev: Span | None = None
    for span in spans:
        if prev is None:
            parts.append(span.text)
            prev = span
            continue
        gap = span.x0 - prev.x1
        left = parts[-1] if parts else ""
        open_paren = left.rstrip().endswith("(")
        between_parens = open_paren and span.text.lstrip().startswith(")")
        mid_icon = 11.0 <= gap <= 28.0 and not left.endswith(" ") and not span.text.startswith(" ")
        if open_paren and gap > 4.5:
            parts.append(_icon_token(left, span.text))
            if not span.text.startswith((")", "=", " ")):
                parts.append(" ")
        elif re.fullmatch(r"[•●·\-–—\d.]+", left.strip()) and gap < 55.0:
            if not left.endswith(" "):
                parts.append(" ")
        elif between_parens or (mid_icon and not left.endswith("-")):
            parts.append(_icon_token(left, span.text))
            if not span.text.startswith(")") and between_parens:
                parts.append(" ")
        elif re.fullmatch(r"[•●·\-–—\d.]+", left.strip()) and gap < 55.0:
            if not left.endswith(" "):
                parts.append(" ")
        elif gap >= 14.0:
            token = _icon_token(left, span.text)
            if not left.endswith(" "):
                parts.append(" ")
            parts.append(token)
            if not span.text.startswith(" "):
                parts.append(" ")
        elif gap > 1.6 and not left.endswith((" ", "\n")) and not span.text.startswith((" ", "\n")):
            parts.append(" ")
        parts.append(span.text)
        prev = span
    text = "".join(parts)
    text = re.sub(r"\(\s*\)", "([UNCLEAR])", text)
    text = re.sub(r"\(roll\s+\)", "(roll [UNCLEAR])", text)
    text = re.sub(r"\(\s*\[UNCLEAR\]\s*\)", "([UNCLEAR])", text)
    text = re.sub(r"\(\s*(\[[^\]]+\])\s*\)", r"(\1)", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def _max_size(line: Line) -> float:
    return max(s.size for s in line.spans)


def _heading_span(line: Line) -> Span | None:
    first = line.spans[0]
    if HEADING_FONT_RE.search(first.font) and not BODY_FONT_RE.search(first.font):
        return first
    if first.size >= _max_size(line) - 0.15 and first.size >= 12.5:
        return first
    return None


def _leading_name_spans(line: Line) -> list[Span]:
    name: list[Span] = []
    for span in line.spans:
        heavy = HEADING_FONT_RE.search(span.font) and not BODY_FONT_RE.search(span.font)
        if heavy and span.size <= 12.5:
            name.append(span)
            continue
        break
    return name if name and len(name) < len(line.spans) else []


def _emit_line(line: Line, body_size: float) -> str:
    text = _join_spans(line.spans)
    if not text:
        return ""
    size = _max_size(line)
    name_spans = _leading_name_spans(line)
    if name_spans:
        name = _join_spans(name_spans)
        body = _join_spans(line.spans[len(name_spans) :])
        if name and body:
            return f"**{name}** {body}"
    if NEW_ENTRY_RE.match(text) and " – " in text:
        name, body = text.split(" – ", 1)
        if 1 <= len(name) <= 40:
            return f"**{name.strip('*')}** – {body}"

    if PAGE_NUM_RE.match(text):
        return text

    heading = _heading_span(line)
    if heading is not None and size >= max(body_size + 2.4, 12.0) and (size >= 13.0 or len(text) <= 80):
        if size >= 18:
            return f"# {text}"
        if size >= 13.5:
            return f"## {text}"
        return f"### {text}"
    return text


def _body_size(lines: list[Line]) -> float:
    sizes = [round(s.size, 1) for ln in lines for s in ln.spans]
    if not sizes:
        return 10.0
    counts: dict[float, int] = {}
    for size in sizes:
        counts[size] = counts.get(size, 0) + 1
    return max(counts.items(), key=lambda kv: kv[1])[0]


def convert_page(page: pymupdf.Page) -> str:
    lines = _page_lines(page)
    body_size = _body_size(lines)
    chunks: list[tuple[float, str, str]] = [
        (ln.y0, _emit_line(ln, body_size), ln.column) for ln in lines
    ]
    chunks = [(y, t, col) for y, t, col in chunks if t]

    out: list[str] = []
    prev_y: float | None = None
    prev_col = ""
    prev_was_named = False
    for y, text, col in chunks:
        named = text.startswith("**") or bool(NEW_ENTRY_RE.match(text))
        heading = text.startswith(("# ", "## ", "### "))
        if prev_y is not None:
            gap = y - prev_y
            wrap = (
                0 < gap <= body_size * 2.05
                and col == prev_col
                and not named
                and not heading
            )
            if wrap and out:
                out[-1] = f"{out[-1]} {text}"
                prev_y = y
                prev_col = col
                continue
            if gap > body_size * 2.05 or named or heading or prev_was_named or col != prev_col:
                if out and out[-1] != "":
                    out.append("")
        out.append(text)
        prev_y = y
        prev_col = col
        prev_was_named = named or heading
    return "\n".join(out).strip()


KNOWN_TITLES = (
    (("tmb-ub", "unbreakable"), "Too Many Bones: Unbreakable Rulebook"),
    (("tmbu", "undertow"), "Too Many Bones: Undertow Rulebook"),
    (("baddie",), "Too Many Bones: Baddie Skills Reference Sheet"),
)


def _header(path: Path, first_page_text: str, title: str | None = None) -> str:
    version = ""
    m = re.search(r"Version\s+([0-9.]+)", first_page_text, re.I)
    if m:
        version = m.group(1)
    else:
        m = re.search(r"\bv([0-9.]+)\b", first_page_text, re.I)
        if m:
            version = m.group(1)
    resolved = (title or "").strip()
    if not resolved:
        lower = path.name.lower()
        for needles, known in KNOWN_TITLES:
            if any(needle in lower for needle in needles):
                resolved = known
                break
        else:
            resolved = path.stem.replace("_", " ").strip()
    lines = [f"# {resolved}", f"**Source:** {path.name}"]
    if version:
        lines.append(f"**Version:** {version}")
    return "\n".join(lines)


def convert_pdf(pdf_path: Path, title: str | None = None) -> str:
    doc = pymupdf.open(pdf_path)
    try:
        first = doc[0].get_text("text") if doc.page_count else ""
        parts = [_header(pdf_path, first, title=title), ""]
        for i, page in enumerate(doc):
            parts.append(f"<!-- PAGE {i + 1} -->")
            parts.append("")
            body = convert_page(page)
            parts.append(body if body else "[UNCLEAR]")
            parts.append("")
        return "\n".join(parts).rstrip() + "\n"
    finally:
        doc.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a rulebook PDF to retrieval Markdown.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Install the PDF extra first: pip install -e '.[pdf]'",
    )
    parser.add_argument("pdf", type=Path, help="Path to a local publisher PDF")
    parser.add_argument("-o", "--output", type=Path, help="Write Markdown here instead of stdout")
    parser.add_argument("--title", help="Source title for the Markdown header")
    args = parser.parse_args()
    pdf = args.pdf.expanduser().resolve()
    if not pdf.is_file():
        print(f"missing PDF: {pdf}", file=sys.stderr)
        raise SystemExit(1)
    markdown = convert_pdf(pdf, title=args.title)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
        print(f"wrote {args.output} ({len(markdown.splitlines())} lines)")
    else:
        sys.stdout.write(markdown)


if __name__ == "__main__":
    main()
