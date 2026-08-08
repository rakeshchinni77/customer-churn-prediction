"""
Script to load and inspect the Telco Customer Churn dataset.
"""

import sys
from pathlib import Path

# Ensure root directory is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.model import (
    load_data,
    get_dataset_shape,
    get_column_names,
    get_missing_summary,
    get_target_distribution,
    get_feature_lists,
)
from app.logger import logger


def main():
    logger.info("Running dataset loading script...")
    df = load_data()

    print("\n==========================================")
    print("Dataset loaded successfully")
    print("==========================================")

    shape = get_dataset_shape(df)
    print(f"\nShape: {shape[0]} rows, {shape[1]} columns")

    columns = get_column_names(df)
    print(f"\nColumns ({len(columns)}):")
    print(columns)

    missing = get_missing_summary(df)
    print("\nMissing values:")
    if missing.empty:
        print("No missing values found.")
    else:
        print(missing.to_string())

    target_dist = get_target_distribution(df, target_col="Churn")
    print("\nTarget distribution (Churn):")
    for class_label, stats in target_dist.items():
        print(f"  {class_label}: {stats['count']} ({stats['percentage']}%)")

    cat_cols, num_cols = get_feature_lists(df)
    print(f"\nCategorical features ({len(cat_cols)}): {cat_cols}")
    print(f"Numerical features ({len(num_cols)}): {num_cols}")
    print("==========================================\n")


if __name__ == "__main__":
    main()
