import os
import json

def build_metadata(input_dir):
    metadata = []
    for root, dirs, files in os.walk(input_dir):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    article = json.load(file)
                    title = article.get("title", file_name.replace('.json', ''))
                    content = article.get("content", "")
                    summary = content[0:100]
                    meta = {
                        "title": title,
                        "url": article.get("url", ""),
                        "summary": summary,
                        "file_name": os.path.relpath(file_path, input_dir)  # 相对路径
                    }
                    metadata.append(meta)
    return metadata

def save_metadata(metadata, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(metadata, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    input_dir = 'data/'  # 原始数据目录
    output_file = 'engine/metadata.json'  # 元数据输出文件
    metadata = build_metadata(input_dir)
    save_metadata(metadata, output_file)
