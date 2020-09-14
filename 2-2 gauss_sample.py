import math
import random

def gusaa_pdf(x):
    y = 1.0 / (math.sqrt(2 * math.pi) * sigma) * \
        math.exp(-math.pow(x - mu, 2.0) / (2 * sigma * sigma))
    return y

def guass_sample(mu, sigma):
    x_min = -3 * sigma
    x_max = 3 * sigma
    x_intv = x_max - x_min
    y_min = 0
    y_max = 1.0 / math.sqrt(2 * math.pi)
    y_intv = y_max - y_min
    while True:
        x = x_min + x_intv * random.random()
        y = y_min + y_intv * random.random()
        if y < gusaa_pdf(x):
            return x


def mean_var(arr):
    dim = len(arr)
    if dim == 0:
        return (0, 0)
    sumOrig = 0.0
    sumSquare = 0.0
    for ele in arr:
        sumOrig += ele
        sumSquare += ele**2
    mean = sumOrig / dim
    variance = sumSquare / dim - mean**2
    return (mean, variance)


if __name__ == '__main__':
    mu = 3.0
    sigma = 5.0
    arr = []
    for i in xrange(100000):
        arr.append(guass_sample(mu, sigma))
    print mean_var(arr)
