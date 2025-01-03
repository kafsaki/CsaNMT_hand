from modelscope.trainers.nlp import CsanmtTranslationTrainer

trainer = CsanmtTranslationTrainer(model="./model/damo/nlp_csanmt_translation_en2zh")
trainer.train()
