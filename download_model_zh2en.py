from modelscope import snapshot_download
model_dir = snapshot_download("damo/nlp_csanmt_translation_zh2en", revision = "v1.0.1",cache_dir="./model")