import tensorflow as tf
from modelscope.models.base import Model
from modelscope.utils.constant import ModelFile, Tasks
from modelscope.utils.config import Config
from sacremoses import MosesDetokenizer, MosesPunctNormalizer, MosesTokenizer
from subword_nmt import apply_bpe
from modelscope.outputs import OutputKeys
import numpy as np
import time

if tf.__version__ >= '2.0':
    tf = tf.compat.v1
    tf.disable_eager_execution()

def en2zh(input):
    cfg_dir = "./model/damo/nlp_csanmt_translation_en2zh/configuration.json"
    cfg = Config.from_file(cfg_dir)
    
    src_vocab_dir = "./model/damo/nlp_csanmt_translation_en2zh/src_vocab.txt"
    # _src_vocab 是一个字典，key是英文src_vocab.txt中的一行，value是index，length = 49998, _trg_rvocab同理
    _src_vocab = dict([
                (w.strip(), i) for i, w in enumerate(open(src_vocab_dir))
            ])
    
    trg_vocab_dir = "./model/damo/nlp_csanmt_translation_en2zh/trg_vocab.txt"
    _trg_rvocab = dict([
                (i, w.strip()) for i, w in enumerate(open(trg_vocab_dir))
            ])
    
    input_wids = tf.placeholder(
                dtype=tf.int64, shape=[None, None], name='input_wids')
    output = {}
    
    _src_lang = cfg['preprocessor']['src_lang'] #en
    _tgt_lang = cfg['preprocessor']['tgt_lang'] #zh
    
    _src_bpe_path = "./model/damo/nlp_csanmt_translation_en2zh/bpe.en"
    
    _punct_normalizer = MosesPunctNormalizer(lang=_src_lang)
    _tok = MosesTokenizer(lang=_src_lang)
    _detok = MosesDetokenizer(lang=_tgt_lang)
    _bpe = apply_bpe.BPE(open(_src_bpe_path))
    
    # input = ["How are you?", "OK, I am fine. Thank you! And you?", "Do you know where you are?", "Mr.Zhang test firstly!"]
    
    input = [_punct_normalizer.normalize(item) for item in input]
    
    aggressive_dash_splits = True
    
    if (_src_lang in ['es', 'fr'] and _tgt_lang == 'en') or (_src_lang == 'en' and _tgt_lang in ['es', 'fr']):
        aggressive_dash_splits = False
    
    input_tok = [
                    _tok.tokenize(
                        item,
                        return_str=True,
                        aggressive_dash_splits=aggressive_dash_splits)
                    for item in input
                ]
    input_bpe = [
                _bpe.process_line(item).strip().split() for item in input_tok
            ]
    
    MAX_LENGTH = max([len(item) for item in input_bpe])#200
    
    input_ids = np.array([[
                _src_vocab[w] if w in _src_vocab else
                cfg['model']['src_vocab_size'] - 1 for w in item
            ] + [0] * (MAX_LENGTH - len(item)) for item in input_bpe])
    
    tf_config = tf.ConfigProto(allow_soft_placement=True)
    
    sess = tf.Session(graph=tf.Graph(), config=tf_config)
    # Restore model from the saved_modle file, that is exported by TensorFlow estimator.
    MetaGraphDef = tf.saved_model.loader.load(sess, ['serve'], './CSANMT_en2zh')
    
    # SignatureDef protobuf
    SignatureDef_map = MetaGraphDef.signature_def
    SignatureDef = SignatureDef_map['translation_signature']
    # TensorInfo protobuf
    X_TensorInfo = SignatureDef.inputs['input_wids']
    y_TensorInfo = SignatureDef.outputs['output_seqs']
    X = tf.saved_model.utils.get_tensor_from_tensor_info(
        X_TensorInfo, sess.graph)
    y = tf.saved_model.utils.get_tensor_from_tensor_info(
        y_TensorInfo, sess.graph)
    sttime = time.time()
    outputs = sess.run(y, feed_dict={X: input_ids})
    
    x, y, z = outputs.shape
    
    translation_out = []
    for i in range(x):
        output_seqs = outputs[i]
        wids = list(output_seqs[0]) + [0]
        wids = wids[:wids.index(0)]
        translation = ' '.join([
            _trg_rvocab[wid] if wid in _trg_rvocab else '<unk>'
            for wid in wids
        ]).replace('@@ ', '').replace('@@', '')
        translation_out.append(_detok.detokenize(translation.split()))
    return translation_out
