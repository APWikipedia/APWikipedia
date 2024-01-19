import json
import os
from collections import defaultdict

DATA_ROOT = "data/"
CACHE_FILE = "articles_index.json"
CACHE_PATH = os.path.join(DATA_ROOT, CACHE_FILE)


def update_cache():
    # K:V -> category:(articles, revision_id)
    articles = defaultdict(set)
    for category in os.listdir(DATA_ROOT):
        category_path = os.path.join(DATA_ROOT, category)
        if os.path.isdir(category_path):
            for article_file in os.listdir(category_path):
                article_name = os.path.splitext(article_file)[
                    0
                ]  # Remove file extension

                revision_id = extract_revision_id(
                    os.path.join(category_path, article_file)
                )

                if revision_id and article_name:
                    articles[category].add((article_name, revision_id))

    # Convert sets to lists for JSON serialization
    articles_json_ready = {k: list(v) for k, v in articles.items()}

    # Write to cache file
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(articles_json_ready, f)


def cache_outdated(cached, new):
    if len(new.keys()) != len(cached.keys()):
        return True
    for category, article_set in new.items():
        if article_set != cached.get(category, set()):
            return True
    return False


def extract_revision_id(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            revision_id = file.readline().strip()
            return revision_id
    except Exception as e:
        print(f"Error extracting revision_id from {file_path}: {e}")
        return None


if __name__ == "__main__":
    update_cache()
