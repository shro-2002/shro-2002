"""Render the activity dashboard SVGs and the README activity block from assets/activity/data.json.

Run: python3 assets/src/activity_render.py  (after activity_data.py)
Output depends only on data.json, so an unchanged day produces byte-identical files and no commit.
"""

import html
import json
import math
import re
from datetime import date, timedelta

from activity_data import DATA, is_own_repo
from kit import ASSETS, MONO, SANS, THEMES, backdrop, svg, text

README = ASSETS.parent / "README.md"
BLOCK = re.compile(r"<!-- activity:start -->.*?<!-- activity:end -->", re.S)
# Live dot pulses unless the viewer asked for reduced motion.
PULSE = ("<style>@keyframes pulse{0%,100%{opacity:1}50%{opacity:.2}}.pulse{animation:pulse 2.4s ease-in-out infinite}"
         "@media (prefers-reduced-motion: reduce){.pulse{animation:none}}</style>")
TITLE = "Recent public GitHub activity"


def weekly(days, weeks=8):
    """Totals for the last `weeks` complete Sunday-to-Saturday weeks (GitHub's calendar weeks)."""
    buckets = {}
    for d in days:
        day = date.fromisoformat(d["date"])
        buckets.setdefault(day - timedelta(days=(day.weekday() + 1) % 7), []).append(d["count"])
    return [(start, sum(v)) for start, v in sorted(buckets.items()) if len(v) == 7][-weeks:]


def short(s, limit):
    return s if len(s) <= limit else s[:limit - 1].rstrip() + "…"


def period(weeks):
    """The charted window as text, first day to last day: 'Sep 27 – Nov 21, 2026'."""
    first, last = weeks[0][0], weeks[-1][0] + timedelta(days=6)
    return f"{first:%b} {first.day} – {last:%b} {last.day}, {last.year}"


def summary(data):
    cal, prs = data["calendar"], data["prs"]
    weeks = weekly(cal["days"])
    return {"weeks": weeks, "period": period(weeks), "headline": f"The last {len(weeks)} weeks, in context.",
            "in_window": sum(n for _, n in weeks), "total": cal["total"], "prs": len(prs),
            "upstream": [p for p in prs if not is_own_repo(p["repo"])], "updated": data["updated"]}


def describe(s):
    weeks = s["weeks"]
    trend = ", ".join(f"{start:%b} {start.day}: {n}" for start, n in weeks)
    return (f"Weekly public GitHub contributions for the last {len(weeks)} complete weeks, {s['period']} ({trend}). "
            f"These weeks hold {s['in_window']} of the {s['total']} public contributions in the last 12 months. "
            f"{s['prs']} pull requests merged in 12 months, {len(s['upstream'])} upstream. "
            f"Data as of {s['updated']}.")


def tiles(s):
    """(icon, title, value line) for the two tiles under the chart: the window in context, and upstream work."""
    up = s["upstream"]
    open_source = "No upstream PRs merged in 12 months"
    if up:
        more = f" + {len(up) - 1} more" if len(up) > 1 else ""
        open_source = f"{up[0]['repo'].split('/')[-1]} #{up[0]['number']}{more} merged upstream"
    return [("bars", "Share of the last 12 months",
             f"{s['in_window']} of {s['total']} contributions in these {len(s['weeks'])} weeks"),
            ("pr", "Open source", open_source)]


def icon(kind, x, y, colour):
    """22-unit line icons drawn at (x, y) top-left."""
    st = f'fill="none" stroke="{colour}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    paths = {
        "pr": (f'<circle cx="{x + 5}" cy="{y + 4}" r="3" {st}/><circle cx="{x + 5}" cy="{y + 18}" r="3" {st}/>'
               f'<circle cx="{x + 17}" cy="{y + 18}" r="3" {st}/><path d="M{x + 5} {y + 7}v8M{x + 17} {y + 15}V{y + 9}a3 3 0 0 0-3-3h-4" {st}/>'),
        "bars": f'<path d="M{x + 1} {y + 21}h20M{x + 4} {y + 18}v-5M{x + 9} {y + 18}v-9M{x + 14} {y + 18}v-6M{x + 19} {y + 18}V{y + 3}" {st}/>',
    }
    return paths[kind]


def live_icon(x, y, size, c):
    st = f'fill="none" stroke="{c["green"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'
    return (f'<g class="pulse"><rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * 0.22:.0f}" {st}/>'
            f'<path d="M{x + size * .2:.1f} {y + size * .62:.1f}l{size * .2:.1f}-{size * .22:.1f} {size * .16:.1f} '
            f'{size * .16:.1f} {size * .24:.1f}-{size * .3:.1f}" {st}/></g>')


