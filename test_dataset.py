from datatools.text_midi import PrepareDataset

dataset = PrepareDataset()
trainX, trainY, train_orig, enc_seq_length, dec_seq_length, enc_vocab_size, dec_vocab_size = dataset('data/texts_df.pkl')

print(trainX.shape)
print(trainY.shape)