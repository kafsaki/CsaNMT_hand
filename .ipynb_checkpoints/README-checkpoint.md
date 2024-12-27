# CsaNMT_hand
使用CsaNMT的zh_en&amp;en_zh对手语进行翻译

运行流程：
运行download_model_en2zh.py  download_model_zh2en.py 下载模型
运行trans_mdoel_en2zh.py  trans_mdoel_zh2en.py 转换模型
运行test_local_zh2en2zh.py进行测试
运行translate_CECSL_groundtruth.py  translate_CECSL_recognition.py 分别对真实手语序列和识别手语序列进行翻译
（因为翻译后json已经存在，需要删除两个CE-CSL-translated文件）
