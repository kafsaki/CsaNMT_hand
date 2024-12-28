# CsaNMT_hand
使用CsaNMT的zh_en&amp;en_zh对手语进行翻译

## 运行流程：

#### 模型准备：

运行download_model_en2zh.py  download_model_zh2en.py 下载模型

运行trans_mdoel_en2zh.py  trans_mdoel_zh2en.py 转换模型

#### 本地测试：

运行test_local_zh2en2zh.py进行测试

运行translate_CECSL_groundtruth.py  translate_CECSL_recognition.py 分别对真实手语序列和识别手语序列进行翻译

（因为翻译后json已经存在，需要删除两个CE-CSL-translated文件）

#### 开启服务，实时翻译前端数据：

运行APP_translate_recognition.py

## 环境配置：

如果嫌配置环境麻烦，可以使用damodel的Pytorch2.1.2镜像，然后使用conda创建python=3.8.18环境，安装：

pip install:

tensorflow===2.13.0

modelscope===1.9.5 

torch-2.1.0+cu121-cp38-cp38-linux_x86_64.whl

flask

jieba

sacremoses

subword_nmt
