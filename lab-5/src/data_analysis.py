"""Small reusable pandas CSV analysis for laboratory work №5."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import TypedDict

import pandas as pd
from pandas.api.types import is_numeric_dtype


class AnalysisResult(TypedDict):
    selected_rows: int
    mean: float


def analyze_csv(
    file_path: str | Path,
    filter_column: str,
    filter_value: str,
    mean_column: str,
) -> AnalysisResult:
    """Filter CSV rows and calculate a numeric column's arithmetic mean."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"CSV file does not exist: {path}")

    frame = pd.read_csv(path)
    missing = [name for name in (filter_column, mean_column) if name not in frame]
    if missing:
        raise ValueError(f"CSV column does not exist: {', '.join(missing)}")
    if not is_numeric_dtype(frame[mean_column]):
        raise ValueError(f"Mean column must be numeric: {mean_column}")

    # Compare as strings so command-line values work for text and simple numbers.
    selected = frame[frame[filter_column].astype(str) == str(filter_value)]
    if selected.empty:
        raise ValueError(
            f"No rows where {filter_column} equals {filter_value!r}."
        )

    return {
        "selected_rows": int(len(selected)),
        "mean": float(selected[mean_column].mean()),
    }


def main() -> int:
    default_csv = Path(__file__).resolve().parents[1] / "data" / "sample_data.csv"
    parser = argparse.ArgumentParser(description="Filter a CSV and calculate mean.")
    parser.add_argument("file", nargs="?", default=str(default_csv))
    parser.add_argument("--filter-column", default="category")
    parser.add_argument("--filter-value", default="A")
    parser.add_argument("--mean-column", default="price")
    args = parser.parse_args()
    try:
        result = analyze_csv(
            args.file, args.filter_column, args.filter_value, args.mean_column
        )
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as exc:
        print(f"Error: {exc}")
        return 1

    print(f"Filter: {args.filter_column} == {args.filter_value!r}")
    print(f"Selected rows: {result['selected_rows']}")
    print(f"Mean {args.mean_column}: {result['mean']:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
