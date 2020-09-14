index_count = 10
dense_vector_dim = 100
sequence_length = 3
x = Input(shape=(sequence_length,))
embed_layer = Embedding(input_dim=index_count + 1, output_dim=dense_vector_dim, input_length=sequence_length)
y = embed_layer(x)  # (None, 3, 100)