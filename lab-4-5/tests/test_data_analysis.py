from pathlib import Path

import pandas as pd
import pytest

from src.data_analysis import analyze_csv


@pytest.fixture
def csv_file(tmp_path: Path) -> Path:
    path = tmp_path / "products.csv"
    pd.DataFrame(
        {"category": ["A", "B", "A"], "price": [10, 99, 30], "name": ["x", "y", "z"]}
    ).to_csv(path, index=False)
    return path


def test_category_filtering_and_mean(csv_file: Path) -> None:
    assert analyze_csv(csv_file, "category", "A", "price") == {
        "selected_rows": 2,
        "mean": 20.0,
    }


def test_nonexistent_column_is_controlled_error(csv_file: Path) -> None:
    with pytest.raises(ValueError, match="column does not exist"):
        analyze_csv(csv_file, "missing", "A", "price")


def test_empty_filtered_result_is_controlled_error(csv_file: Path) -> None:
    with pytest.raises(ValueError, match="No rows"):
        analyze_csv(csv_file, "category", "C", "price")


def test_mean_column_must_be_numeric(csv_file: Path) -> None:
    with pytest.raises(ValueError, match="must be numeric"):
        analyze_csv(csv_file, "category", "A", "name")
