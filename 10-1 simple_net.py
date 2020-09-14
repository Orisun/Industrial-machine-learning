# coding=utf-8

import numpy as np
from keras.layers import Input, Dense
from keras.models import Model
from keras.utils import plot_model

# 定义网络结构
input = Input(shape=(3,))
dense_layer = Dense(units=2, activation='softmax')
output = dense_layer(input)
model = Model(inputs=[input], outputs=[output])
# 画出网络结构
plot_model(model, to_file="simple_net.png", show_shapes=True)

# 生成虚拟数据
x_train = np.random.random((100, 3))
y_train = np.random.randint(low=0, high=1, size=(100, 2))
# 配置训练过程
model.compile(optimizer="sgd", loss="categorical_crossentropy")
# 开始训练
model.fit(x_train, y_train, batch_size=10, epochs=2)
# 打印训练完成后的权值
print dense_layer.get_weights()[0]

# 用训练好的模型预测新数据
x_test = np.random.random((1, 3))
y_pred = model.predict(x_test)
print y_pred