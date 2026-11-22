"""Build the profile artwork in dark and light variants.

Run: python3 assets/src/build.py  (writes assets/*.svg and assets/covers/*.svg)
README.md picks each variant with <picture>: (max-width: 640px) for the phone layouts,
prefers-color-scheme for the theme. Covers embed the screenshots in assets/projects/.
"""

from content import PROJECTS
from covers import cover_desktop, cover_mobile, research_desktop, research_mobile
from hero import hero_desktop, hero_mobile, shortcut
from kit import ASSETS, THEMES


def main():
    (ASSETS / "covers").mkdir(exist_ok=True)
    (ASSETS / "shortcuts").mkdir(exist_ok=True)
    for p in PROJECTS:
        (ASSETS / f"shortcuts/{p['slug']}.svg").write_text(shortcut(p))
    for theme, c in THEMES.items():
        outputs = {
            f"hero-{theme}.svg": hero_desktop(c),
            f"hero-mobile-{theme}.svg": hero_mobile(c),
            f"covers/rewardshield-{theme}.svg": research_desktop(c),
            f"covers/rewardshield-mobile-{theme}.svg": research_mobile(c),
        }
        for p in PROJECTS:
            outputs[f"covers/{p['slug']}-{theme}.svg"] = cover_desktop(p, c)
            outputs[f"covers/{p['slug']}-mobile-{theme}.svg"] = cover_mobile(p, c)
        for name, content in outputs.items():
            (ASSETS / name).write_text(content)


if __name__ == "__main__":
    main()
