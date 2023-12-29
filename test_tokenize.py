from miditok import REMI
from keras.preprocessing.text import Tokenizer
import os
import pandas as pd
from tqdm import tqdm

# keep all file names, texts, midi_tokens and have an empty column for text_tokens
df = pd.DataFrame(columns=['name', 'text', 'midi_tokens', 'text_tokens'])
df = df.set_index(['name'])

# keep all texts for tokenization
texts = []

midi_tokenizer = REMI()
midi_path = 'data/midis/'
text_path = 'data/texts/'

midi_list = os.listdir(midi_path)

for i in tqdm(range(len(midi_list[:10]))):
    m = midi_list[i]
    file_name = m.split('.')[0]
    midi_tokens = midi_tokenizer( midi_path + m )
    with open(text_path + file_name + '.txt', 'r') as file:
        text = '<START> ' + file.read().rstrip() + ' <EOS>'
        texts.append( text )
    df.at[file_name, 'text'] = text
    df.at[file_name, 'midi_text'] = '<START> ' + (' ').join(midi_tokens[0].tokens) + ' <EOS>'
# end for

# text tokenizer
# remove # from the filters to accept A# etc
text_tokenizer = Tokenizer(filters='!"$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n')
text_tokenizer.fit_on_texts(texts)
# midi text tokenizer
midi_text_tokenizer = Tokenizer(filters='')
midi_text_tokenizer.fit_on_texts(texts)
print(texts[:2])
print(text_tokenizer.texts_to_sequences(texts[:2]))
# print(midi_tokens)

for i in tqdm(range(len(midi_list[:10]))):
    m = midi_list[i]
    file_name = m.split('.')[0]
    df.at[file_name, 'music_ids']

# save results
df.to_pickle('data/' + 'test_df.pkl')
df.to_csv('data/' + 'midi_text.csv')