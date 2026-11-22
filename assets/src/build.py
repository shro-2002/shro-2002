"""Build the profile SVGs in dark and light variants.

Run: python3 assets/src/build.py  (writes assets/*.svg)
One palette per theme keeps both variants in sync; GitHub picks the variant
through <picture> + prefers-color-scheme in README.md.
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent

THEMES = {
    "dark": {
        "bg": "#0B0F14", "border": "#1E2630", "grid": "#141B23",
        "text": "#E6EDF3", "muted": "#8B949E", "faint": "#56606B",
        "accent": "#E8A33D", "ok": "#3FB950", "node": "#0B0F14",
    },
    "light": {
        "bg": "#FBFAF7", "border": "#D8DEE4", "grid": "#EFEDE8",
        "text": "#0D1117", "muted": "#57606A", "faint": "#8C959F",
        "accent": "#B4690E", "ok": "#1A7F37", "node": "#FBFAF7",
    },
}

SANS = "Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

STEPS = [
    ("01", "PROPOSE", "The model plans the action"),
    ("02", "ENFORCE", "Policy in code allows or denies"),
    ("03", "AUTHORIZE", "A person signs what can't be undone"),
    ("04", "VERIFY", "Outcome re-checked at the source"),
]


def grid(c, width, height, cols=12, inset=56):
    step = (width - 2 * inset) / cols
    lines = [
        f'<line x1="{inset + i * step:.1f}" y1="1" x2="{inset + i * step:.1f}" '
        f'y2="{height - 1}" stroke="{c["grid"]}" stroke-width="1"/>'
        for i in range(cols + 1)
    ]
    return "\n".join(lines)


def node(kind, x, y, c):
    """Glyph per stage: dashed circle (probabilistic), square (deterministic),
    diamond (human gate), check (verified)."""
    if kind == 0:
        return (f'<circle cx="{x}" cy="{y}" r="11" fill="{c["node"]}" stroke="{c["muted"]}" '
                f'stroke-width="2" stroke-dasharray="3 3"/>')
    if kind == 1:
        return (f'<rect x="{x - 10}" y="{y - 10}" width="20" height="20" fill="{c["accent"]}"/>')
    if kind == 2:
        return (f'<path d="M{x} {y - 13} L{x + 13} {y} L{x} {y + 13} L{x - 13} {y} Z" '
                f'fill="{c["node"]}" stroke="{c["accent"]}" stroke-width="2.5"/>')
    return (f'<circle cx="{x}" cy="{y}" r="12" fill="{c["ok"]}"/>'
            f'<path d="M{x - 5} {y} l3.5 3.5 l6.5 -7" fill="none" stroke="{c["node"]}" '
            f'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')


def hero(c):
    w, h = 1200, 420
    xs = [80, 368, 656, 944]
    line_y = 318
    flow = []
    for i in range(3):
        x1, x2 = xs[i] + 18, xs[i + 1] - 22
        dash = ' stroke-dasharray="4 5"' if i == 0 else ""
        flow.append(
            f'<line x1="{x1}" y1="{line_y}" x2="{x2}" y2="{line_y}" '
            f'stroke="{c["muted"] if i == 0 else c["accent"]}" stroke-width="2"{dash}/>'
            f'<path d="M{x2} {line_y - 5} L{x2 + 8} {line_y} L{x2} {line_y + 5} Z" '
            f'fill="{c["muted"] if i == 0 else c["accent"]}"/>'
        )
    steps = []
    for i, (num, label, desc) in enumerate(STEPS):
        x = xs[i]
        steps.append(node(i, x, line_y, c))
        steps.append(
            f'<text x="{x - 12}" y="{line_y + 44}" font-family="{MONO}" font-size="13" '
            f'letter-spacing="2" fill="{c["faint"]}">{num}  '
            f'<tspan fill="{c["text"]}" font-weight="600">{label}</tspan></text>'
            f'<text x="{x - 12}" y="{line_y + 68}" font-family="{SANS}" font-size="16" '
            f'fill="{c["muted"]}">{desc}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">
<title id="t">Shroddha Ghosh — Software Engineer, AI Systems and Agentic Applications</title>
<desc id="d">Building AI systems that reason, use tools, verify outcomes and stay inside enforceable limits. Four stages: the model proposes, code enforces policy, a person authorizes irreversible actions, and the outcome is verified at the source.</desc>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{c["bg"]}" stroke="{c["border"]}"/>
{grid(c, w, h)}
<text x="56" y="62" font-family="{MONO}" font-size="13" letter-spacing="2.6" fill="{c["muted"]}">SOFTWARE ENGINEER  /  AI SYSTEMS &amp; AGENTIC APPLICATIONS</text>
<text x="{w - 56}" y="62" text-anchor="end" font-family="{MONO}" font-size="13" letter-spacing="2.6" fill="{c["faint"]}">GE VERNOVA</text>
<line x1="56" y1="80" x2="{w - 56}" y2="80" stroke="{c["text"]}" stroke-width="2"/>
<text x="52" y="164" font-family="{SANS}" font-size="78" font-weight="700" letter-spacing="-2.5" fill="{c["text"]}">Shroddha Ghosh</text>
<rect x="56" y="186" width="44" height="4" fill="{c["accent"]}"/>
<text x="56" y="228" font-family="{SANS}" font-size="25" fill="{c["text"]}">Building AI systems that reason, use tools, verify outcomes,</text>
<text x="56" y="260" font-family="{SANS}" font-size="25" fill="{c["muted"]}">and stay inside limits that code can enforce.</text>
{"".join(flow)}
{"".join(steps)}
</svg>
"""


def main():
    for name, c in THEMES.items():
        (OUT / f"hero-{name}.svg").write_text(hero(c))


if __name__ == "__main__":
    main()
