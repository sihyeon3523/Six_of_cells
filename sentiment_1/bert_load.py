import os
import pickle
import logging
import numpy as np

import tensorflow as tf
# import tensorflow_addons as tfa # for using Rectified-Adam optimizer (instead of Adam optimizer) <- TF 2.5.0 에서 사용 불가
from tensorflow.keras import layers, initializers, losses, optimizers, metrics, callbacks
import transformers
from transformers import TFBertModel
import sentencepiece as spm
from .bert_tokenizer import KoBertTokenizer


# Random seed 고정
tf.random.set_seed(1234)
np.random.seed(1234)

# Transformers logging level 변경 (WARNING -> ERROR) @ https://huggingface.co/transformers/main_classes/logging.html
transformers.logging.set_verbosity(transformers.logging.ERROR)

# Tensorflow logging level 변경
tf.get_logger().setLevel(logging.ERROR)



def create_bert_model(max_length=300):

    bert_base_model = TFBertModel.from_pretrained("monologg/kobert", from_pt=True)

    input_token_ids   = layers.Input((max_length,), dtype=tf.int32, name='input_token_ids')   # tokens_tensor
    input_masks       = layers.Input((max_length,), dtype=tf.int32, name='input_masks')       # masks_tensor
    input_segments    = layers.Input((max_length,), dtype=tf.int32, name='input_segments')    # segments_tensor

    bert_outputs = bert_base_model([input_token_ids, input_masks, input_segments])
    # bert_outputs -> 0 : 'last_hidden_state' & 1 : 'pooler_output' == the embedding of [CLS] token (https://j.mp/3iTNa6e)

    bert_outputs = bert_outputs[1] # ('pooler_output', <KerasTensor: shape=(None, 768) dtype=float32 (created by layer 'tf_bert_model')>)
    bert_outputs = layers.Dropout(0.2)(bert_outputs)
    final_output = layers.Dense(units=4, activation='softmax', kernel_initializer=initializers.TruncatedNormal(stddev=0.02), name="classifier")(bert_outputs)

    model = tf.keras.Model(inputs=[input_token_ids, input_masks, input_segments], outputs=final_output)

    model.compile(optimizer=optimizers.Adam(learning_rate=1e-5),
                  # optimizer=tfa.optimizers.RectifiedAdam(learning_rate=1e-5, weight_decay=0.0025, warmup_proportion=0.05), # TF 2.5.0 에서 사용 불가
                  loss=losses.SparseCategoricalCrossentropy(),
                  metrics=[metrics.SparseCategoricalAccuracy()])

    # 저장된 parameter를 loading
    model.load_weights(filepath='./trained_KoBERT/best_bert_weights.h5')

    return model



def load_bert_tokenizer():

    tokenizer = KoBertTokenizer.from_pretrained('monologg/kobert')

    return tokenizer
