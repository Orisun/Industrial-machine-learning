# -*- coding:utf-8 -*-

import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model
from keras.layers import Dense, Embedding, Input, Activation, LSTM, Bidirectional, GRU
from keras.layers import Convolution1D, Flatten, Dropout, MaxPool1D
from keras.layers import BatchNormalization
from keras.layers.merge import concatenate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 语料中词的个数
WORD_COUNT = 10000
# 词向量长度
WORD_VEC_DIM = 100
# 一条文本中最多包含几个词
MAX_SEQUENCE_LENGTH = 20


def text_cnn(x_train, y_train, x_test, y_test):
    main_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='float64')
    embedding_matrix = np.zeros((WORD_COUNT + 1, WORD_VEC_DIM))
    for i in xrange(1, WORD_COUNT+1):
        embedding_matrix[i] = np.random.random(WORD_VEC_DIM).tolist()
    embed = Embedding(WORD_COUNT + 1,  # 词的个数
                      WORD_VEC_DIM,    # 词向量长度
                      weights=[embedding_matrix],
                      input_length=MAX_SEQUENCE_LENGTH,
                      trainable=True,  # 在训练过程中可更新
                      )(main_input)
    cnvs = []
    filter_size = 64	# 每种卷积核对应几个filter(或称为通道)
    for kernel_size in [2, 3, 4, 5]:
        out = Convolution1D(filter_size, kernel_size, padding='valid')(embed)
        out = BatchNormalization()(out)
        out = Activation('relu')(out)
        out = MaxPool1D(pool_size=MAX_SEQUENCE_LENGTH - kernel_size + 1)(out)
        cnvs.append(out)
    cnn = concatenate(cnvs, axis=-1)
    flat = Flatten()(cnn)
    drop = Dropout(0.5)(flat)
    fc = Dense(4 * MAX_SEQUENCE_LENGTH)(drop)
    bn = BatchNormalization()(fc)
    main_output = Dense(MAX_SEQUENCE_LENGTH, activation='softmax')(bn)
    model = Model(inputs=main_input, outputs=main_output)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    x_train_padded_seqs = pad_sequences(x_train, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post", dtype="float64")
    y_train_padded_seqs = pad_sequences(y_train, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post", dtype="float64")
    x_test_padded_seqs = pad_sequences(x_test, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post", dtype="float64")
    y_test_padded_seqs = pad_sequences(y_test, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post", dtype="float64")

    BATCH = 64  # mini-batch
    history = model.fit(x_train_padded_seqs, y_train_padded_seqs, batch_size=BATCH, epochs=100, validation_data=(x_test_padded_seqs, y_test_padded_seqs))

    plt.subplot(211)
    plt.title("Accuracy")
    plt.plot(history.history["acc"], color="g", label="Train")
    plt.plot(history.history["val_acc"], color="b", label="Test")
    plt.legend(loc="best")

    plt.subplot(212)
    plt.title("Loss")
    plt.plot(history.history["loss"], color="g", label="Train")
    plt.plot(history.history["val_loss"], color="b", label="Test")
    plt.legend(loc="best")

    plt.tight_layout()
    plt.show()
    plt.savefig("cnn_history.png", format="png")

    return model