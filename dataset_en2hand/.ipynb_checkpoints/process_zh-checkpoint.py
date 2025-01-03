import jieba

fR = open('train.zh', 'r', encoding='UTF-8')
fW = open('train.zh.tok', 'w', encoding='UTF-8')

for sent in fR: 
    sent = fR.read()
    sent_list = jieba.cut(sent)
    fW.write(' '.join(sent_list))

fR.close()
fW.close()
