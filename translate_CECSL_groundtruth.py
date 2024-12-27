import json
from test_local_zh2en import zh2en
from test_local_en2zh import en2zh

# 读取更新后的 JSON 文件
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 保存更新后的 JSON 文件
def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 主程序
if __name__ == '__main__':
    json_file_path = 'CE-CSL.json'
    json_data = load_json(json_file_path)
    
    # 提取所有 'groundtruth' 字段，存入一个列表
    groundtruth_list = [entry['groundtruth'] for entry in json_data if entry.get('groundtruth')]

    print(f"Total groundtruth items to translate: {len(groundtruth_list)}")

    # 分批翻译：每次处理 10 个 'groundtruth'
    batch_size = 10
    total_batches = (len(groundtruth_list) + batch_size - 1) // batch_size  # 向上取整

    for batch_num in range(total_batches):
        # 处理当前批次
        start_index = batch_num * batch_size
        end_index = min((batch_num + 1) * batch_size, len(groundtruth_list))

        # 提取当前批次的 groundtruth
        current_batch = groundtruth_list[start_index:end_index]

        # 打印当前批次的信息
        print(f"\nProcessing batch {batch_num + 1}/{total_batches} (Groundtruth {start_index + 1} to {end_index})")
        
        # 使用 zh2en 翻译中文到英文
        middle_output = zh2en(current_batch)
        print(f"Middle output (zh2en) for batch {batch_num + 1}: {middle_output}")

        # 使用 en2zh 将英文翻译回中文
        output = en2zh(middle_output)
        print(f"Output (en2zh) for batch {batch_num + 1}: {output}")

        # 将翻译结果填入 JSON 数据
        for i, entry in enumerate(json_data[start_index:end_index]):
            entry['translation'] = output[i]  # 假设翻译结果顺序与原数据顺序一致

        # 实时保存当前批次的翻译结果
        save_json(json_data, 'CE-CSL-translated-groundtruth.json')
        print(f"Batch {batch_num + 1} translations saved.")

    print("All batches processed and saved to CE-CSL-translated-groundtruth.json")
