from pickle import load
import pandas as pd
from numpy.random import shuffle
from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences # produced error
from keras.utils import pad_sequences # found on stack overflow
from tensorflow import convert_to_tensor, int64
import numpy as np

class PrepareDataset:
    def __init__(self,**kwargs):
        super(PrepareDataset, self).__init__(**kwargs)
        self.n_sentences = 10000
        self.train_split = 0.9
    # end init

    def create_tokenizer(self, dataset):
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(dataset)
        return tokenizer
    # end create_tokenizer

    def find_seq_length(self, dataset):
        return max(len(seq.split()) for seq in dataset)
    # end find_seq_length

    def find_vocab_size(self, tokenizer, dataset):
        tokenizer.fit_on_texts(dataset)
        return len(tokenizer.word_index) + 1
    # end find_vocab_size

    def __call__(self, filename, **kwargs):
        with open(filename, 'rb') as f:
            df = load(f)
        d = np.array( list( zip(df['midi_text'],df['text']) ) )
        dataset = d[:self.n_sentences, :]
        # for i in range(dataset[:,0].size):
        #     dataset[i][0] = '<START> ' + dataset[i][0] + ' <EOS>'
        #     dataset[i][1] = '<START> ' + dataset[i][1] + ' <EOS>'
        # shuffle and get training data
        shuffle(dataset) # no return
        train = dataset[:int(self.n_sentences * self.train_split)]
        # Prepare tokenizer for the encoder input
        enc_tokenizer = self.create_tokenizer(train[:, 0])
        enc_seq_length = self.find_seq_length(train[:, 0])
        enc_vocab_size = self.find_vocab_size(enc_tokenizer, train[:, 0])
        # Encode and pad the input sequences
        trainX = enc_tokenizer.texts_to_sequences(train[:, 0])
        trainX = pad_sequences(trainX, maxlen=enc_seq_length, padding='post')
        trainX = convert_to_tensor(trainX, dtype=int64)
        # Prepare tokenizer for the decoder input
        dec_tokenizer = self.create_tokenizer(train[:, 1])
        dec_seq_length = self.find_seq_length(train[:, 1])
        dec_vocab_size = self.find_vocab_size(dec_tokenizer, train[:, 1])
        
        # Encode and pad the input sequences
        trainY = dec_tokenizer.texts_to_sequences(train[:, 1])
        trainY = pad_sequences(trainY, maxlen=dec_seq_length, padding='post')
        trainY = convert_to_tensor(trainY, dtype=int64)
        return trainX, trainY, train, enc_seq_length, dec_seq_length, enc_vocab_size, dec_vocab_size
    # end call
