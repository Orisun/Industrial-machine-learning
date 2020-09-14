# coding=utf-8

import numpy as np
from keras import backend as K
from keras.layers import Input, Dense, Layer, Add, Activation
from keras.models import Model
from keras.utils import plot_model
from keras.initializers import RandomNormal, Constant


class MyDenseLayer(Layer):
    def __init__(self, units, **kargs):
        self.output_dim = units
        super(MyDenseLayer, self).__init__(**kargs)

    def build(self, input_shapes):
        trainable_input_shape = input_shapes[0]
        constant_input_shape = input_shapes[1]
        # 随机初始化weight
        self.trainable_kernel = self.add_weight(name="trainable", shape=(trainable_input_shape[1], self.output_dim),
                                                initializer=RandomNormal(), trainable=True)
        # 用常量初始化weight，且训练过程中保持不变
        self.constant_kernel = self.add_weight(name="constant", shape=(constant_input_shape[1], self.output_dim),
                                               initializer=Constant(np.array([1.0] * constant_input_shape[1])),
                                               trainable=False)
        super(MyDenseLayer, self).build(input_shapes)

    def call(self, inputs):
        return Add()([K.dot(inputs[0], self.trainable_kernel), K.dot(inputs[1], self.constant_kernel)])

    def compute_output_shape(self, input_shapes):
        return (input_shapes[0][0], self.output_dim)


input1 = Input(shape=(2,))
input2 = Input(shape=(3,))
dense_layer = MyDenseLayer(units=2)
output = dense_layer([input1, input2])
activation = Activation(activation="softmax")
output = activation(output)
model = Model(inputs=[input1, input2], outputs=[output])
# 画出网络结构
plot_model(model, to_file="multi_weight.png", show_shapes=True)

# 生成虚拟数据
x_train_1 = np.random.random((100, 2))
x_train_2 = np.random.random((100, 3))
y_train = np.random.randint(low=0, high=1, size=(100, 2))
# 配置训练过程
model.compile(optimizer="sgd", loss="categorical_crossentropy")
# 开始训练
model.fit([x_train_1, x_train_2], y_train, batch_size=10, epochs=2)
# 打印训练完成后的权值
print dense_layer.get_weights()[0]
print dense_layer.get_weights()[1]

# 用训练好的模型预测新数据
x_test_1 = np.random.random((1, 2))
x_test_2 = np.random.random((1, 3))
y_pred = model.predict([x_test_1, x_test_2])
print y_pred
