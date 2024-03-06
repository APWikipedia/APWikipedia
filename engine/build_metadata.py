import os
import json

def load_tags(tags_file):
    with open(tags_file, 'r', encoding='utf-8') as file:
        tags_data = json.load(file)
    return tags_data

def build_metadata(input_dir, tags_file):
    tags_data = load_tags(tags_file)
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
                    tags = tags_data.get(title, [])  # 根据标题获取tags，如果没有找到，则默认为空列表
                    meta = {
                        "title": title,
                        "url": article.get("url", ""),
                        "summary": summary,
                        "tags": tags,  # 添加tags
                        "file_name": os.path.relpath(file_path, input_dir)  # 相对路径
                    }
                    metadata.append(meta)
    return metadata

def save_metadata(metadata, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(metadata, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    input_dir = 'data/'  # 原始数据目录
    tags_file = 'engine/labels.json'  # 标签数据文件
    output_file = 'engine/metadata.json'  # 元数据输出文件
    metadata = build_metadata(input_dir, tags_file)
    save_metadata(metadata, output_file)
