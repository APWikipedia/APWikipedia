import os
import json
import re

def clean_text(text):
    """ 
    Clean text by removing special characters (except sentence enders) and extra whitespace. 
    """
    text = re.sub(r'[^\w\s.!?]', '', text)  # Remove non-word characters except for .!?
    text = re.sub(r'\s+', ' ', text)  # Replace all whitespace with a single space
    return text.strip()

def split_into_sentences(text):
    """ 
    Split text into individual sentences. 
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [sentence.strip() for sentence in sentences if sentence]

def process_file(file_path, output_dir, original_dir):
    """ 
    Process a single file and save as a JSON file with each sentence on a new line. 
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if 'content' in data:
            text = data['content']

            cleaned_text = clean_text(text)
            sentences = split_into_sentences(cleaned_text)

            # We can change it into Array whether necessary
            data['content'] = ' '.join(sentences)

            rel_path = os.path.relpath(file_path, start=original_dir)
            json_path = os.path.splitext(rel_path)[0] + '.json'
            output_path = os.path.join(output_dir, json_path)

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as output_file:
                json.dump(data, output_file, ensure_ascii=False, indent=4)


def process_all_files(original_dir, output_dir):
    """ 
    Process all files in the directory and its subdirectories. 
    """
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for root, dirs, files in os.walk(original_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                process_file(file_path, output_dir, original_dir)

input_dir = '../spider/data/'
output_dir = 'data/'

process_all_files(input_dir, output_dir)


