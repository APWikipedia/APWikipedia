import argparse
import json
import logging
import os
import sys
from collections import defaultdict
from logging.config import fileConfig
from pprint import pprint

import pywikibot
import wikipediaapi
from cache import CACHE_PATH, cache_outdated, update_cache
from parserx import setup_args
from pywikibot import Page

fileConfig("logging_config.ini")
logger = logging.getLogger()
logger.debug("All pass, all distinction, all 100")

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
    [
        "3D Computer Graphics",
        "3D Printing",
        "3D Printing Technologies",
        "5G Technology",
        "Acoustic Engineering",
        "Ad Hoc Networks",
        "Adaptive Learning Systems",
        "Advanced Database Systems",
        "Agile Software Development",
        "Algorithms",
        "Applied Mathematics",
        "Apps",
        "Artificial Intelligence",
        "Artificial intelligence",
        "Audio Engineering",
        "Augmented Reality",
        "Augmented Reality Development",
        "Automated Reasoning Systems",
        "Automation",
        "Autonomous Vehicles",
        "Avionics",
        "Big Data",
        "Bioinformatics",
        "Biologically Inspired Computing",
        "Biometric Authentication Technologies",
        "Biotechnology",
        "Blockchain",
        "Blockchain in Healthcare",
        "Business Continuity Planning",
        "Business Intelligence",
        "Cartography",
        "Change Management",
        "Chemical engineering",
        "Circuits",
        "Classes of computers",
        "Cloud Analytics",
        "Cloud Computing",
        "Cloud Computing Security",
        "Cloud Security",
        "Cloud Storage",
        "Cognitive Computing",
        "Cognitive Science",
        "Communication ",
        "Companies",
        "Computational Aerodynamics",
        "Computational Astrophysics",
        "Computational Biology",
        "Computational Chemistry",
        "Computational Finance",
        "Computational Fluid Dynamics",
        "Computational Geometry",
        "Computational Linguistics",
        "Computational Neuroscience",
        "Computational Physics",
        "Computational Social Science",
        "Computational Sociology",
        "Computer Aided Design",
        "Computer Animation",
        "Computer Animation Techniques",
        "Computer Architecture",
        "Computer Ethics",
        "Computer Forensics",
        "Computer Graphics",
        "Computer Hardware",
        "Computer Music",
        "Computer Networks",
        "Computer Performance",
        "Computer Security Incident Management",
        "Computer Simulation",
        "Computer Viruses",
        "Computer Vision",
        "Computer architecture",
        "Computer engineering",
        "Computer model",
        "Computer science",
        "Computer security",
        "Computer-Aided Design",
        "Computer-Aided Engineering",
        "Computer-Aided Manufacturing",
        "Computing",
        "Computing and society",
        "Concurrent Programming",
        "Connectors",
        "Construction",
        "Consumer electronics",
        "Control theory",
        "Cryptocurrency",
        "Cryptography",
        "Customer Relationship Management",
        "Cyber Physical Systems",
        "Cyber Risk Management",
        "Cyber Warfare",
        "Cybersecurity",
        "Data",
        "Data Center Management",
        "Data Compression Algorithms",
        "Data Ethics",
        "Data Fusion Techniques",
        "Data Mining",
        "Data Privacy Laws",
        "Data Quality",
        "Data Recovery",
        "Data Storage Systems",
        "Data Structures",
        "Data Visualization",
        "Data Warehousing Solutions",
        "Data science",
        "Database Technologies",
        "Decision Support Systems",
        "Deep learning",
        "Design",
        "DevOps",
        "Digital Accessibility",
        "Digital Art",
        "Digital Currency",
        "Digital Currency Technologies",
        "Digital Forensics",
        "Digital Humanities",
        "Digital Libraries",
        "Digital Marketing",
        "Digital Policy",
        "Digital Privacy",
        "Digital Rights Management",
        "Digital Signal Controllers",
        "Digital Signal Processing",
        "Digital Signal Processors",
        "Digital Transformation",
        "Digital divide",
        "Digital electronics",
        "Digital media",
        "Disaster Recovery",
        "Distributed Database",
        "Distributed Systems",
        "E-Commerce",
        "E-Commerce Technology",
        "E-Government",
        "ERP Systems",
        "Earthquake engineering",
        "Edge Computing",
        "Edge Computing Architectures",
        "Educational Technology",
        "Electrical components",
        "Electrical engineering",
        "Electronic Voting Systems",
        "Electronic design",
        "Electronics",
        "Electronics manufacturing",
        "Embedded Software Development",
        "Embedded Systems",
        "Embedded systems",
        "Energy",
        "Enterprise Architecture",
        "Enterprise Resource Planning",
        "Enterprise Software",
        "Environmental engineering",
        "Ergonomics",
        "Esports",
        "Ethical Hacking",
        "Evolutionary Computation",
        "FinTech",
        "Fintech",
        "Fire prevention",
        "Firefighting",
        "Forensic Data Analysis",
        "Forensic science",
        "Forestry",
        "Formal Methods",
        "Free software",
        "Functional Programming",
        "Fuzzy Logic Systems",
        "GPU Programming",
        "Game Development",
        "Game Theory in Computer Science",
        "Genetic Algorithms",
        "Geographic Information Systems",
        "Gesture Recognition Systems",
        "Graph Theory",
        "Graphical User Interfaces",
        "Green IT",
        "Hacking",
        "Haptic Technology",
        "Hardware Security Modules",
        "Health Informatics",
        "High Performance Computing",
        "High-Throughput Computing",
        "Homomorphic Encryption Methods",
        "Human Factors Engineering",
        "Human-Centered Computing",
        "Human-Computer Interaction",
        "Human-Robot Interaction",
        "Human-computer interaction",
        "Hybrid Cloud Solutions",
        "IT Auditing",
        "IT Compliance",
        "IT Compliance and Ethics",
        "IT Governance",
        "IT Legislation",
        "IT Management",
        "IT Outsourcing",
        "IT Project Management",
        "IT Service Management",
        "Indoor Positioning Systems",
        "Industry",
        "Information Assurance",
        "Information Economics",
        "Information Ethics",
        "Information Retrieval",
        "Information Security Management",
        "Information Systems",
        "Information Theory",
        "Information Theory in Cryptography",
        "Information science",
        "Information systems",
        "Information technology",
        "Innovation Management",
        "Integrated Development Environments",
        "Integrated circuits",
        "Internet",
        "Internet Governance",
        "Internet Law",
        "Internet Protocol",
        "Internet Safety",
        "Internet of Things",
        "Internet search engines",
        "IoT Security Protocols",
        "Knowledge Management",
        "Knowledge Representation and Reasoning",
        "Languages",
        "Location-Based Services",
        "Log File Analysis Techniques",
        "Logic Programming",
        "Low-Power Computing",
        "Machine Ethics",
        "Machine Learning in Bioinformatics",
        "Machine learning",
        "Malware Analysis",
        "Management",
        "Manufacturing",
        "Marketing",
        "Materials science",
        "Mathematical Software",
        "Mechanical engineering",
        "Media Technology",
        "Media studies",
        "Medicine",
        "Metalworking",
        "Microcontrollers",
        "Microprocessor Design",
        "Microprocessors",
        "Microtechnology",
        "Microwave technology",
        "Military science",
        "Mining",
        "Mobile App Development",
        "Mobile Computing",
        "Mobile Device Forensics",
        "Mobile Networking",
        "Mobile Payment Systems",
        "Mobile web",
        "Molecular electronics",
        "Multimedia",
        "Multimedia Learning Systems",
        "Multimedia Networking",
        "Multimedia Systems",
        "Nanotechnology",
        "Natural Language Processing",
        "Network Architecture",
        "Network Function Virtualization",
        "Network Management",
        "Network Protocols",
        "Network Security",
        "Network Security Algorithms",
        "Networks (Industrial)",
        "Neural Network Optimization",
        "Neural Networks",
        "Neuromorphic Computing",
        "Non-Fungible Token Technologies",
        "Nuclear technology",
        "Object-Oriented Programming",
        "Open Source Intelligence Techniques",
        "Open Source Software",
        "Operating System Development",
        "Operating Systems",
        "Operating systems",
        "Optical Character Recognition",
        "Optical Computing",
        "Optics",
        "Optoelectronics",
        "Parallel Computing",
        "Parallel Programming",
        "Pattern Recognition",
        "Penetration Testing",
        "Platforms",
        "Plumbing",
        "Predictive Analytics Models",
        "Privacy Enhancing Technologies",
        "Product lifecycle management",
        "Program Synthesis",
        "Programmable Logic",
        "Programming",
        "Programming Languages",
        "Quality Assurance",
        "Quantum Communication Networks",
        "Quantum Computing",
        "Quantum Cryptography",
        "Quantum Information Processing",
        "Quantum Information Science",
        "Quantum Machine Learning",
        "Quantum electronics",
        "RFID Technology",
        "Radio Frequency Identification",
        "Radio electronics",
        "Radio-frequency identification RFID",
        "Real-Time Computing",
        "Real-Time Systems",
        "Real-time computing",
        "Reconfigurable Computing",
        "Reinforcement Learning Applications",
        "Remote Sensing Technology",
        "Renewable Energy Technology",
        "Risk Management",
        "Robotics",
        "Robotics Control Systems",
        "Semantic Web",
        "Semantic Web Technologies",
        "Semiconductors",
        "Sensor Networks",
        "Signal cables",
        "Smart Cities",
        "Smart Grid Cybersecurity",
        "Social Media Technology",
        "Social Network Analysis",
        "Social Network Analysis Algorithms",
        "Software",
        "Software Architecture",
        "Software Defined Networking",
        "Software Engineering",
        "Software Licensing",
        "Software Metrics",
        "Software Modeling",
        "Software Quality Assurance",
        "Software Testing",
        "Software engineering",
        "Sound technology",
        "Space Computing Technology",
        "Speech Processing",
        "Speech Recognition Technology",
        "Storage Area Networks",
        "Structural engineering",
        "Supply Chain Management",
        "Supply Chain Management Software",
        "Surveillance",
        "Sustainable Computing",
        "System Administration",
        "System On Chip",
        "Systems Analysis",
        "Systems Engineering",
        "Systems Integration",
        "Systems engineering",
        "Technical Support",
        "Technology Adoption",
        "Technology Education",
        "Technology Ethics",
        "Technology Forecasting",
        "Technology Management",
        "Technology Policy",
        "Technology forecasting",
        "Telecommunications",
        "Telecommunications Law",
        "Text Mining Algorithms",
        "Threat Intelligence Platforms",
        "Time Series Analysis in Finance",
        "Tools",
        "Ubiquitous Computing",
        "Ubiquitous Networking",
        "Unsolved problems in computer science",
        "Unsolved problems in neuroscience",
        "Urban Informatics",
        "User Experience Design",
        "User Generated Content Moderation",
        "User Interface Design",
        "User Interface Design Principles",
        "VLSI Design",
        "Video Game Design",
        "Virtual Machines",
        "Virtual Private Networks",
        "Virtual Reality",
        "Virtual Reality Gaming",
        "Virtual Reality in Medicine",
        "Virtualization Security",
        "Virtualization Technology",
        "Voice Recognition Technologies",
        "Water technology",
        "Wearable Computing",
        "Wearable Device Technologies",
        "Wearable Technology",
        "Web Accessibility Standards",
        "Web Development",
        "Web Engineering",
        "Web Scraping Techniques",
        "Web Services",
        "Wireless Communication Standards",
        "Wireless Networks",
        "Wireless Security",
        "Wireless Sensor Networks",
        "Zero Trust Network Architectures",
        "Zigbee Communication Protocols",
    ]
)
# K:V -> category:(articles, revision_id)
articles = defaultdict(set)


def load_indexs_from_cache():
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            cache = json.load(f)
            return defaultdict(
                set,
                {
                    category: {tuple(article) for article in articles}
                    for category, articles in cache.items()
                },
            )
    except (FileNotFoundError, json.JSONDecodeError):
        # If cache file doesn't exist or is corrupted, update cache
        update_cache()
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            cache = json.load(f)
            return defaultdict(
                set,
                {
                    category: {tuple(article) for article in articles}
                    for category, articles in cache.items()
                },
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
            "content": page.text,
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
                last_revision_id = write_article(
                    category, c.title, fetch_links=fetch_links
                )
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
