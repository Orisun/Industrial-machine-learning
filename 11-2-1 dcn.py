# coding:utf-8

import numpy as np
from keras.layers import Input, Dense, Activation, Concatenate, Multiply, Add, Embedding, Flatten, BatchNormalization
from keras.models import Model
from keras.optimizers import Adam

# 假设有3个离散特征，每个特征分别有3、4、2个取值
categorical_value_count = [3, 4, 2]
categorical_feature_count = len(categorical_value_count)
F = 8  # v向量的维度为8

def build_cross_net(input):
    x0 = Concatenate()(input)  # 对Embedding得到的稠密向量进行拼接
    xl = x0
    for i in xrange(4):  # 4层Cross
        tmp = Dense(1, use_bias=True)(xl)  # 根据矩阵乘法的结合律，先计算xl*w，得到一维系数
        tmp = Multiply()([x0, tmp])  # x0中每一个元素乘以上一步得到的系数
        xl = Add()([xl, tmp])  # 加上当前的xl，得到下一层的xl
    return xl

def build_dnn(input):
    deep_in = Concatenate()(input)
    deep_out = Dense(8)(deep_in)
    deep_out = BatchNormalization()(deep_out)  # 批量归一化
    deep_out = Activation("relu")(deep_out)
    deep_out = Dense(4)(deep_out)
    deep_out = BatchNormalization()(deep_out)
    deep_out = Activation("relu")(deep_out)
    return deep_out

def build_deep_fm():
    inputs = []
    f_dim_vectors = []
    for i in xrange(categorical_feature_count):
        cate_in = Input((1,))  # 每个离散特征的输入是1维向量，而非one-hot向量
        inputs.append(cate_in)
        f_dim_vector = Embedding(categorical_value_count[i], F, input_length=1)(cate_in)
        f_dim_vector = Flatten()(f_dim_vector)
        f_dim_vectors.append(f_dim_vector)
    cross_net = build_cross_net(f_dim_vectors)  # CrossNet
    deep_out = build_dnn(f_dim_vectors)  # 深层网络
    # 结合CrossNet和深层网络
    concat_fm_deep = Concatenate()([cross_net, deep_out])
    outputs = Dense(1, activation="sigmoid")(concat_fm_deep)
    model = Model(inputs=inputs, outputs=outputs)
    solver = Adam(lr=0.01, decay=0.1)
    model.compile(optimizer=solver, loss='binary_crossentropy', metrics=['acc'])
    return model

if __name__ == "__main__":
    # 构造虚拟数据
    sample = 1000
    X = []
    Y = np.random.randint(low=0, high=2, size=(sample, 1))
    for i in xrange(categorical_feature_count):
        feature = np.random.randint(low=0, high=categorical_value_count[i], size=(sample, 1))
        X.append(feature)

    model = build_deep_fm()
    model.fit(X, Y, batch_size=256, epochs=5)