import gzip
import os
import json
import math
from collections import defaultdict
import gzip
import pickle

def load_data(input_dir):
    data = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(input_dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                data.extend(json.load(file))
    return data

def default_dict_list():
    return defaultdict(list)

def create_inverted_index(data):
    """
    Create both lightweight and heavyweight inverted indexes from the input data.
    The lightweight index will not include position data and will store precomputed TF-IDF values.
    The heavyweight index will include position data for proximity queries.
    """
    lightweight_index = defaultdict(dict)  # 不包含位置信息，将存储TF-IDF值
    heavyweight_index = {}  # 包含位置信息，手动管理
    doc_frequency = defaultdict(int)  # 用于计算DF
    doc_lengths = defaultdict(int)  # 存储每个文档的长度

    # First pass: Build both indexes and compute document frequencies
    for document in data:
        file_name = document.get("file_name", "")
        content = document.get("content", {})
        tokens = content.get("token", [])
        seen_tokens = set()  # Track tokens seen in this document to correctly compute DF
        for position, token in enumerate(tokens):
            # Update heavyweight index
            if token not in heavyweight_index:
                heavyweight_index[token] = {file_name: [position]}
            else:
                if file_name not in heavyweight_index[token]:
                    heavyweight_index[token][file_name] = [position]
                else:
                    # Subtract the last position to store the gap, not the absolute position
                    heavyweight_index[token][file_name].append(position - heavyweight_index[token][file_name][-1])

            # Ensure each token is only counted once for DF per document
            if token not in seen_tokens:
                doc_frequency[token] += 1
                seen_tokens.add(token)

            doc_lengths[file_name] += 1

    # Second pass: Compute TF-IDF for lightweight index
    total_docs = len(data)
    for token, docs in heavyweight_index.items():
        idf = math.log10(total_docs / doc_frequency[token])
        for file_name, positions in docs.items():
            tf = len(positions)
            tf_idf = (1 + math.log10(tf)) * idf
            lightweight_index[token][file_name] = tf_idf

    return lightweight_index, heavyweight_index



def save_inverted_index(lightweight_index, heavyweight_index, lw_output_file, hw_output_file):
    """
    Save both lightweight and heavyweight inverted indexes using gzip to save storage.
    """
    # Save lightweight index
    with gzip.open(lw_output_file, 'wt', encoding='utf-8') as file:
        json.dump(lightweight_index, file, ensure_ascii=False)

    # Save heavyweight index
    with gzip.open(hw_output_file, 'wt', encoding='utf-8') as file:
        json.dump({word: {doc: positions for doc, positions in docs.items()}
                  for word, docs in heavyweight_index.items()}, file, ensure_ascii=False)
        
def save_inverted_index_pickle(lightweight_index, heavyweight_index, lw_output_file, hw_output_file):
    """
    使用pickle保存轻量级和重量级倒排索引
    """
    # 保存轻量级索引
    with open(lw_output_file, 'wb') as file:
        pickle.dump(lightweight_index, file)

    # 保存重量级索引
    with open(hw_output_file, 'wb') as file:
        pickle.dump(heavyweight_index, file)

if __name__ == "__main__":        
    input_dir = '../processed_data/'         
    lw_output_file = 'engine/lightweight_index.pkl'
    hw_output_file = 'engine/heavyweight_index.pkl'
    data = load_data(input_dir)
    lightweight_index, heavyweight_index = create_inverted_index(data)
    save_inverted_index_pickle(lightweight_index, heavyweight_index, lw_output_file, hw_output_file)
