import argparse
import json
import os
import sys
from collections import defaultdict
from pprint import pprint
import logging

import pywikibot
import wikipediaapi
from cache import CACHE_PATH, cache_outdated, update_cache
from parserx import setup_args
from pywikibot import Page

from logging.config import fileConfig

fileConfig('../logging_config.ini')
logger = logging.getLogger()
logger.debug('All pass, all distinction, all 100')

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
    ["Machine learning", "Deep learning", "Internet search engines", "Data science",
    "Computer Vision","Natural Language Processing","Big Data","Cloud Computing",
    "Internet of Things","Software Engineering","Computer Networks","Cybersecurity",
    "Mobile App Development","Operating Systems","Programming Languages", 
    "Algorithms","Database Technologies","Distributed Systems",
    # 以上词条能爬取4922篇，耗时一小时
    # 新增类别，谁来爬一下，挂几小时机

     # 每人18行先 雷
    "Artificial Intelligence", "Human-Computer Interaction", "Quantum Computing",
    "Virtual Reality", "Augmented Reality", "Blockchain", "Cryptocurrency",
    "Digital Signal Processing", "Game Development", "Web Development",
    "Computer Graphics", "User Experience Design", "Network Security",
    "Parallel Computing", "Embedded Systems", "Computer Architecture",
    "Information Retrieval", "E-Commerce Technology", "Computational Biology",
    "Computational Physics", "Mathematical Software", "Ethical Hacking",
    "Robotics", "Automation", "Digital Marketing", "Social Media Technology",
    "Cloud Security", "Data Mining", "Machine Ethics", "Bioinformatics",
    "Computer-Aided Design", "Computer Animation", "Wireless Networks",
    "Wearable Technology", "5G Technology", "Edge Computing", "Fintech",
    "Smart Cities", "Digital Art", "Information Theory", "Acoustic Engineering",
    "Software Testing", "DevOps", "Agile Software Development", "System Administration",
    "Data Visualization", "Graph Theory", "Information Systems", "IT Management",
    "Quantum Information Science", "Computational Chemistry", "Digital Humanities",
    "Technology Ethics", "Digital Privacy", "Cyber Physical Systems", "Information Economics",
    "Ubiquitous Computing", "Human-Robot Interaction", "Computational Finance",
    "Digital Forensics", "Autonomous Vehicles", "Cognitive Computing", "Applied Mathematics",
    # 沈
    "Data Ethics", "Sustainable Computing", "Green IT", "Computational Sociology",
    "Technology Management", "Educational Technology", "Health Informatics",
    "Neural Networks", "Evolutionary Computation", "High Performance Computing",
    "Open Source Software", "Software Metrics", "Network Management",
    "Digital Libraries", "Technology Policy", "Digital Accessibility",
    "Computational Geometry", "Pattern Recognition", "Computer Music",
    "Multimedia Systems", "Speech Processing", "Sensor Networks", "Haptic Technology",
    "Real-Time Systems", "Computer Forensics", "IT Legislation", "IT Project Management",
    "Computational Astrophysics", "Cyber Warfare", "Human-Centered Computing",
    "Cryptography", "Data Storage Systems", "Computer Ethics", "Cloud Storage",
    "Enterprise Software", "Graphical User Interfaces", "Digital Signal Processors",
    "Mobile Networking", "Ad Hoc Networks", "Microprocessor Design", "VLSI Design",
    "Wearable Computing", "Computer Simulation", "Digital Signal Controllers",
    "Microcontrollers", "Optical Computing", "Quantum Cryptography",
    "Computer-Aided Engineering", "Computer-Aided Manufacturing", "Virtual Machines",
    "Computer Performance", "Distributed Database", "IT Service Management",
    "Multimedia Networking", "Network Security Algorithms", "Parallel Programming",
    "Programmable Logic", "Reconfigurable Computing", "RFID Technology",
    # 姜
    "Software Quality Assurance", "Speech Recognition Technology", "System On Chip",
    "Virtual Reality Gaming", "Web Engineering", "Wireless Sensor Networks",
    "Computer Security Incident Management", "Data Privacy Laws", "Edge Computing Architectures",
    "Fuzzy Logic Systems", "Genetic Algorithms", "Hardware Security Modules",
    "Information Theory in Cryptography", "IoT Security Protocols", "Machine Learning in Bioinformatics",
    "Neural Network Optimization", "Quantum Machine Learning", "Reinforcement Learning Applications",
    "Social Network Analysis Algorithms", "Software Defined Networking", "Virtualization Security",
    "Web Scraping Techniques", "3D Computer Graphics", "Advanced Database Systems",
    "Augmented Reality Development", "Biometric Authentication Technologies",
    "Cloud Computing Security", "Computer Animation Techniques", "Data Compression Algorithms",
    "Digital Currency Technologies", "Electronic Voting Systems", "Forensic Data Analysis",
    "GPU Programming", "High-Throughput Computing", "IT Compliance and Ethics",
    "Knowledge Representation and Reasoning", "Low-Power Computing", "Mobile Payment Systems",
    "Network Function Virtualization", "Open Source Intelligence Techniques", "Predictive Analytics Models",
    "Quantum Communication Networks", "Remote Sensing Technology", "Smart Grid Cybersecurity",
    "Text Mining Algorithms", "Ubiquitous Networking", "Virtual Private Networks",
    "Web Accessibility Standards", "Zigbee Communication Protocols", "Adaptive Learning Systems",
    "Biologically Inspired Computing", "Computational Aerodynamics", "Data Fusion Techniques",
    # 唐
    "Embedded Software Development", "Gesture Recognition Systems", "Homomorphic Encryption Methods",
    "Indoor Positioning Systems", "Location-Based Services", "Mobile Device Forensics",
    "Neuromorphic Computing", "Optical Character Recognition", "Program Synthesis",
    "Quantum Information Processing", "Robotics Control Systems", "Space Computing Technology",
    "Threat Intelligence Platforms", "User Interface Design Principles", "Voice Recognition Technologies",
    "Wearable Device Technologies", "3D Printing Technologies", "Automated Reasoning Systems",
    "Blockchain in Healthcare", "Computational Fluid Dynamics", "Data Warehousing Solutions",
    "Enterprise Resource Planning", "Game Theory in Computer Science", "Hybrid Cloud Solutions",
    "Integrated Development Environments", "Log File Analysis Techniques", "Multimedia Learning Systems",
    "Non-Fungible Token Technologies", "Operating System Development", "Privacy Enhancing Technologies",
    "Radio Frequency Identification", "Semantic Web Technologies", "Supply Chain Management Software",
    "Time Series Analysis in Finance", "User Generated Content Moderation", "Virtual Reality in Medicine",
    "Wireless Communication Standards", "Zero Trust Network Architectures"]
    # ["Machine learning"]
)
# K:V -> category:(articles, revision_id)
articles = defaultdict(set)