def axis(vmax):
    """Round tick step and tick count (at most 4 intervals) that just covers vmax."""
    vmax = max(vmax, 1)
    mag = max(10 ** math.floor(math.log10(vmax / 4)), 1)
    mults = (1, 2, 5, 10) if mag == 1 else (1, 2, 2.5, 5, 10)
    steps = [m * mag for m in mults if math.ceil(vmax / (m * mag)) <= 4]
    step = min(steps, key=lambda st: (st * math.ceil(vmax / st), st))
    return step, math.ceil(vmax / step)


def line_chart(weeks, c, box, size, label_every=1):
    """Weekly totals as a ringed-point line over a soft area, inside box=(x, y, w, h)."""
    x, y, w, h = box
    step, ticks = axis(max(n for _, n in weeks))
    top = step * ticks
    parts = [f'<linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["cyan"]}" '
             f'stop-opacity="0.22"/><stop offset="1" stop-color="{c["cyan"]}" stop-opacity="0"/></linearGradient>']
    for i in range(ticks + 1):
        yy = y + h - h * i / ticks
        parts += [f'<line x1="{x}" y1="{yy:.1f}" x2="{x + w}" y2="{yy:.1f}" stroke="{c["border"]}" stroke-dasharray="2 6"/>',
                  text(x - size * 0.8, yy + size * 0.35, f"{step * i:g}", size, c["faint"], SANS, 400, 0, "end")]
    gap = w / (len(weeks) - 1)
    pts = [(x + i * gap, y + h - h * n / top) for i, (_, n) in enumerate(weeks)]
    line = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    parts += [f'<polygon points="{x},{y + h} {line} {x + w},{y + h}" fill="url(#area)"/>',
              f'<polyline points="{line}" fill="none" stroke="{c["cyan"]}" stroke-width="3" stroke-linejoin="round"/>']
    for i, ((px, py), (start, n)) in enumerate(zip(pts, weeks)):
        parts += [f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{size * 0.4:.1f}" fill="{c["cyan"]}" stroke="{c["text"]}" '
                  f'stroke-width="2.5"/>',
                  text(px, py - size * 0.95, str(n), size, c["muted"], SANS, 600, 0, "middle")]
        if (len(weeks) - 1 - i) % label_every == 0:
            parts.append(text(px, y + h + size * 1.9, f"{start:%b} {start.day}", size, c["faint"], SANS, 400, 0, "middle"))
    return "".join(parts)


def tile(t, c, box, size, limit):
    kind, title, value = t
    x, y, w, h = box
    return "".join([f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{c["panel"]}" stroke="{c["border"]}"/>',
                    icon(kind, x + 24, y + 22, c["muted"]),
                    text(x + 24, y + 22 + size * 2.55, title, size * 1.3, c["text"], SANS, 600),
                    text(x + 24, y + 22 + size * 4.15, short(value, limit), size, c["muted"])])


def desktop(s, c):
    w, h = 1200, 784
    defs, field = backdrop(w, h, c, 22)
    body = [field, text(40, 54, f"SHRO-2002 / PUBLIC ACTIVITY · {s['period'].upper()}", 15, c["muted"], MONO, 500, 2),
            text(38, 104, s["headline"], 40, c["text"], SANS, 700, -0.8),
            live_icon(1124, 34, 36, c), line_chart(s["weeks"], c, (110, 172, 1040, 370), 18),
            text(40, 628, f"Weekly public contributions, {len(s['weeks'])} complete weeks · GitHub's graph below shows "
                          f"the full year · data as of {s['updated']}", 16, c["muted"])]
    for i, t in enumerate(tiles(s)):
        body.append(tile(t, c, (40 + i * 566, 656, 554, 104), 16, 62))
    return svg(w, h, TITLE, describe(s), "".join(body), defs + PULSE)


def mobile(s, c):
    w, h = 560, 884
    defs, field = backdrop(w, h, c, 18)
    body = [field, text(28, 50, s["period"].upper(), 20, c["muted"], MONO, 500, 1.6),
            text(26, 104, s["headline"], 36, c["text"], SANS, 700, -0.6),
            live_icon(492, 26, 40, c), line_chart(s["weeks"], c, (88, 176, 432, 300), 21, label_every=2),
            text(28, 562, f"Weekly public contributions, {len(s['weeks'])}", 21, c["muted"]),
            text(28, 590, f"complete weeks · data as of {s['updated']}", 21, c["muted"])]
    for i, t in enumerate(tiles(s)):
        body.append(tile(t, c, (16, 618 + i * 126, 528, 114), 21, 41))
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
            f"The chart covers {s['period']} only; those weeks hold {s['in_window']} of my {s['total']} public "
            f"contributions in the last 12 months, and GitHub's own graph under this README shows the full year. "
            f"Rebuilt daily by the [activity workflow](.github/workflows/activity.yml) from public GitHub data; pull "
            f"requests to this profile repository, housekeeping commits and bot commits are left out. Data as of "
            f"{s['updated']}.\n<!-- activity:end -->")


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
