def stack_bi_lstm(x_train, y_train, x_test, y_test):
    main_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='float64')
    embedding_matrix = np.zeros((WORD_COUNT + 1, WORD_VEC_DIM))
    for i in xrange(1, WORD_COUNT+1):
        embedding_matrix[i] = np.random.random(WORD_VEC_DIM).tolist()
    embed = Embedding(WORD_COUNT + 1, WORD_VEC_DIM, weights=[embedding_matrix], input_length=MAX_SEQUENCE_LENGTH, trainable=True)(main_input)

    # 两层RNN堆叠时，第一层把return_sequences设为True
    out = Bidirectional(LSTM(units=128, dropout=0.2, recurrent_dropout=0.1, return_sequences=True))(embed)
    # 可以把LSTM直接替换成GRU
    out = Bidirectional(LSTM(units=128, dropout=0.2, recurrent_dropout=0.1))(out)
    out = Dropout(0.5)(out)
    main_output = Dense(MAX_SEQUENCE_LENGTH, activation='softmax')(out)
    model = Model(inputs=main_input, outputs=main_output)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    x_train_padded_seqs = pad_sequences(x_train, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post", dtype="float64")
    y_train_padded_seqs = pad_sequences(y_train, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post", dtype="float64")
    x_test_padded_seqs = pad_sequences(x_test, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post", dtype="float64")
    y_test_padded_seqs = pad_sequences(y_test, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post", dtype="float64")

    model.fit(x_train_padded_seqs, y_train_padded_seqs, batch_size=64, epochs=100, validation_data=(x_test_padded_seqs, y_test_padded_seqs))