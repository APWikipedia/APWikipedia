import json
import os
import re
import string
from multiprocessing import Pool, cpu_count
from typing import Dict, List, Set, Tuple

from nltk.stem import SnowballStemmer

STOP_FILE_PATH = "./preprocess/ttds_2023_english_stop_words.txt"


class DataPreProcessor:
    def __init__(self) -> None:
        self.stopwords = set(open(STOP_FILE_PATH, encoding="utf-8").read().splitlines())
        self.stemmer = self.stemmer = SnowballStemmer("english")
        self.patterns = {
            "newlines": re.compile(r"\n+"),
            "latex_env": re.compile(r"\\begin\{.*?\}.*?\\end\{.*?\}", re.DOTALL),
            "latex_cmd": re.compile(r"\\[a-zA-Z]+"),
            "unbalanced_latex": re.compile(r"\$.+?\$"),
            "curly_braces": re.compile(r"\{.*?\}"),
            "special_chars": re.compile(r"[+=^{}_()\[\]]"),
            "single_char": re.compile(r"\s[^\s]\s"),
            "extra_spaces": re.compile(r"\s+")
        }

    def clean_text(self, text):
        # 使用预编译的正则表达式
        text = self.patterns["newlines"].sub(" ", text)
        text = self.patterns["latex_env"].sub(" ", text)
        text = self.patterns["latex_cmd"].sub(" ", text)
        text = self.patterns["unbalanced_latex"].sub(" ", text)
        text = self.patterns["curly_braces"].sub(" ", text)
        text = self.patterns["special_chars"].sub(" ", text)
        text = self.patterns["single_char"].sub(" ", text)
        text = self.patterns["extra_spaces"].sub(" ", text)
        return text.strip() 

    def tokenize(self, text):
        text = "".join(ch for ch in text if ch not in string.punctuation)
        text = text.split()
        filtered_text = [word for word in text if word not in self.stopwords]
        tokens = [self.stemmer.stem(word) for word in filtered_text]
        return tokens

    def process_file(self, file_path, output_dir):
        """
        Process a single merged JSON file.
        """
        with open(file_path, "r", encoding="utf-8") as input_file:
            data = json.load(input_file)
            for item in data:
                if "content" in item and "content" in item["content"]:
                    actual_content = item["content"]["content"]
                    cleaned_text = self.clean_text(actual_content)
                    tokens = self.tokenize(cleaned_text)
                    item["content"]["content"] = cleaned_text
                    item["content"]["token"] = tokens

        output_file_path = os.path.join(output_dir, os.path.basename(file_path))
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=4)


def process_file_wrapper(args):
    """
    Wrapper function for multiprocessing.
    """
    dataPreProcessor = DataPreProcessor()
    dataPreProcessor.process_file(*args)


def process_files_in_parallel(input_dir, output_dir):
    """
    Process all merged JSON files in the directory in parallel.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    files_to_process = [
        (os.path.join(input_dir, file), output_dir)
        for file in os.listdir(input_dir)
        if file.endswith(".json")
    ]

    pool = Pool(processes=cpu_count())
    pool.map(process_file_wrapper, files_to_process)
    pool.close()
    pool.join()


if __name__ == "__main__":
    input_dir = "merged_data/"
    output_dir = "processed_data/"
    process_files_in_parallel(input_dir, output_dir)
