x_list = []
y_list = []
for i in xrange(sequence_length):
    x = Input(shape=(index_count + 1,))
    x_list.append(x)
    y = Dense(dense_vector_dim)(x)  # (None, 100)
    y = Reshape((1, -1))(y)  # (None, 1, 100)
    y_list.append(y)
y = Concatenate(axis=1)(y_list)  # (None, 3, 100)