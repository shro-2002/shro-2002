"""Fail if any artwork text renders too small to read on GitHub.

GitHub draws README images ~324 CSS px wide on a 390px phone and ~850 px wide on a
1440px desktop, so a 560-unit phone SVG is scaled by 324/560 and a 1200-unit desktop
SVG by 850/1200. Run: python3 assets/src/check_sizes.py
"""

import re
import sys

from kit import ASSETS

# (glob, rendered width in CSS px, minimum readable text size in CSS px)
TARGETS = [("**/*mobile-dark.svg", 324, 11.5), ("**/*[!e]-dark.svg", 850, 9.9)]


def smallest(path, img_px):
    src = path.read_text()
    width = float(re.search(r'viewBox="0 0 ([\d.]+)', src).group(1))
    sizes = [float(s) for s in re.findall(r'<text[^>]*font-size="([\d.]+)"', src)]
    return min(sizes) * img_px / width


def main():
    bad = []
    for pattern, img_px, min_px in TARGETS:
        for path in sorted(ASSETS.glob(pattern)):
            px = smallest(path, img_px)
            print(f"{px:5.1f}px  {path.relative_to(ASSETS)}")
            if px < min_px:
                bad.append(f"{path.name} ({px:.1f}px < {min_px}px)")
    if bad:
        sys.exit("text too small: " + ", ".join(bad))


if __name__ == "__main__":
    main()
