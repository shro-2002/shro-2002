"""Project covers (real screenshot + evidence column) and the RewardShield research card."""

from content import REWARD_BARS, REWARD_FACTS, REWARD_NOTE
from kit import MONO, SANS, backdrop, label, pill, screenshot, svg, text


def cover_desc(p):
    metrics = "; ".join(f"{v} {' '.join(lines)}" for v, lines in p["metrics"])
    return f"{p['name']}: {' '.join(p['pitch_lines'])} Evidence: {metrics}. Status: {p['status'].lower()}."


def header(p, c, x, right, y, name_size, name_y):
    col = c[p["accent"]]
    return "".join([
        f'<rect x="{x - 8}" y="0.5" width="150" height="3" fill="{col}"/>',
        text(x, y, f"{p['num']}  /  FLAGSHIP", 14, col, MONO, 600, 2.4),
        pill(right, y - 18, p["status"], col, 12),
        text(x - 3, name_y, p["name"], name_size, c["text"], SANS, 700, -1),
    ])


def metric_block(value, lines, c, x, y, col, value_size=34, label_size=16):
    parts = [text(x, y, value, value_size, col, SANS, 700, -0.5)]
    parts += [text(x, y + 30 + 21 * i, s, label_size, c["muted"]) for i, s in enumerate(lines)]
    return "".join(parts)


def cover_desktop(p, c):
    w, h = 1200, 640
    defs, field = backdrop(w, h, c)
    col = c[p["accent"]]
    body = [field, header(p, c, 40, 1160, 56, 46, 116), label(40, 150, p["category"], col),
            text(40, 186, p["pitch"], 19, c["muted"]),
            screenshot(p["shot"], 40, 212, 704, 396, c, f"s-{p['slug']}"),
            label(784, 236, "EVIDENCE", c["faint"])]
    for i, (value, lines) in enumerate(p["metrics"]):
        y = 286 + i * 104
        body.append(metric_block(value, lines, c, 784, y, c["text"] if i else col))
        body.append(f'<line x1="784" y1="{y + 66}" x2="1160" y2="{y + 66}" stroke="{c["border"]}"/>')
    body += [text(784, 588 + 20 * i, s, 13, c["faint"], MONO, 500) for i, s in enumerate(p["stack"])]
    return svg(w, h, p["name"], cover_desc(p), "".join(body), defs)


def cover_mobile(p, c):
    w, h = 560, 900
    defs, field = backdrop(w, h, c, 16)
    col = c[p["accent"]]
    body = [field, header(p, c, 28, 532, 50, 44, 112), label(28, 148, p["category"], col, 14),
            text(28, 190, p["pitch_lines"][0], 22, c["muted"]), text(28, 220, p["pitch_lines"][1], 22, c["muted"]),
            screenshot(p["shot"], 28, 248, 504, 284, c, f"m-{p['slug']}")]
    for i, (value, lines) in enumerate(p["metrics"]):
        y = 598 + i * 94
        body.append(text(28, y, value, 28, c["text"] if i else col, SANS, 700, -0.5))
        body += [text(248, y - 16 + 26 * j, s, 19, c["muted"]) for j, s in enumerate(lines)]
        body.append(f'<line x1="28" y1="{y + 36}" x2="532" y2="{y + 36}" stroke="{c["border"]}"/>')
    body.append(text(28, 878, p["stack"][0], 15, c["faint"], MONO, 500))
    return svg(w, h, p["name"], cover_desc(p), "".join(body), defs)


RESEARCH_TITLE = "RewardShield — research"
RESEARCH_DESC = (
    "RewardShield, a pre-registered study of how often SQL execution rewards accept wrong queries. "
    "False-accept share on the dev-A audit split: " + "; ".join(f"{n} ({d}) {v}%" for n, d, v in REWARD_BARS)
    + ". " + " ".join(" ".join(f) for f in REWARD_FACTS) + " " + " ".join(REWARD_NOTE)
)


def bars(c, x_label, x_bar, y0, max_w, step=32, size=14):
    small = size - 2
    title = "FALSE-ACCEPT SHARE · LOWER IS BETTER" if size > 14 else "FALSE-ACCEPT SHARE · DEV-A · LOWER IS BETTER"
    parts = [label(x_label, y0 - 34, title, c["faint"], small)]
    for i, (name, dbs, value) in enumerate(REWARD_BARS):
        y = y0 + i * step
        best = name == "targeted-4"
        fill = c["cyan"] if best else c["faint"]
        bw = round(max_w * value / 4.5)
        parts += [text(x_label, y + 5, name, size, c["text"] if best else c["muted"], MONO, 600 if best else 400),
                  text(x_bar - 12, y + 5, dbs, small, c["faint"], MONO, 400, 0, "end"),
                  f'<rect x="{x_bar}" y="{y - size * 0.6:.0f}" width="{bw}" height="{size}" rx="3" fill="{fill}" '
                  f'fill-opacity="{1 if best else 0.55}"/>',
                  text(x_bar + bw + 10, y + 5, f"{value:.2f}%", size, c["text"] if best else c["muted"], MONO,
                       600 if best else 400)]
    return "".join(parts)


def research_head(c, x, right, title_size):
    return "".join([
        f'<rect x="{x - 8}" y="0.5" width="150" height="3" fill="{c["cyan"]}"/>',
        text(x, 56, "RESEARCH  /  OPEN SOURCE", 14, c["cyan"], MONO, 600, 2.4),
        pill(right, 38, "PRE-REGISTERED", c["cyan"], 12),
        text(x - 3, 114, "RewardShield", title_size, c["text"], SANS, 700, -1),
    ])


def facts(c, x, y0, size=16, step=58):
    parts = []
    for i, (a, b) in enumerate(REWARD_FACTS):
        y = y0 + i * step
        parts += [f'<rect x="{x}" y="{y - 11}" width="7" height="7" fill="{c["cyan"]}"/>',
                  text(x + 20, y, a, size, c["text"]), text(x + 20, y + size + 6, b, size, c["muted"])]
    return "".join(parts)


def research_desktop(c):
    w, h = 1200, 440
    defs, field = backdrop(w, h, c)
    body = [field, research_head(c, 40, 1160, 44),
            text(40, 152, "How often do SQL execution rewards accept wrong queries,", 19, c["muted"]),
            text(40, 178, "and does catching them change what a small agent learns?", 19, c["muted"]),
            facts(c, 40, 236), bars(c, 640, 830, 236, 260),
            text(640, 404, REWARD_NOTE[0], 12, c["faint"], MONO), text(640, 422, REWARD_NOTE[1], 12, c["faint"], MONO)]
    return svg(w, h, RESEARCH_TITLE, RESEARCH_DESC, "".join(body), defs)


def research_mobile(c):
    w, h = 560, 900
    defs, field = backdrop(w, h, c, 16)
    body = [field, research_head(c, 28, 532, 44),
            text(28, 156, "How often do SQL execution rewards", 22, c["muted"]),
            text(28, 186, "accept wrong queries, and does it", 22, c["muted"]),
            text(28, 216, "change what a small agent learns?", 22, c["muted"]),
            bars(c, 28, 272, 300, 172, 44, 18), facts(c, 28, 560, 19, 76)]
    body += [text(28, 820 + 24 * i, s, 15, c["faint"], MONO) for i, s in enumerate(
        ("Registered seeds. Averaged over 200 draws,", "targeted-4 beats random-4 by 0.25 pts on",
         "dev-A and 1.57 pts on held-out schemas."))]
    return svg(w, h, RESEARCH_TITLE, RESEARCH_DESC, "".join(body), defs)
