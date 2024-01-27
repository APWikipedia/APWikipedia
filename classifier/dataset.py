import json
import os

import pandas as pd

DATA_FOLDER = "data/"
CSV_PATH = "classifier/raw_data.csv"

if __name__ == "__main__":
    texts = []
    labels = []

    for category in os.listdir(DATA_FOLDER):
        category_folder = os.path.join(DATA_FOLDER, category)

        if os.path.isdir(category_folder):
            for file in os.listdir(category_folder):
                file_path = os.path.join(category_folder, file)

                if os.path.isfile(file_path):
                    try:
                        with open(file_path, "r", encoding="utf-8") as json_file:
                            data = json.load(json_file)

                            if "content" in data:
                                texts.append(data["content"])
                                labels.append(category)
                    except json.JSONDecodeError:
                        print(
                            f"cannot read {file_path}, file may be empty or wroing formatted"
                        )

    df = pd.DataFrame({"content": texts, "label": labels})

    # To csv
    df.to_csv(CSV_PATH, index=False)

    print(
        f"Dataset is stored at {CSV_PATH}\n \
          having {len(texts)} articles and {len(set(labels))} categories."
    )
