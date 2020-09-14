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
    print mean_var([1, 2, 3, 4, 5, 6, 7, 8])
