from test_local_zh2en import zh2en
from test_local_en2zh import en2zh

input = ["你好吗?", "我很好，谢谢!你呢?", "你知道你在哪里吗?", "再见!"]
middle_output = []
output = []

print(f"\033[32minput:{input}\033[0m");
middle_output = zh2en(input)
print(f"\033[32mmiddle output:{middle_output}\033[0m")
output = en2zh(middle_output)
print(f"\033[32moutput:{output}\033[0m")