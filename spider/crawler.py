import argparse
import json
import os
import sys
from collections import defaultdict
from pprint import pprint

import pywikibot
import wikipediaapi
from cache import CACHE_PATH, cache_outdated, update_cache
from parserx import setup_args
from pywikibot import Page

DATA_ROOT = "data/"
if not os.path.exists(DATA_ROOT):
    os.makedirs(DATA_ROOT)

wikibot = pywikibot.Site("en", "wikipedia")

wiki_wiki = wikipediaapi.Wikipedia(
    user_agent="Advanced personalized wikimedia (CW of UoE) (Yongtengrey@outlook.com)",
    language="en",
    extract_format=wikipediaapi.ExtractFormat.WIKI,
)

categories = set(
    # ["Machine learning", "Deep learning", "Internet search engines", "Data science"]
    ["Machine learning"]
)
# K:V -> category:(articles, revision_id)
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
    """
    Write article information:
        latest revision id
        URL
        External links (out->)
        Backlinks (in<-)
        content
    """
    page = wiki_wiki.page(title)
    if page.exists():
        dir = os.path.join(DATA_ROOT, category)
        if not os.path.exists(dir):
            os.makedirs(dir)

        lastest_revision_id = str(get_revision_id(title))
        # TODO: Delete
        if not lastest_revision_id:
            print(f"{title}: Revision id NOT FOUND")

        # URL: can be None, even page.exists() is pass
        url = page.fullurl if page.fullurl else ""
        # TODO: Delete
        if not url:
            print(f"{title}:Url NOT FOUND")

        # External links (out) PERF: Time consuming...
        external_links = format_external_links(page)

        # Back links (in) PERF: Time consuming...
        backlinks = format_backlinks(page)

        # Content
        name = page.title
        article_path = os.path.join(dir, f"{name}.txt")
        with open(article_path, "w", encoding="utf-8") as file:
            file.write(lastest_revision_id + "\n")
            file.write(url + "\n")
            file.write(external_links + "\n")
            file.write(backlinks + "\n")
            file.write(page.text)
        return lastest_revision_id
    return -1


def format_external_links(page):
    return "|".join(
        link_page.fullurl if link_page.fullurl else ""
        for link_page in page.links.values()
        if link_page.exists()
    )


def format_backlinks(page):
    return "|".join(
        link_page.fullurl if link_page.fullurl else ""
        for link_page in page.backlinks.values()
        if link_page.exists()
    )


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

    cached_articles = [article for article, _ in articles.get(category, set())]

    pages = cat.categorymembers
    for c in pages.values():
        if (c.ns == wikipediaapi.Namespace.MAIN) and (c.title not in cached_articles):
            try:
                last_revision_id = write_article(category, c.title)
                articles[category].add((c.title, last_revision_id))
                print(f"Added {category}:{c.title}")
            except Exception as e:
                print(f"Error processing article {category}:{c.title}: {e}")
        elif c.title in articles[category]:
            print(f"Escaped {category}:{c.title}")


# PERF: Cost lot of time to check...
def get_revision_id(title):
    """
    Get the latest_revision_id
    """
    page = Page(wikibot, title)
    return page.latest_revision_id


if __name__ == "__main__":
    """Example usage:
    python crawler.py \
        --debug True \
    """
    parser = argparse.ArgumentParser()
    setup_args(parser)
    args = parser.parse_args(sys.argv[1:])

    pprint(f"Parsed Arguments: {vars(args)}")

    # Load indexes
    cached_articles = load_indexs_from_cache()
    articles = cached_articles.copy()

    # Automatically explore related categories
    if not args.debug:
        for category in categories.copy():
            get_related_categories(category)

        print(f"{categories:}")

    # Collect articles from category
    for category in categories:
        get_category_articles(category)

    if cache_outdated(cached_articles, articles):
        update_cache()
        print("updated cache")
