from modelscope.models import Model
model_id = 'damo/nlp_csanmt_translation_en2zh'
model = Model.from_pretrained(model_id)
from modelscope.exporters import TfModelExporter
output_files = TfModelExporter.from_model(model).export_saved_model(output_dir='./CSANMT_en2zh')
print(output_files) # {'model': '/tmp'}
