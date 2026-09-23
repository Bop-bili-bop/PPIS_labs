"""Extract h1, h2 and h3 headings from web pages."""

from __future__ import annotations

import argparse
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

USER_AGENT = "PIIS-University-Lab/1.0 (educational heading parser)"


class ScraperError(RuntimeError):
    """A controlled URL, network, or parsing error."""


def validate_url(url: str) -> None:
    """Accept only absolute HTTP(S) URLs."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("URL must be an absolute http:// or https:// address.")


def parse_headings(html: str) -> list[dict[str, str]]:
    """Parse h1/h2/h3 elements from HTML without performing a network call."""
    soup = BeautifulSoup(html, "html.parser")
    return [
        {"level": heading.name, "text": heading.get_text(" ", strip=True)}
        for heading in soup.select("h1, h2, h3")
    ]


def get_headings(url: str, timeout: float = 10.0) -> list[dict[str, str]]:
    """Download *url* and return its h1/h2/h3 headings."""
    validate_url(url)
    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=timeout,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ScraperError(f"Could not retrieve {url}: {exc}") from exc
    return parse_headings(response.text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract h1-h3 page headings.")
    parser.add_argument("url", nargs="?", default="https://example.com")
    args = parser.parse_args()
    try:
        headings = get_headings(args.url)
    except (ValueError, ScraperError) as exc:
        print(f"Error: {exc}")
        return 1

    if not headings:
        print("No h1, h2 or h3 headings found.")
    else:
        for heading in headings:
            print(f"{heading['level']}: {heading['text']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
