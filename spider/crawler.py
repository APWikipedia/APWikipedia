import json
import os
from collections import defaultdict

import wikipediaapi

from cache import CACHE_PATH, check_cache, update_cache

DATA_ROOT = "data/"
if not os.path.exists(DATA_ROOT):
    os.makedirs(DATA_ROOT)

wiki_wiki = wikipediaapi.Wikipedia(
    user_agent="Advanced personalized wikimedia (CW of UoE) (Yongtengrey@outlook.com)",
    language="en",
    extract_format=wikipediaapi.ExtractFormat.WIKI,
)

categories = set(
    ["Machine learning", "Deep learning", "Internet search engines", "Data science"]
)
# category:articles
articles = defaultdict(set)


def load_indexs_from_cache():
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            cache = json.load(f)
            return defaultdict(
                set, {category: set(articles) for category, articles in cache.items()}
            )
    except (FileNotFoundError, json.JSONDecodeError):
        # If cache file doesn't exist or is corrupted, update cache
        update_cache()
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            cache = json.load(f)
            return defaultdict(
                set, {category: set(articles) for category, articles in cache.items()}
            )


def write_article(category, title):
    page = wiki_wiki.page(title)
    if page.exists():
        dir = os.path.join(DATA_ROOT, category)
        if not os.path.exists(dir):
            os.makedirs(dir)

        name = page.title
        path = os.path.join(dir, name)
        with open(path, "w", encoding="utf-8") as file:
            file.write(page.text)


def get_related_categories(category, level=0, max_level=1):
    if category not in categories:
        print(f"New category: {category}")
        categories.add(category)

    cat = wiki_wiki.page("Category:" + category)
    if not cat.exists():
        return

    pages = cat.categorymembers
    for c in pages.values():
        if (
            c.ns == wikipediaapi.Namespace.CATEGORY
            and level < max_level
            and c.title not in categories
        ):
            new_category = c.title[9:] if c.title.startswith("Category:") else c.title
            get_related_categories(new_category, level=level + 1, max_level=max_level)


def get_category_articles(category):
    cat = wiki_wiki.page("Category:" + category)
    if not cat.exists():
        return

    pages = cat.categorymembers
    for c in pages.values():
        if (c.ns == wikipediaapi.Namespace.MAIN) and (
            c.title not in articles[category]
        ):
            try:
                articles[category].add(c.title)
                write_article(category, c.title)
                print(f"Added {category}:{c.title}")
            except Exception as e:
                print(f"Error processing article {category}:{c.title}: {e}")
        elif c.title in articles[category]:
            print(f"Escaped {category}:{c.title}")


if __name__ == "__main__":
    # Load indexes
    cached_articles = load_indexs_from_cache()
    articles = cached_articles.copy()

    # Automatically explore related categories
    for category in categories.copy():
        get_related_categories(category)

    print(f"{categories:}")

    # Collect articles from category
    for category in categories:
        get_category_articles(category)

    if check_cache(cached_articles, articles):
        update_cache()
        print("updated cache")
