"""Project covers (real screenshot + evidence column) and the RewardShield research card."""

from content import REWARD_BARS, REWARD_FACTS, REWARD_NOTE
from kit import MONO, SANS, backdrop, label, pill, screenshot, svg, text


def metric_lines(p, phone=False):
    """(value, label lines) per metric; the phone layout takes a metric's narrower lines where it has them."""
    return [(value, narrow[0] if phone and narrow else lines) for value, lines, *narrow in p["metrics"]]


def cover_desc(p):
    metrics = "; ".join(f"{value} {' '.join(lines)}" for value, lines in metric_lines(p))
    return f"{p['name']}: {' '.join(p['pitch_lines'])} Evidence: {metrics}. Status: {p['status'].lower()}."


def header(p, c, x, right, y, name_size, name_y, small=14):
    col = c[p["accent"]]
    return "".join([
        f'<rect x="{x - 8}" y="0.5" width="150" height="3" fill="{col}"/>',
        text(x, y, f"{p['num']}  /  FLAGSHIP", small, col, MONO, 600, 2.4),
        pill(right, y - small - 6, p["status"], col, small),
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
    # Two label lines per metric is the base layout; each extra line tightens the column to make room.
    metrics = metric_lines(p)
    extra = sum(len(lines) for _, lines in metrics) - 2 * len(metrics)
    y = 286 - 10 * extra
    for i, (value, lines) in enumerate(metrics):
        body.append(metric_block(value, lines, c, 784, y, c["text"] if i else col))
        y += 62 + 21 * len(lines)
        body.append(f'<line x1="784" y1="{y - 38}" x2="1160" y2="{y - 38}" stroke="{c["border"]}"/>')
    body += [text(784, 588 + 11 * extra + 20 * i, s, 14, c["faint"], MONO, 500) for i, s in enumerate(p["stack"])]
    return svg(w, h, p["name"], cover_desc(p), "".join(body), defs)


def cover_mobile(p, c):
    metrics = metric_lines(p, phone=True)
    w, h = 560, 618 + sum(38 + 28 * len(lines) for _, lines in metrics)
    defs, field = backdrop(w, h, c, 16)
    col = c[p["accent"]]
    body = [field, header(p, c, 28, 532, 52, 44, 114, 20), label(28, 150, p["category"], col, 20),
            text(28, 190, p["pitch_lines"][0], 22, c["muted"]), text(28, 220, p["pitch_lines"][1], 22, c["muted"]),
            screenshot(p["shot"], 28, 248, 504, 284, c, f"m-{p['slug']}")]
    y = 598
    for i, (value, lines) in enumerate(metrics):
        body.append(text(28, y, value, 28, c["text"] if i else col, SANS, 700, -0.5))
        body += [text(236, y - 16 + 28 * j, s, 21, c["muted"]) for j, s in enumerate(lines)]
        y += 38 + 28 * len(lines)
        body.append(f'<line x1="28" y1="{y - 58}" x2="532" y2="{y - 58}" stroke="{c["border"]}"/>')
    body.append(text(28, h - 22, p["stack"][0], 20, c["faint"], MONO, 500))
    return svg(w, h, p["name"], cover_desc(p), "".join(body), defs)


RESEARCH_TITLE = "RewardShield — research"
RESEARCH_DESC = (
    "RewardShield, a pre-registered study of how often SQL execution rewards accept wrong queries. "
    "False-accept share on the dev-A audit split: " + "; ".join(f"{n} ({d}) {v}%" for n, d, v in REWARD_BARS)
    + ". " + " ".join(" ".join(f) for f in REWARD_FACTS) + " " + " ".join(REWARD_NOTE)
)


def bars(c, x_label, x_bar, y0, max_w, step=32, size=14, show_dbs=True):
    title = "FALSE-ACCEPT SHARE · DEV-A · LOWER IS BETTER" if show_dbs else "FALSE-ACCEPT SHARE (LOWER WINS)"
    parts = [label(x_label, y0 - 34, title, c["faint"], 14 if show_dbs else size - 2)]
    for i, (name, dbs, value) in enumerate(REWARD_BARS):
        y = y0 + i * step
        best = name == "targeted-4"
        fill = c["cyan"] if best else c["faint"]
        bw = round(max_w * value / 4.5)
        parts += [text(x_label, y + 5, name, size, c["text"] if best else c["muted"], MONO, 600 if best else 400),
                  text(x_bar - 12, y + 5, dbs, 14, c["faint"], MONO, 400, 0, "end") if show_dbs else "",
                  f'<rect x="{x_bar}" y="{y - size * 0.6:.0f}" width="{bw}" height="{size}" rx="3" fill="{fill}" '
                  f'fill-opacity="{1 if best else 0.55}"/>',
                  text(x_bar + bw + 10, y + 5, f"{value:.2f}%", size, c["text"] if best else c["muted"], MONO,
                       600 if best else 400)]
    return "".join(parts)


def research_head(c, x, right, title_size, small=14, tag="RESEARCH  /  OPEN SOURCE"):
    return "".join([
        f'<rect x="{x - 8}" y="0.5" width="150" height="3" fill="{c["cyan"]}"/>',
        text(x, 56, tag, small, c["cyan"], MONO, 600, 2.4),
        pill(right, 56 - small - 6, "PRE-REGISTERED", c["cyan"], small),
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
            text(640, 402, REWARD_NOTE[0], 14, c["faint"], MONO), text(640, 422, REWARD_NOTE[1], 14, c["faint"], MONO)]
    return svg(w, h, RESEARCH_TITLE, RESEARCH_DESC, "".join(body), defs)


def research_mobile(c):
    w, h = 560, 900
    defs, field = backdrop(w, h, c, 16)
    body = [field, research_head(c, 28, 532, 44, 20, "RESEARCH"),
            text(28, 156, "How often do SQL execution rewards", 22, c["muted"]),
            text(28, 186, "accept wrong queries, and does it", 22, c["muted"]),
            text(28, 216, "change what a small agent learns?", 22, c["muted"]),
            bars(c, 28, 248, 300, 210, 48, 22, show_dbs=False), facts(c, 28, 572, 21, 80)]
    body += [text(28, 800 + 26 * i, s, 20, c["faint"], MONO) for i, s in enumerate(
        ("Registered seeds. Averaged over", "200 draws, targeted-4 beats", "random-4 by 0.25 pts on dev-A",
         "and 1.57 pts on held-out schemas."))]
    return svg(w, h, RESEARCH_TITLE, RESEARCH_DESC, "".join(body), defs)
