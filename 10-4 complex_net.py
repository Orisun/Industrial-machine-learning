# -*- coding:utf-8 -*-

import numpy as np
from keras.layers import Input, Dense, Concatenate, Multiply, Reshape, Embedding
from keras.models import Model
from keras.utils import plot_model


def build_model():
    x0 = Input(shape=(8,), name="x0")
    x1 = Input(shape=(1,), name="x1")
    embed = Embedding(input_dim=10, output_dim=8, input_length=1, name="embed")(x1)  # Embedding层的输出尺寸为(batch_size, sequence_length, output_dim)，即此处embed的尺寸为(None, 1, 8)。input_dim=10，则输入的索引值必须小于10
    embed = Reshape(target_shape=(8,))(embed)  # 把embed的尺寸转为(None, 8)，target_shape中不包含表示批量的轴
    concat1 = Concatenate(axis=-1, name="concat1")([x0, embed])
    dense1 = Dense(units=4, name="dense1")(concat1)
    output1 = Dense(units=1, name="output1")(dense1)
    dense2 = Dense(units=4, name="dense2")(dense1)
    mult = Multiply(name="mult")([x0, embed])
    dense3 = Dense(units=4, name="dense3")(mult)
    concat2 = Concatenate(name="concat2")([dense2, dense3])
    dense4 = Dense(units=4, name="dense4")(concat2)
    output2 = Dense(units=1, name="output2")(dense4)
    model = Model(inputs=[x0, x1], outputs=[output1, output2], name="complex_net")
    plot_model(model, to_file="complex_net.png")  # 画出网络结构
    return model


def prepare_data():
    batch = 10000
    numerical_x = np.random.random((batch, 8))  # (10000, 8)
    categorical_x = np.random.randint(0, 10, (batch, 1))  # (10000, 1) 索引值必须小于10
    y = np.random.randint(0, 2, batch)  # (10000,)  0/1二分类问题
    return numerical_x, categorical_x, y


model = build_model()
model.compile(optimizer="sgd", loss='binary_crossentropy', metrics=['acc'])
numerical_x, categorical_x, y = prepare_data()
model.fit([numerical_x, categorical_x], [y, y], batch_size=100, epochs=1)