def load_indexs_from_cache():
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            cache = json.load(f)
            return defaultdict(
                set, {category: {tuple(article) for article in articles} for category, articles in cache.items()}
            )
    except (FileNotFoundError, json.JSONDecodeError):
        # If cache file doesn't exist or is corrupted, update cache
        update_cache()
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            cache = json.load(f)
            return defaultdict(
                set, {category: {tuple(article) for article in articles} for category, articles in cache.items()}
            )


def write_article(category, title, fetch_links):
    """
    Write article information in JSON format:
        - latest revision id
        - URL
        - External links
        - Backlinks
        - content
    """
    page = wiki_wiki.page(title)
    if page.exists():
        dir = os.path.join(DATA_ROOT, category)
        if not os.path.exists(dir):
            os.makedirs(dir)

        article_data = {
            "lastest_revision_id": str(get_revision_id(title)),
            "url": page.fullurl if page.fullurl else "",
            "external_links": format_external_links(page) if fetch_links else [],
            "backlinks": format_backlinks(page) if fetch_links else [],
            "content": page.text
        }

        name = page.title
        file_extension = "json"
        article_path = os.path.join(dir, f"{name}.{file_extension}")
        with open(article_path, "w", encoding="utf-8") as file:
            json.dump(article_data, file, ensure_ascii=False, indent=4)
        return article_data["lastest_revision_id"]
    return -1


def format_external_links(page):
    return [
        link_page.fullurl
        for link_page in page.links.values()
        if link_page.exists() and link_page.fullurl
    ]

def format_backlinks(page):
    return [
        link_page.fullurl
        for link_page in page.backlinks.values()
        if link_page.exists() and link_page.fullurl
    ]


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


def get_category_articles(category, fetch_links=False):
    cat = wiki_wiki.page("Category:" + category)
    if not cat.exists():
        return

    cached_articles = [article for article, _ in articles.get(category, set())]

    pages = cat.categorymembers
    for c in pages.values():
        if (c.ns == wikipediaapi.Namespace.MAIN) and (c.title not in cached_articles):
            try:
                last_revision_id = write_article(category, c.title, fetch_links=fetch_links)
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

def count_files_in_directory(directory):
    total_files = 0
    for root, dirs, files in os.walk(directory):
        total_files += len(files)
    return total_files

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
        get_category_articles(category, fetch_links=args.fetch_links)

    if cache_outdated(cached_articles, articles):
        update_cache()
        print("updated cache")

    file_count = count_files_in_directory(DATA_ROOT)
    print(f"Totally {file_count} files have been stored.")
