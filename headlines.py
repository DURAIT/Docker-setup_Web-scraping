#!/usr/bin/env python3
"""Print the top 5 headlines from bbc.com/news.

Usage:
    python headlines.py            # print the headlines
    python headlines.py --inspect  # show which tags/attributes the page uses,
                                   # to re-verify the selector if BBC changes its markup
"""
import sys
from collections import Counter

import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en;q=0.9",
}

# Headline selector: BBC's card components put each headline in an <h2> (or <h3>)
# tagged data-testid="card-headline". Falling back to bare <h2>/<h3> if the
# attribute ever disappears.
PRIMARY_SELECTOR = '[data-testid="card-headline"]'
FALLBACK_SELECTOR = "h2, h3"


def fetch_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=15)
    if response.status_code != 200:
        sys.exit(f"Request failed: HTTP {response.status_code} for {url}")
    return response.text


def extract_headlines(html: str, limit: int = 5) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.select(PRIMARY_SELECTOR) or soup.select(FALLBACK_SELECTOR)

    headlines, seen = [], set()
    for el in elements:
        text = " ".join(el.get_text().split())  # strip + collapse whitespace
        if not text or text in seen:
            continue
        seen.add(text)
        headlines.append(text)
        if len(headlines) == limit:
            break
    return headlines


def inspect(html: str) -> None:
    soup = BeautifulSoup(html, "html.parser")
    print("Heading tags:", {t: len(soup.find_all(t)) for t in ("h1", "h2", "h3")})
    testids = Counter(e["data-testid"] for e in soup.find_all(attrs={"data-testid": True}))
    print("Most common data-testid values:")
    for name, count in testids.most_common(10):
        print(f"  {count:3d}  {name}")
    print("Sample matches for", PRIMARY_SELECTOR)
    for el in soup.select(PRIMARY_SELECTOR)[:3]:
        print(f"  <{el.name}> {' '.join(el.get_text().split())[:80]}")


def main() -> None:
    try:
        html = fetch_html(URL)
    except requests.RequestException as exc:
        sys.exit(f"Could not fetch {URL}: {exc}")

    if "--inspect" in sys.argv:
        inspect(html)
        return

    headlines = extract_headlines(html)
    if not headlines:
        sys.exit("No headlines found. The page layout may have changed; try --inspect.")

    for i, title in enumerate(headlines, start=1):
        print(f"{i}. {title}")
    if len(headlines) < 5:
        print(f"(Only {len(headlines)} headline(s) found.)")


if __name__ == "__main__":
    main()