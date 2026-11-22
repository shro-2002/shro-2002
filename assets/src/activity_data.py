"""Fetch public GitHub activity for the profile dashboard into assets/activity/data.json.

Run: GITHUB_TOKEN=... python3 assets/src/activity_data.py
Only public data is requested (public events, `is:public` search, public repositories);
the contribution calendar is the one GitHub shows on the profile. Each section is fetched
independently: if one fails, its previous value is kept and a warning is printed, so the
dashboard always renders from the last good data.
"""

import json
import os
import re
import sys
import time
from collections import Counter
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

from kit import ASSETS

LOGIN = "shro-2002"
PROFILE_REPO = f"{LOGIN}/{LOGIN}"
DATA = ASSETS / "activity" / "data.json"
API = "https://api.github.com"
FEED_SIZE = 4
CHART_DAYS = 84
LANGUAGE_DAYS = 90
TITLE_MAX = 90
# Housekeeping that does not show shipped work.
TRIVIAL = re.compile(r"^(merge|bump|chore|ci|style|docs|build|wip)\b|dependabot|renovate|^update readme|\[skip",
                     re.I)
CALENDAR_QUERY = """
query($login: String!, $from: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from) {
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
      totalCommitContributions
      totalRepositoriesWithContributedCommits
    }
  }
}"""


class FetchError(Exception):
    """A GitHub API call failed after retries."""


def request(url, body=None, attempts=3):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-activity",
               "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(body).encode() if body else None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.load(resp)
        except (urllib.error.URLError, TimeoutError) as err:
            status = getattr(err, "code", None)
            retryable = status is None or status in (403, 429) or status >= 500
            if attempt == attempts - 1 or not retryable:
                raise FetchError(f"{url}: {err}") from err
            time.sleep(2 ** attempt * 3)


def graphql(query, variables):
    result = request(f"{API}/graphql", {"query": query, "variables": variables})
    if result.get("errors"):
        raise FetchError(f"graphql: {result['errors'][0].get('message')}")
    return result["data"]


def streaks(counts):
    """(current, longest) runs of days with contributions; a quiet today does not end the current run."""
    longest = run = 0
    for n in counts:
        run = run + 1 if n else 0
        longest = max(longest, run)
    current = 0
    for n in reversed(counts[:-1] if counts and not counts[-1] else counts):
        if not n:
            break
        current += 1
    return current, longest


