import json
from jiwer import wer
import re
import jieba

# def process_text(text):
#     # 去掉所有标点符号
#     text = re.sub(r'[^\w\s]', '', text)
#     # 在每个汉字之间添加空格
#     text = ' '.join(text)
#     return text

def process_text(text):
    # 使用 jieba 进行分词
    words = jieba.cut(text)
    # 在每个词之间添加空格
    text = ' '.join(words)
    return text

file_path = 'CE-CSL-translated-groundtruth.json'
# file_path = 'CE-CSL-translated-recognition.json'


# 读取 JSON 文件
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 初始化变量，用于累计 WER 总和
total_wer = 0
num_entries = len(data)

# 计算每一条记录的 WER
for entry in data:
    translation = entry.get('translation', '')
    origin = entry.get('origin', '')
    # print(translation)
    # print(origin)
    translation = process_text(translation)
    origin = process_text(origin)
    # 计算 WER 分数
    score = wer(origin, translation)
    total_wer += score
    # print(translation)
    # print(origin)

# 计算平均 WER
average_wer = total_wer / num_entries

# 输出结果
print(f'总共 {num_entries} 个条目，平均 WER: {average_wer:.4f}')
