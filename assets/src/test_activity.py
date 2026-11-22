"""Checks for the activity feed selection and rendering helpers.

Run: python3 assets/src/test_activity.py  (also collected by pytest)
"""

from datetime import date, timedelta

from activity_data import pick_feed, streaks
from activity_render import axis, md, weekly


def entry(repo, date, title="feat: ship it"):
    return {"repo": repo, "date": date, "title": title, "url": f"https://github.com/{repo}"}


def test_feed_puts_upstream_first_and_keeps_one_entry_per_repo():
    prs = [entry("shro-2002/a", "2026-11-20"), entry("other/lib", "2026-01-01")]
    commits = [entry("shro-2002/a", "2026-11-21"), entry("shro-2002/b", "2026-11-19")]
    feed = pick_feed(prs, [], commits)
    assert [e["repo"] for e in feed] == ["other/lib", "shro-2002/a", "shro-2002/b"]
    assert feed[0]["kind"] == "Upstream PR merged"
    assert feed[1]["kind"] == "Commit"


def test_feed_drops_housekeeping_and_caps_length():
    commits = [entry(f"shro-2002/r{i}", f"2026-11-{10 + i}") for i in range(6)]
    commits.append(entry("shro-2002/bot", "2026-11-30", "chore(deps): bump x"))
    feed = pick_feed([], [], commits)
    assert len(feed) == 4
    assert all(e["repo"] != "shro-2002/bot" for e in feed)


def test_markdown_escaping_neutralises_links_and_html():
    assert md("[x](y) <b>_a_|") == r"\[x\](y) &lt;b&gt;\_a\_\|"


def test_axis_covers_peak_with_round_integer_ticks():
    for peak in (0, 1, 7, 83, 136, 412, 999):
        step, ticks = axis(peak)
        assert ticks <= 4 and step * ticks >= peak and float(step).is_integer()



def test_weekly_keeps_only_complete_sunday_weeks():
    first = date(2026, 11, 4)  # a Wednesday: its week is partial, as is the week holding the last day
    days = [{"date": (first + timedelta(days=i)).isoformat(), "count": 1} for i in range(20)]
    assert weekly(days) == [(date(2026, 11, 8), 7), (date(2026, 11, 15), 7)]


def test_streaks_ignore_a_quiet_today():
    assert streaks([1, 1, 0, 1, 1, 1, 0]) == (3, 3)
    assert streaks([1, 0, 1, 1, 1, 1]) == (4, 4)
    assert streaks([1, 1, 0, 0]) == (0, 2)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
    print("activity tests passed")
