# CsaNMT_hand
使用CsaNMT的zh_en&amp;en_zh对手语进行翻译

## 运行流程：

#### 模型准备：

运行download_model_en2zh.py  download_model_zh2en.py 下载模型

运行trans_mdoel_en2zh.py  trans_mdoel_zh2en.py 转换模型

#### 本地测试：

运行test_local_zh2en2zh.py进行测试

#### 手语翻译：

运行translate_CECSL_groundtruth.py  translate_CECSL_recognition.py 分别对真实手语序列和识别手语序列进行翻译

（因为翻译后json已经存在，需要删除两个CE-CSL-translated文件）

#### 开启服务，实时翻译前端数据：

运行APP_translate_recognition.py

#### 构建英文转中文手语句子数据集，对模型微调：

要加强模型对手语句子的翻译能力，只需对en2zh进行微调，也就是增强模型从中间英语结果到最终手语句子的能力

运行generate_dataset_en2hand.py 将CE-CSL-translated-groundtruth.json中的英文中间结果和真实中文句子提取到dataset_en2hand （已提取）

运行dataset_en2hand/process_zh.py 使用jieba将中文分词 （已分词）

安装mosesdecoder，运行perl tokenizer.perl -l en < train.en > train.en.tok （已分词）

完成上述模型下载后，将dataset_en2hand文件夹复制到model/damo/nlp_csanmt_translation_en2zh下

修改model/damo/nlp_csanmt_translation_en2zh的configuration.json，替换为项目根目录下的configuration.json

运行项目根目录下的train.py


## 环境配置：

如果嫌配置环境麻烦，可以使用damodel的Pytorch2.1.2镜像，然后使用conda创建python=3.8.18环境，安装：

**(update: cuda12.1只能用cpu跑tf，需要切换到cuda11.8，请更换版本或者使用带cuda11.8的镜像)**

pip install:

tensorflow===2.13.0

modelscope===1.9.5 

torch-2.1.0+cu121-cp38-cp38-linux_x86_64.whl （需要在官网下载whl）**(update: torch-2.1.0+cu118-cp38-cp38-linux_x86_64.whl)**


flask

jieba

sacremoses

subword_nmt
