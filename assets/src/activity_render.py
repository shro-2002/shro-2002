"""Render the activity dashboard SVGs and the README activity block from assets/activity/data.json.

Run: python3 assets/src/activity_render.py  (after activity_data.py)
Output depends only on data.json, so an unchanged day produces byte-identical files and no commit.
"""

import html
import json
import math
import re
from datetime import date

from activity_data import DATA, is_own_repo
from kit import ASSETS, MONO, SANS, THEMES, backdrop, chamfer, label, pill, svg, text

README = ASSETS.parent / "README.md"
BLOCK = re.compile(r"<!-- activity:start -->.*?<!-- activity:end -->", re.S)
# Live dot pulses unless the viewer asked for reduced motion.
PULSE = ("<style>@keyframes pulse{0%,100%{opacity:1}50%{opacity:.2}}.pulse{animation:pulse 2.4s ease-in-out infinite}"
         "@media (prefers-reduced-motion: reduce){.pulse{animation:none}}</style>")
TITLE = "Engineering activity: building in public"


def summary(data):
    cal, prs = data["calendar"], data["prs"]
    peak = max(cal["days"], key=lambda d: d["count"])
    upstream = sum(not is_own_repo(p["repo"]) for p in prs)
    return {"cal": cal, "prs": len(prs), "upstream": upstream, "peak": peak, "updated": data["updated"]}


def describe(s):
    cal, peak = s["cal"], s["peak"]
    return (f"Daily public GitHub contributions over the last 12 weeks, peaking at {peak['count']} on "
            f"{peak['date']}; {cal['last30']} in the last 30 days. Last 12 months: {cal['total']} contributions, "
            f"{cal['commits']} commits, {s['prs']} pull requests merged ({s['upstream']} upstream), commits in "
            f"{cal['repos_with_commits']} repositories. Data as of {s['updated']}.")


def axis(vmax):
    """Round tick step and tick count (at most 4 intervals) that just covers vmax."""
    vmax = max(vmax, 1)
    mag = max(10 ** math.floor(math.log10(vmax / 4)), 1)
    mults = (1, 2, 5, 10) if mag == 1 else (1, 2, 2.5, 5, 10)
    steps = [m * mag for m in mults if math.ceil(vmax / (m * mag)) <= 4]
    step = min(steps, key=lambda st: (st * math.ceil(vmax / st), st))
    return step, math.ceil(vmax / step)


def chart(days, c, box, size):
    """Daily bars inside box=(x, y, w, h); left gutter holds the axis labels, months sit below."""
    x, y, w, h = box
    gutter = size * 2.6
    step, ticks = axis(max(d["count"] for d in days))
    top = step * ticks
    parts = []
    for i in range(ticks + 1):
        yy = y + h - h * i / ticks
        parts += [f'<line x1="{x + gutter}" y1="{yy:.1f}" x2="{x + w}" y2="{yy:.1f}" stroke="{c["border"]}"/>',
                  text(x, yy + size * 0.35, f"{step * i:g}", size, c["faint"], MONO)]
    slot = (w - gutter) / len(days)
    for i, d in enumerate(days):
        bx = x + gutter + i * slot + slot * 0.2
        bh = max(h * min(d["count"], top) / top, 1.5)
        recent = i >= len(days) - 7
        parts.append(f'<rect x="{bx:.1f}" y="{y + h - bh:.1f}" width="{slot * 0.6:.1f}" height="{bh:.1f}" rx="1" '
                     f'fill="{c["amber"] if recent else c["cyan"]}" fill-opacity="{1 if d["count"] else 0.35}"/>')
        if d["date"].endswith("-01"):
            month = date.fromisoformat(d["date"]).strftime("%b").upper()
            parts.append(text(bx, y + h + size * 1.7, month, size, c["faint"], MONO, 500, 1.2))
    return "".join(parts)


def head(c, x, right, tag, pill_text, small):
    dot_x = right - round(len(pill_text) * small * 0.78 + 20) - small
    return "".join([
        f'<rect x="{x - 8}" y="0.5" width="150" height="3" fill="{c["cyan"]}"/>',
        text(x, 52, tag, small, c["cyan"], MONO, 600, 2.4),
        f'<circle class="pulse" cx="{dot_x}" cy="{52 - small * 0.35:.0f}" r="{small * 0.32:.1f}" fill="{c["green"]}"/>',
        pill(right, 52 - small - 6, pill_text, c["green"], small),
    ])


