import json
import os
import re
import string
from typing import Dict, List, Set, Tuple

from nltk.stem import SnowballStemmer


class DataPreProcessor:
    def __init__(self) -> None:
        self.stopwords = set(
            open("ttds_2023_english_stop_words.txt", encoding="utf-8")
            .read()
            .splitlines()
        )
        self.stemmer = self.stemmer = SnowballStemmer("english")

    def clean_text(self, text):
        """
        Clean text
        """
        # 去除换行符
        text = re.sub(r"\n+", " ", text)
        # 去除LaTeX数学环境
        text = re.sub(r"\\begin\{.*?\}.*?\\end\{.*?\}", " ", text, flags=re.DOTALL)
        # 去除独立的LaTeX命令
        text = re.sub(r"\\[a-zA-Z]+", " ", text)
        # 去除未闭合的LaTeX公式部分
        text = re.sub(r"\$.+?\$", " ", text)
        text = re.sub(r"\{.*?\}", " ", text)

        # 去除特定的特殊符号（+ = } 等）
        text = re.sub(r"[+=^{}_()\[\]]", " ", text)
        # 去除被空格包围的单个字符（字母、数字、符号）
        text = re.sub(r"\s[^\s]\s", " ", text)
        # 进一步去除因去除公式后留下的多余空格
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def tokenize(self, text):
        text = "".join(ch for ch in text if ch not in string.punctuation)
        text = text.split()
        filtered_text = [word for word in text if word not in self.stopwords]
        tokens = [self.stemmer.stem(word) for word in filtered_text]
        return tokens

    def process_files(self, input_dir, output_dir):
        """
        Process all merged JSON files in the directory.
        """
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        for file in os.listdir(input_dir):
            if file.endswith(".json"):
                file_path = os.path.join(input_dir, file)
                with open(file_path, "r", encoding="utf-8") as input_file:
                    data = json.load(input_file)
                    for item in data:
                        if "content" in item and "content" in item["content"]:
                            actual_content = item["content"]["content"]
                            cleaned_text = self.clean_text(actual_content)
                            tokens = self.tokenize(cleaned_text)
                            item["content"]["content"] = cleaned_text
                            item["content"]["token"] = tokens

                output_path = os.path.join(output_dir, file)
                with open(output_path, "w", encoding="utf-8") as output_file:
                    json.dump(data, output_file, ensure_ascii=False, indent=4)


input_dir = "../spider/merged_data/"
output_dir = "./data/"
dataPreProcessor = DataPreProcessor()
dataPreProcessor.process_files(input_dir, output_dir)
