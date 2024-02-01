import json
import os


def merge_json_files(original_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    for root, dirs, files in os.walk(original_dir):
        merged_data = []
        for file in files:
            if file.endswith(".json") and file != "articles_index.json":
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    merged_data.append(
                        {"file_name": os.path.splitext(file)[0], "content": data}
                    )

        if merged_data:
            folder_name = os.path.basename(root)
            output_path = os.path.join(output_dir, folder_name + ".json")
            with open(output_path, "w", encoding="utf-8") as output_file:
                json.dump(merged_data, output_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    input_dir = "data/"
    output_dir = "merged_data/"
    merge_json_files(input_dir, output_dir)