def fetch_calendar(now):
    since = (now - timedelta(days=365)).strftime("%Y-%m-%dT00:00:00Z")
    coll = graphql(CALENDAR_QUERY, {"login": LOGIN, "from": since})["user"]["contributionsCollection"]
    cal = coll["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    cutoff = (now - timedelta(days=30)).date().isoformat()
    current, longest = streaks([d["contributionCount"] for d in days])
    return {
        "streak": current,
        "longest_streak": longest,
        "days": [{"date": d["date"], "count": d["contributionCount"]} for d in days[-CHART_DAYS:]],
        "total": cal["totalContributions"],
        "last30": sum(d["contributionCount"] for d in days if d["date"] > cutoff),
        "commits": coll["totalCommitContributions"],
        "repos_with_commits": coll["totalRepositoriesWithContributedCommits"],
    }


def is_own_repo(repo):
    return repo.startswith(f"{LOGIN}/")


def repo_name(url):
    return url.split("/repos/", 1)[1]


def fetch_prs(now):
    since = (now - timedelta(days=365)).date().isoformat()
    q = f"author:{LOGIN} is:pr is:merged is:public merged:>={since}"
    items = request(f"{API}/search/issues?per_page=100&sort=updated&q={urllib.request.quote(q)}")["items"]
    prs = [{"repo": repo_name(i["repository_url"]), "number": i["number"], "title": i["title"],
            "url": i["html_url"], "date": i["closed_at"][:10]} for i in items]
    return [p for p in prs if p["repo"] != PROFILE_REPO]


def fetch_releases():
    events = request(f"{API}/users/{LOGIN}/events/public?per_page=100")
    return [{"repo": e["repo"]["name"], "title": e["payload"]["release"].get("name") or e["payload"]["release"]["tag_name"],
             "url": e["payload"]["release"]["html_url"], "date": e["created_at"][:10]}
            for e in events if e["type"] == "ReleaseEvent" and e["payload"].get("action") == "published"]


def public_repos():
    """LOGIN's own public, non-fork, non-archived repositories, most recently pushed first."""
    repos = request(f"{API}/users/{LOGIN}/repos?type=owner&sort=pushed&per_page=30")
    return [r for r in repos
            if not (r["fork"] or r["archived"] or r["private"] or r["full_name"] == PROFILE_REPO)]


def fetch_languages(now):
    """Primary language of each repository pushed in the last LANGUAGE_DAYS, counted per repository (not bytes)."""
    cutoff = (now - timedelta(days=LANGUAGE_DAYS)).isoformat()
    counts = Counter(r["language"] for r in public_repos() if r["language"] and r["pushed_at"] >= cutoff)
    return [[lang, n] for lang, n in counts.most_common(3)]


def fetch_commits(limit=6):
    """Latest non-trivial commit by LOGIN in each recently pushed public, non-fork repository."""
    picked = []
    for r in public_repos()[:15]:
        commits = request(f"{API}/repos/{r['full_name']}/commits?author={LOGIN}&per_page=15")
        subject = next((c for c in commits if not TRIVIAL.search(c["commit"]["message"].splitlines()[0])), None)
        if subject:
            picked.append({"repo": r["full_name"], "title": subject["commit"]["message"].splitlines()[0],
                           "url": subject["html_url"], "date": subject["commit"]["author"]["date"][:10]})
        if len(picked) == limit:
            break
    return picked


def pick_feed(prs, releases, commits):
    """Upstream merged PRs first (up to two), then everything else newest first, one entry per repository."""
    upstream = [dict(p, kind="Upstream PR merged") for p in prs if not is_own_repo(p["repo"])][:2]
    rest = ([dict(p, kind="PR merged") for p in prs if is_own_repo(p["repo"])]
            + [dict(r, kind="Release") for r in releases] + [dict(c, kind="Commit") for c in commits])
    rest = [e for e in rest if not TRIVIAL.search(e["title"])]
    feed, seen = [], set()
    for entry in upstream + sorted(rest, key=lambda e: e["date"], reverse=True):
        if entry["repo"] in seen:
            continue
        seen.add(entry["repo"])
        feed.append({"date": entry["date"], "kind": entry["kind"], "repo": entry["repo"],
                     "title": entry["title"][:TITLE_MAX], "url": entry["url"]})
    return feed[:FEED_SIZE]


def section(name, fn, old):
    try:
        return fn()
    except (FetchError, KeyError, TypeError, ValueError) as err:
        print(f"::warning::activity {name} not refreshed, keeping last good data: {err}")
        return old.get(name)


def main():
    now = datetime.now(timezone.utc)
    old = json.loads(DATA.read_text()) if DATA.exists() else {}
    calendar = section("calendar", lambda: fetch_calendar(now), old)
    prs = section("prs", lambda: fetch_prs(now), old)
    feed = section("feed", lambda: pick_feed(prs or [], fetch_releases(), fetch_commits()), old)
    languages = section("languages", lambda: fetch_languages(now), old)
    new = {"calendar": calendar, "prs": prs, "feed": feed, "languages": languages}
    if None in new.values():
        sys.exit("activity: no data yet for " + ", ".join(k for k, v in new.items() if v is None))
    changed = {k: v for k, v in old.items() if k != "updated"} != new
    updated = now.date().isoformat() if changed else old["updated"]
    DATA.parent.mkdir(exist_ok=True)
    DATA.write_text(json.dumps(new | {"updated": updated}, indent=1, ensure_ascii=False) + "\n")
    print(f"activity: data {'changed' if changed else 'unchanged'}, as of {updated}")


if __name__ == "__main__":
    main()
