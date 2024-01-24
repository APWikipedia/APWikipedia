import os
import json
import re
from typing import List, Tuple, Dict, Set
from nltk.stem import SnowballStemmer
import string

class DataPreProcessor():
    def __init__(self) -> None:
        self.stopwords = set(open('ttds_2023_english_stop_words.txt', encoding='utf-8').read().splitlines())
        self.stemmer = self.stemmer = SnowballStemmer("english")
                
    def clean_text(self, text):
        """ 
        Clean text
        """
        # 去除换行符
        text = re.sub(r'\n+', ' ', text)
        # 去除LaTeX数学环境
        text = re.sub(r'\\begin\{.*?\}.*?\\end\{.*?\}', ' ', text, flags=re.DOTALL)
        # 去除独立的LaTeX命令
        text = re.sub(r'\\[a-zA-Z]+', ' ', text)
        # 去除未闭合的LaTeX公式部分
        text = re.sub(r'\$.+?\$', ' ', text)
        text = re.sub(r'\{.*?\}', ' ', text)
        
        # 去除特定的特殊符号（+ = } 等）
        text = re.sub(r'[+=^{}_()\[\]]', ' ', text)
        # 去除被空格包围的单个字符（字母、数字、符号）
        text = re.sub(r'\s[^\s]\s', ' ', text)
        # 进一步去除因去除公式后留下的多余空格
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def tokenize(self, text):
        text = ''.join(ch for ch in text if ch not in string.punctuation)
        text = text.split()
        filtered_text = [word for word in text if word not in self.stopwords]
        tokens = [self.stemmer.stem(word) for word in filtered_text]
        return tokens
        
    def process_file(self, file_path, output_dir, original_dir):
        """ 
        Process a single file and save as a JSON file with each sentence on a new line. 
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'content' in data:
                text = data['content']
                data['content'] = self.clean_text(text)
                data['token'] = self.tokenize(data['content'])

                rel_path = os.path.relpath(file_path, start=original_dir)
                json_path = os.path.splitext(rel_path)[0] + '.json'
                output_path = os.path.join(output_dir, json_path)

                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, 'w', encoding='utf-8') as output_file:
                    json.dump(data, output_file, ensure_ascii=False, indent=4)


    def process_all_files(self, original_dir, output_dir):
        """ 
        Process all files in the directory and its subdirectories. 
        """
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        for root, dirs, files in os.walk(original_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    self.process_file(file_path, output_dir, original_dir)

input_dir = '../spider/data/'
output_dir = 'data/'
dataPreProcessor = DataPreProcessor()
dataPreProcessor.process_all_files(input_dir, output_dir)


