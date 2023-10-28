from miditok import REMI
import os
import pandas as pd
from tqdm import tqdm

# keep all file names, texts, midi_tokens and have an empty column for text_tokens
df = pd.DataFrame(columns=['name', 'text', 'midi_tokens', 'text_tokens'])
df = df.set_index(['name'])

print(df)

midi_tokenizer = REMI()
midi_path = 'data/midis/'
text_path = 'data/texts/'

midi_list = os.listdir(midi_path)

for i in tqdm(range(len(midi_list))):
    m = midi_list[i]
    file_name = m.split('.')[0]
    midi_tokens = midi_tokenizer( midi_path + m )
    with open(text_path + file_name + '.txt', 'r') as file:
        text = file.read().rstrip()
    df.at[file_name, 'text'] = text
    df.at[file_name, 'midi_tokens'] = midi_tokens[0].tokens
# end for

# save results
df.to_pickle('data/' + 'test_df.pkl')
df.to_csv('data/' + 'test_df.csv')