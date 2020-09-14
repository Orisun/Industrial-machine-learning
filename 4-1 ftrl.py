import numpy as np
import sys

NEAR_0 = 1e-10

class LR_CLS(object):
    '''用于二分类的LR
    '''

    @staticmethod
    def fn(w, x):
        '''决策函数为sigmoid函数'''
        return 1.0 / (1.0 + np.exp(-np.dot(x, w))).reshape(x.shape[0], 1)

    @staticmethod
    def loss(y, y_hat):
        '''交叉熵损失函数'''
        return np.sum(
            np.nan_to_num(-y * np.log(y_hat + NEAR_0) - (1 - y) * np.log(1 - y_hat + NEAR_0)))  # 加上NEAR_0避免出现log(0)

    @staticmethod
    def grad(y, y_hat, x):
        '''交叉熵损失函数对权重w的一阶导数'''
        return np.mean((y_hat - y) * x, axis=0)


class LR_REG(object):
    '''用回归的LR
    '''

    @staticmethod
    def fn(w, x):
        '''决策函数为sigmoid函数'''
        return 1.0 / (1.0 + np.exp(-np.dot(x, w))).reshape(x.shape[0], 1)

    @staticmethod
    def loss(y, y_hat):
        '''误差平方和损失函数'''
        return np.sum(np.nan_to_num((y_hat - y) ** 2)) / 2

    @staticmethod
    def grad(y, y_hat, x):
        '''误差平方和损失函数对权重w的一阶导数'''
        return np.mean((y_hat - y) * (1 - y_hat) * y_hat * x, axis=0)


class FTRL(object):

    def __init__(self, dim, l1, l2, alpha, beta, decisionFunc=LR_CLS):
        self.dim = dim
        self.decisionFunc = decisionFunc
        self.z = np.zeros(dim)
        self.n = np.zeros(dim)
        self.w = np.zeros(dim)
        self.l1 = l1
        self.l2 = l2
        self.alpha = alpha
        self.beta = beta

    def predict(self, x):
        return self.decisionFunc.fn(self.w, x)

    def update(self, x, y):
        self.w = np.array([0 if np.abs(self.z[i]) <= self.l1 else (np.sign(self.z[i]) * self.l1 - self.z[i]) / (self.l2 + (self.beta + np.sqrt(self.n[i])) / self.alpha) for i in xrange(self.dim)])
        y_hat = self.predict(x)
        g = self.decisionFunc.grad(y, y_hat, x)
        sigma = (np.sqrt(self.n + g * g) - np.sqrt(self.n)) / self.alpha
        self.z += g - sigma * self.w
        self.n += g * g
        return self.decisionFunc.loss(y, y_hat)

    def train(self, corpus_generator, verbos=False, epochs=100, batch=64):
        test_loss_history = []
        total = 0
        for itr in xrange(epochs):
            if verbos:
                sys.stderr.write("=" * 100 + "\n")
                sys.stderr.write("Epoch={:d}\n".format(itr))
            # 尽量使用mini batch，充分发挥numpy的并行计算能力
            mini_batch_x = []
            mini_batch_y = []
            n = 0
            for x, y in corpus_generator:
                n += 1
                mini_batch_x.append(x)
                mini_batch_y.append([y])
                if len(mini_batch_x) >= batch:
                    self.update(np.array(mini_batch_x), np.array(mini_batch_y))
                    if verbos:
                        Y_HAT = self.predict(np.array(mini_batch_x))
                        train_loss = self.decisionFunc.loss(np.array(mini_batch_y), Y_HAT) / len(mini_batch_x)
                        sys.stderr.write("{:d}/{:d} train loss: {:f}\n".format(n, total, train_loss))
                    mini_batch_x = []
                    mini_batch_y = []
            self.update(np.array(mini_batch_x), np.array(mini_batch_y))
            if total == 0:
                total = n
            if verbos:
                Y_HAT = self.predict(np.array(mini_batch_x))
                train_loss = self.decisionFunc.loss(np.array(mini_batch_y), Y_HAT) / len(mini_batch_x)
                sys.stderr.write("{:d}/{:d} train loss: {:f}\n".format(n, total, train_loss))