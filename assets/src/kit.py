"""Shared palette, fonts and SVG primitives for the profile artwork."""

import base64
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent

THEMES = {
    "dark": {
        "bg": "#0A0E14", "panel": "#0F151E", "border": "#1E2834", "grid": "#18222E",
        "text": "#E8EDF2", "muted": "#8F9BAA", "faint": "#556171", "frame": "#05080C",
        "amber": "#F0A832", "cyan": "#4FD1E8", "green": "#3FB950", "glow": "0.10",
    },
    "light": {
        "bg": "#F5F3EE", "panel": "#FFFFFF", "border": "#DCD7CC", "grid": "#E4DED2",
        "text": "#0D1117", "muted": "#56606C", "faint": "#8A929C", "frame": "#0D1117",
        "amber": "#B86E00", "cyan": "#0A7D93", "green": "#1A7F37", "glow": "0.07",
    },
}

SANS = "'Avenir Next', 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def svg(w, h, title, desc, body, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">'
        f'<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>'
        f"<defs>{defs}</defs>{body}</svg>\n"
    )


def text(x, y, s, size, fill, font=SANS, weight=400, spacing=0, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
        f'letter-spacing="{spacing}" fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>'
    )


def label(x, y, s, fill, size=13, anchor="start"):
    """Wide-tracked monospace caps: section labels and categories."""
    return text(x, y, s, size, fill, MONO, 500, 2.4, anchor)


def chamfer(x, y, w, h, c, cut=20):
    """Card with the top-right corner cut, the recurring module shape."""
    d = f"M{x} {y} H{x + w - cut} L{x + w} {y + cut} V{y + h} H{x} Z"
    return f'<path d="{d}" fill="{c["panel"]}" stroke="{c["border"]}"/>'


def pill(x_right, y, s, colour, size=11):
    """Outlined status pill, right-aligned at x_right with its top at y."""
    w = round(len(s) * size * 0.78 + 20)
    return (
        f'<rect x="{x_right - w}" y="{y}" width="{w}" height="{size * 2.2:.0f}" rx="{size * 1.1:.0f}" '
        f'fill="none" stroke="{colour}" stroke-width="1.2"/>'
        + text(x_right - w / 2, y + size * 1.48, s, size, colour, MONO, 600, 1.4, "middle")
    )


def backdrop(w, h, c, rx=18):
    """Rounded field with a dot grid and a faint amber glow from the top left."""
    defs = (
        f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<circle cx="1.5" cy="1.5" r="1.1" fill="{c["grid"]}"/></pattern>'
        f'<radialGradient id="glow" cx="0.15" cy="0.15" r="0.75">'
        f'<stop offset="0" stop-color="{c["amber"]}" stop-opacity="{c["glow"]}"/>'
        f'<stop offset="1" stop-color="{c["amber"]}" stop-opacity="0"/></radialGradient>'
    )
    body = "".join(
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="{f}"{s}/>'
        for f, s in [(c["bg"], f' stroke="{c["border"]}"'), ("url(#dots)", ""), ("url(#glow)", "")]
    )
    return defs, body


def stage_node(kind, x, y, c):
    """Dashed circle = model (probabilistic), square = code, diamond = human gate, check = verified."""
    if kind == 0:
        return (f'<circle cx="{x}" cy="{y}" r="9" fill="{c["panel"]}" stroke="{c["muted"]}" '
                f'stroke-width="2" stroke-dasharray="3 3"/>')
    if kind == 1:
        return f'<rect x="{x - 8}" y="{y - 8}" width="16" height="16" fill="{c["amber"]}"/>'
    if kind == 2:
        return (f'<path d="M{x} {y - 11} L{x + 11} {y} L{x} {y + 11} L{x - 11} {y} Z" '
                f'fill="{c["panel"]}" stroke="{c["amber"]}" stroke-width="2.2"/>')
    return (f'<circle cx="{x}" cy="{y}" r="10" fill="{c["green"]}"/>'
            f'<path d="M{x - 4} {y} l3 3 l5.5 -6" fill="none" stroke="{c["panel"]}" '
            f'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')


def screenshot(path, x, y, w, h, c, clip_id="shot"):
    """Embed a real app screenshot (data URI, so it renders inside an <img>-loaded SVG)."""
    data = base64.b64encode((ASSETS / path).read_bytes()).decode()
    return (
        f'<clipPath id="{clip_id}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/></clipPath>'
        f'<rect x="{x - 1}" y="{y - 1}" width="{w + 2}" height="{h + 2}" rx="11" fill="{c["frame"]}" '
        f'stroke="{c["border"]}"/>'
        f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" '
        f'clip-path="url(#{clip_id})" href="data:image/jpeg;base64,{data}"/>'
    )