def desktop(s, c):
    w, h = 1200, 560
    defs, field = backdrop(w, h, c)
    cal = s["cal"]
    tiles = [(cal["total"], "contributions"), (cal["commits"], "commits"),
             (s["prs"], f"PRs merged · {s['upstream']} upstream"), (cal["repos_with_commits"], "repos with commits")]
    body = [field, head(c, 40, 1160, "ENGINEERING ACTIVITY  /  BUILDING IN PUBLIC", "LIVE · REFRESHED DAILY", 14),
            text(37, 116, "AI engineering telemetry", 44, c["text"], SANS, 700, -1),
            text(40, 152, "Public GitHub activity, rebuilt every day by GitHub Actions from the GitHub API.", 19,
                 c["muted"]),
            chamfer(40, 184, 744, 300, c), label(64, 222, "CONTRIBUTIONS / DAY · LAST 12 WEEKS", c["faint"]),
            text(760, 222, f"{cal['last30']} IN THE LAST 30 DAYS", 14, c["cyan"], MONO, 600, 1.4, "end"),
            chart(cal["days"], c, (64, 252, 696, 176), 14), label(816, 222, "LAST 12 MONTHS", c["faint"])]
    for i, (value, name) in enumerate(tiles):
        y = 274 + i * 66
        body += [text(816, y, f"{value:,}", 32, c["amber"] if i == 0 else c["text"], SANS, 700, -0.5),
                 text(816, y + 24, name, 16, c["muted"])]
    body.append(text(40, 532, f"SOURCE  GITHUB API · PUBLIC DATA ONLY · DATA AS OF {s['updated']}", 14, c["faint"],
                     MONO, 500, 1.4))
    return svg(w, h, TITLE, describe(s), "".join(body), defs + PULSE)


def mobile(s, c):
    w, h = 560, 1040
    defs, field = backdrop(w, h, c, 16)
    cal = s["cal"]
    tiles = [(cal["total"], ("contributions,", "last 12 months")), (cal["commits"], ("commits,", "last 12 months")),
             (s["prs"], ("PRs merged,", f"{s['upstream']} upstream")), (cal["repos_with_commits"], ("repos with", "commits"))]
    body = [field, head(c, 28, 532, "BUILDING IN PUBLIC", "LIVE · DAILY", 20),
            text(25, 112, "AI engineering telemetry", 36, c["text"], SANS, 700, -1),
            text(28, 152, "Public GitHub activity, rebuilt", 22, c["muted"]),
            text(28, 182, "every day by GitHub Actions.", 22, c["muted"]),
            chamfer(16, 212, 528, 400, c, 16), label(40, 254, "CONTRIBUTIONS / DAY", c["faint"], 20),
            text(40, 288, f"Last 12 weeks · {cal['last30']} in 30 days", 22, c["cyan"], SANS, 600),
            chart(cal["days"], c, (40, 318, 480, 220), 20)]
    for i, (value, lines) in enumerate(tiles):
        x, y = 28 + (i % 2) * 264, 690 + (i // 2) * 136
        body += [text(x, y, f"{value:,}", 40, c["amber"] if i == 0 else c["text"], SANS, 700, -0.5)]
        body += [text(x, y + 32 + 26 * j, line, 21, c["muted"]) for j, line in enumerate(lines)]
    body += [f'<line x1="28" y1="{y}" x2="532" y2="{y}" stroke="{c["border"]}"/>' for y in (634, 900)]
    body += [text(28, 952, "PUBLIC DATA ONLY · GITHUB API", 20, c["faint"], MONO, 500, 1.2),
             text(28, 984, f"DATA AS OF {s['updated']}", 20, c["faint"], MONO, 500, 1.2)]
    return svg(w, h, TITLE, describe(s), "".join(body), defs + PULSE)


def md(s):
    """Escape public titles for a Markdown list item."""
    return re.sub(r"([\\`*_\[\]|#~])", r"\\\1", html.escape(s, quote=False))


def feed_line(e):
    name = e["repo"].split("/", 1)[1] if is_own_repo(e["repo"]) else e["repo"]
    ref = re.search(r"/pull/(\d+)$", e["url"])
    link = f"{name}#{ref.group(1)}" if ref else name
    return f"- **{e['date']} · {e['kind']}** · [{md(link)}]({e['url']}): {md(e['title'])}"


def readme_block(data, s):
    sources = "".join(
        f'  <source media="{m}" srcset="assets/activity/{f}.svg">\n'
        for m, f in [("(max-width: 640px) and (prefers-color-scheme: dark)", "activity-mobile-dark"),
                     ("(max-width: 640px)", "activity-mobile-light"),
                     ("(prefers-color-scheme: dark)", "activity-dark")])
    feed = "\n".join(feed_line(e) for e in data["feed"])
    return (f"<!-- activity:start -->\n<picture>\n{sources}"
            f'  <img alt="{html.escape(describe(s))}" src="assets/activity/activity-light.svg" width="100%">\n'
            f"</picture>\n\n**Recently shipping**\n\n{feed}\n\n"
            f"<sub>Rebuilt daily by the [activity workflow](.github/workflows/activity.yml) from public GitHub data "
            f"(contribution calendar, search and events APIs). Pull requests to this profile repository, housekeeping "
            f"commits and bot commits are left out. Data as of {s['updated']}.</sub>\n<!-- activity:end -->")


def main():
    data = json.loads(DATA.read_text())
    s = summary(data)
    for theme, c in THEMES.items():
        (ASSETS / f"activity/activity-{theme}.svg").write_text(desktop(s, c))
        (ASSETS / f"activity/activity-mobile-{theme}.svg").write_text(mobile(s, c))
    readme = README.read_text()
    if not BLOCK.search(readme):
        raise SystemExit("README.md has no <!-- activity:start --> ... <!-- activity:end --> block")
    README.write_text(BLOCK.sub(lambda _: readme_block(data, s), readme))


if __name__ == "__main__":
    main()
