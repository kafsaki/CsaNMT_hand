from flask import Flask, request, jsonify
from test_local_zh2en import zh2en
from test_local_en2zh import en2zh

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate():
    print("\033[32mServer: receiving data...\033[0m")
    # 接收前端发送的JSON数据
    data = request.get_json()
    print(f"\033[32mreceived data: {data}\033[0m")
    recognition = data.get("recognition", [])

    if not recognition:
        return jsonify({"status": "error", "message": "No recognition data provided"}), 400
        
    # 去掉中间空格。很奇怪，我在传输到服务器之前就去除了，服务器接收后又给我加上了）
    recognition[0] = recognition[0].replace(" ", "")
    
    # 打印输入数据
    print(f"\033[32minput:{recognition}\033[0m");

    # 进行中文到英文的翻译
    middle_output = zh2en(recognition)
    print(f"\033[32mmiddle output:{middle_output}\033[0m")

    # 进行英文到中文的翻译
    output = en2zh(middle_output)
    print(f"\033[32moutput:{output}\033[0m")

    # 返回翻译结果给前端
    return jsonify({"status": "success", "translation": output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
