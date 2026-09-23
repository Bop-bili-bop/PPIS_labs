"""Flask demonstration application for PIIS laboratory work №5."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request

try:
    from .data_analysis import analyze_csv
    from .web_scraper import ScraperError, get_headings
except ImportError:  # Allows: python src/app.py
    from data_analysis import analyze_csv
    from web_scraper import ScraperError, get_headings

LAB_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(LAB_ROOT / ".env")

app = Flask(__name__, template_folder=str(LAB_ROOT / "templates"))


def page_context(**updates: object) -> dict[str, object]:
    context: dict[str, object] = {
        "analysis": None,
        "headings": None,
        "error": None,
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY", "").strip()),
    }
    context.update(updates)
    return context


@app.get("/")
def index():
    return render_template("index.html", **page_context())


@app.post("/analyze")
def analyze():
    try:
        result = analyze_csv(
            LAB_ROOT / "data" / "sample_data.csv",
            "category",
            request.form.get("category", "A"),
            "price",
        )
        return render_template("index.html", **page_context(analysis=result))
    except (FileNotFoundError, ValueError) as exc:
        return render_template("index.html", **page_context(error=str(exc))), 400


@app.post("/scrape")
def scrape():
    url = request.form.get("url", "").strip()
    try:
        headings = get_headings(url)
        return render_template("index.html", **page_context(headings=headings))
    except (ValueError, ScraperError) as exc:
        return render_template("index.html", **page_context(error=str(exc))), 400


if __name__ == "__main__":
    app.run(debug=True)
