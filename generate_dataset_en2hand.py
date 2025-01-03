import json

# 从外部文件1.json读取数据
def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 处理函数，分别将 translation_middle 和 origin 存入文件
def save_translations(data):
    with open("dataset_en2hand/train.en", "w", encoding="utf-8") as en_file, open("dataset_en2hand/train.zh", "w", encoding="utf-8") as zh_file:
        for item in data:
            # 将 translation_middle 写入 .en 文件
            en_file.write(item["translation_middle"] + "\n")
            # 将 origin 写入 .zh 文件
            zh_file.write(item["origin"] + "\n")

# 主函数
def main():
    # 读取外部文件1.json中的数据
    json_data = load_json_data("CE-CSL-translated-groundtruth.json")
    
    # 将数据保存到翻译文件
    save_translations(json_data)
    
    print("文件保存成功！")

# 执行程序
if __name__ == "__main__":
    main()
