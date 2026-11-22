"""Workbench hero: identity module, control-loop module, three project modules."""

from content import META, NAME, PROJECTS, ROLE, STAGES, TAGLINE
from kit import MONO, SANS, THEMES, backdrop, chamfer, label, pill, stage_node, svg, text

TITLE = f"{NAME} — {ROLE}"
DESC = (
    f"{NAME}. {ROLE}. {' '.join(TAGLINE)} Control loop: the model proposes, code enforces policy, "
    "a person authorizes actions above risk limits, the outcome is verified at the source. Flagship "
    "systems: PayOps Sentinel, AgentDoor, DisputeDesk."
)


def control_loop(c, x0, y, span):
    gap = span / 3
    parts = []
    for i in range(3):
        x1, x2 = x0 + i * gap + 16, x0 + (i + 1) * gap - 18
        colour = c["faint"] if i == 0 else c["amber"]
        dash = ' stroke-dasharray="3 5"' if i == 0 else ""
        parts.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{colour}" stroke-width="2"{dash}/>')
    for i, (name, caption) in enumerate(STAGES):
        x = x0 + i * gap
        parts += [stage_node(i, x, y, c), text(x - 10, y + 34, name, 14, c["text"], MONO, 600, 1.6),
                  text(x - 10, y + 54, caption, 14, c["muted"])]
    return "".join(parts)


def project_module(p, c, y):
    col = c[p["accent"]]
    return "".join([
        chamfer(752, y, 424, 172, c),
        f'<rect x="752" y="{y}" width="140" height="3" fill="{col}"/>',
        text(780, y + 46, p["num"], 14, col, MONO, 600, 1.5),
        text(814, y + 47, p["name"], 25, c["text"], SANS, 700),
        pill(1150, y + 26, p["status"], col, 14),
        label(780, y + 76, p["category"], col),
        text(780, y + 106, p["pitch"], 15, c["muted"]),
        f'<line x1="780" y1="{y + 124}" x2="1148" y2="{y + 124}" stroke="{c["border"]}"/>',
        text(780, y + 152, p["hero_evidence"], 14, c["text"], MONO, 500),
    ])


def bus(c):
    """Trace from the identity module to each project module."""
    ys = [110, 300, 490]
    stubs = "".join(f'<path d="M742 {y} H752" stroke="{c["faint"]}"/>'
                    f'<circle cx="742" cy="{y}" r="2.5" fill="{c["faint"]}"/>' for y in ys)
    return (f'<path d="M732 200 H742 M742 {ys[0]} V{ys[-1]}" fill="none" stroke="{c["faint"]}"/>'
            + stubs)


def hero_desktop(c):
    w, h = 1200, 600
    defs, field = backdrop(w, h, c)
    body = [
        field, chamfer(24, 24, 708, 352, c, 28), f'<rect x="24" y="24" width="4" height="352" fill="{c["amber"]}"/>',
        label(60, 68, "IDENTITY  /  SHRO-2002", c["cyan"]),
        text(56, 162, NAME, 78, c["text"], SANS, 700, -2),
        text(60, 206, ROLE, 21, c["amber"], SANS, 500),
        text(60, 262, TAGLINE[0], 25, c["text"]), text(60, 296, TAGLINE[1], 25, c["muted"]),
        f'<line x1="60" y1="330" x2="700" y2="330" stroke="{c["border"]}"/>',
        label(60, 356, META, c["faint"]),
        chamfer(24, 392, 708, 184, c), label(60, 432, "CONTROL LOOP", c["cyan"]),
        label(696, 432, "MODEL PROPOSES · CODE DECIDES", c["faint"], anchor="end"),
        control_loop(c, 74, 488, 570), bus(c),
    ]
    body += [project_module(p, c, 24 + i * 190) for i, p in enumerate(PROJECTS)]
    return svg(w, h, TITLE, DESC, "".join(body), defs)


def project_row(p, c, y):
    col = c[p["accent"]]
    return "".join([
        chamfer(16, y, 528, 116, c, 16),
        f'<rect x="16" y="{y}" width="110" height="3" fill="{col}"/>',
        text(40, y + 47, p["num"], 22, col, MONO, 600),
        text(84, y + 48, p["name"], 30, c["text"], SANS, 700),
        pill(520, y + 18, p["status"], col, 20),
        text(40, y + 94, p["hero_evidence"], 22, c["muted"], MONO, 500),
    ])


def hero_mobile(c):
    w, h = 560, 788
    defs, field = backdrop(w, h, c, 16)
    body = [
        field, chamfer(16, 16, 528, 372, c, 22), f'<rect x="16" y="16" width="4" height="372" fill="{c["amber"]}"/>',
        label(44, 58, "IDENTITY / SHRO-2002", c["cyan"], 20),
        text(40, 128, NAME, 56, c["text"], SANS, 700, -1.5),
        text(44, 170, "Software Engineer ·", 23, c["amber"], SANS, 500),
        text(44, 200, "AI Systems & Agentic Applications", 23, c["amber"], SANS, 500),
        text(44, 252, "Building reliable AI systems that", 24, c["text"]),
        text(44, 284, "use tools, enforce policies,", 24, c["text"]),
        text(44, 316, "and verify outcomes.", 24, c["muted"]),
        label(44, 362, "GE VERNOVA · BENGALURU", c["faint"], 20),
    ]
    body += [project_row(p, c, 404 + i * 128) for i, p in enumerate(PROJECTS)]
    return svg(w, h, TITLE, DESC, "".join(body), defs)


def shortcut(p):
    """Clickable project chip shown under the hero. One dark variant: reads as a button on both themes."""
    c = THEMES["dark"]
    col = c[p["accent"]]
    w, h = 340, 76
    body = "".join([
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="{c["panel"]}" stroke="{col}" '
        f'stroke-opacity="0.55"/>',
        f'<rect x="0.5" y="14" width="4" height="{h - 28}" rx="2" fill="{col}"/>',
        text(24, 34, p["num"], 17, col, MONO, 600),
        text(58, 35, p["name"], 25, c["text"], SANS, 700),
        text(58, 60, f"{p['status']}  ·  REPOSITORY ↗", 14, c["muted"], MONO, 500, 1.2),
    ])
    return svg(w, h, f"{p['name']} repository", f"Open the {p['name']} repository on GitHub.", body)
