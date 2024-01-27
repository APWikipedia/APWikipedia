import pandas as pd
from dataset import CSV_PATH

if __name__ == "__main__":
    loaded_df = pd.read_csv(CSV_PATH)
    print(
        f"Loaded dataset from {CSV_PATH} \n \
          having {len(loaded_df)} articles and {loaded_df['label'].nunique()} categories."
    )
    print(f"{loaded_df.head()}")
