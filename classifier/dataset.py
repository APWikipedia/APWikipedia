import json
import os

import pandas as pd

PROCESSED_DATA_PATH = "processed_data/"
DATA_CSV_PATH = "classifier/processed_data.csv"


def prepare_dataset(data_path):
    data = []
    for filename in os.listdir(data_path):
        if filename.endswith(".json"):
            category = os.path.splitext(filename)[0]
            file_path = os.path.join(data_path, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                articles = json.load(file)
                for article in articles:
                    article_data = {
                        "name": article["file_name"],
                        "token": article["content"]["token"],
                        "category": category,
                    }
                    data.append(article_data)
    return pd.DataFrame(data)


if __name__ == "__main__":
    df = prepare_dataset(PROCESSED_DATA_PATH)
    df = df[df["token"].notna() & df["token"].map(bool)].reset_index(drop=True)
    assert all(
        isinstance(row, list) for row in df["token"]
    ), "Not all rows in 'token' are lists."

    df.to_csv(DATA_CSV_PATH, index=False)

    print(
        f"Dataset is stored at {DATA_CSV_PATH}\n \
        having {len(df)} articles and {len(df['category'].unique())} categories."
    )
