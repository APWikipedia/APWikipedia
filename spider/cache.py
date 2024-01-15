import json
import os
from collections import defaultdict

DATA_ROOT = "../data/"
CACHE_FILE = "articles_index.json"
CACHE_PATH = os.path.join(DATA_ROOT, CACHE_FILE)


def update_cache():
    articles = defaultdict(set)
    for category in os.listdir(DATA_ROOT):
        category_path = os.path.join(DATA_ROOT, category)
        if os.path.isdir(category_path):
            for article_file in os.listdir(category_path):
                article_name = os.path.splitext(article_file)[
                    0
                ]  # Remove file extension
                articles[category].add(article_name)

    # Convert sets to lists for JSON serialization
    articles_json_ready = {k: list(v) for k, v in articles.items()}

    # Write to cache file
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(articles_json_ready, f)


def check_cache(cached, new):
    if new.keys() != cached.keys():
        return True
    for category, article_set in new.items():
        if article_set != cached.get(category, set()):
            return True
    return False


if __name__ == "__main__":
    update_cache()
