import gzip
import os
import json
from collections import defaultdict
import gzip

def load_data(input_dir):
    data = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(input_dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                data.extend(json.load(file))
    return data

def create_inverted_index(data):
    """
    Create an zipped inverted index from the input data to save storage
    """
    inverted_index = defaultdict(lambda: defaultdict(list))
    for document in data:
        file_name = document.get("file_name", "")
        content = document.get("content", {})
        tokens = content.get("token", [])
        for position, token in enumerate(tokens):
            if file_name not in inverted_index[token]:
                inverted_index[token][file_name] = [position]
            else:
                # 存储与前一位置的差值
                inverted_index[token][file_name].append(position - inverted_index[token][file_name][-1])
    return inverted_index


# def save_inverted_index(inverted_index, output_file):
#     # 转换数据结构为可序列化的格式
#     serializable_index = {word: {doc: positions for doc, positions in docs.items()} 
#                           for word, docs in inverted_index.items()}
#     with open(output_file, 'w', encoding='utf-8') as file:
#         json.dump(serializable_index, file, ensure_ascii=False, indent=4)
def save_inverted_index(inverted_index, output_file):
    """
    Use gzip to save storage
    """
    serializable_index = {word: {doc: positions for doc, positions in docs.items()}
                          for word, docs in inverted_index.items()}
    with gzip.open(output_file, 'wt', encoding='utf-8') as file:
        json.dump(serializable_index, file, ensure_ascii=False)

if __name__ == "__main__":        
    input_dir = 'processed_data/'         
    output_file = 'engine/inverted_index.json'   
    data = load_data(input_dir)
    inverted_index = create_inverted_index(data)
    save_inverted_index(inverted_index, output_file)