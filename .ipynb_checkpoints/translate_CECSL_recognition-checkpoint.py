import json
import os
import shutil
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
    json_file_path = 'CE-CSL-translated-recognition.json'  # JSON 文件路径
    # 检查文件是否存在，如果不存在则从 CE-CSL.json 复制
    if not os.path.exists(json_file_path):
        print(f"{json_file_path} not found. Copying from CE-CSL.json...")
        shutil.copy('CE-CSL.json', json_file_path)
        print(f"File copied to {json_file_path}")
    # 读取目标 JSON 文件
    json_data = load_json(json_file_path)
    
    # 计算跳过的元素数，即那些已经翻译过的（有 translation 字段的）元素
    skipped_entries = [entry for entry in json_data if entry.get('translation', '') != '']
    skipped_count = len(skipped_entries)

    # 提取所有 'recognition' 字段，存入一个列表（跳过已经翻译过的项）
    recognition_list = [entry['recognition'] for entry in json_data[skipped_count:] if entry.get('recognition')]

    print(f"Total recognition items to translate: {len(recognition_list)}")
    print(f"Skipped entries: {skipped_count} entries have already been translated.")

    # 分批翻译：每次处理 10 个 'recognition'
    batch_size = 10
    total_batches = (len(recognition_list) + batch_size - 1) // batch_size  # 向上取整

    for batch_num in range(total_batches):
        # 处理当前批次
        start_index = batch_num * batch_size
        end_index = min((batch_num + 1) * batch_size, len(recognition_list))

        # 提取当前批次的 recognition
        current_batch = recognition_list[start_index:end_index]
        
        # 打印当前批次的信息
        print(f"\n\033[32mProcessing batch {batch_num + 1}/{total_batches} (Recognition {start_index + 1} to {end_index})\033[0m")
        print(f"\033[32mInput for batch {batch_num + 1}: {current_batch}\033[0m")
        # 使用 zh2en 翻译中文到英文
        middle_output = zh2en(current_batch)
        print(f"\033[32mMiddle output (zh2en) for batch {batch_num + 1}: {middle_output}\033[0m")

        # 使用 en2zh 将英文翻译回中文
        output = en2zh(middle_output)
        print(f"\033[32mOutput (en2zh) for batch {batch_num + 1}: {output}\033[0m")

        # 将翻译结果填入 JSON 数据，仅更新 translation 字段为空的项
        for i, entry in enumerate(json_data[skipped_count + start_index: skipped_count + end_index]):
            if entry.get('translation', '') == '':  # 仅当 translation 为空时才更新
                entry['translation_middle'] = middle_output[i]  # 创建新的 translation_middle 项
                entry['translation'] = output[i]  # 假设翻译结果顺序与原数据顺序一致

        # 实时保存当前批次的翻译结果
        save_json(json_data, 'CE-CSL-translated-recognition.json')
        print(f"\033[32mBatch {batch_num + 1} translations saved.\033[0m")

    print("All batches processed and saved to CE-CSL-translated-recognition.json")
