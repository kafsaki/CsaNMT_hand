from modelscope import snapshot_download
model_dir = snapshot_download("damo/nlp_csanmt_translation_en2zh", revision = "v1.0.1",cache_dir="./model")