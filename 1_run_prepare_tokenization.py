from miditok import REMI, TokenizerConfig
import os
import pandas as pd
from tqdm import tqdm

# keep all file names, texts, midi_tokens and have an empty column for text_tokens
df = pd.DataFrame(columns=['name', 'text', 'midi'])
df = df.set_index(['name'])

# load downstream
df_downstream_targets = pd.read_csv('data/' + 'downdstream_df.csv')
df_downstream_targets = df_downstream_targets.set_index(['name'])
downstream_keys = ['bars_number_key_idxs', 'tonic_idxs', 'mode_idxs', \
                   'register_key_idxs', 'speed_idxs']
df_downstream = pd.DataFrame(columns=['name', 'text', 'midi', 'bars_number_key_idxs',\
                                      'tonic_idxs', 'mode_idxs', 'register_key_idxs', 'speed_idxs'])
df_downstream = df_downstream.set_index(['name'])

#/ Our tokenizer's configuration
PITCH_RANGE = (21, 109)
BEAT_RES = {(0, 1): 8, (1, 2): 4, (2, 4): 2, (4, 8): 1}
NB_VELOCITIES = 24
SPECIAL_TOKENS = ["PAD", "MASK", "BOS", "EOS"]
USE_CHORDS = True # changed
USE_RESTS = False
USE_TEMPOS = True # changed
USE_TIME_SIGNATURE = False
USE_PROGRAMS = False
NB_TEMPOS = 32
TEMPO_RANGE = (50, 200)  # (min_tempo, max_tempo)
TOKENIZER_PARAMS = {
    "pitch_range": PITCH_RANGE,
    "beat_res": BEAT_RES,
    "nb_velocities": NB_VELOCITIES,
    "special_tokens": SPECIAL_TOKENS,
    "use_chords": USE_CHORDS,
    "use_rests": USE_RESTS,
    "use_tempos": USE_TEMPOS,
    "use_time_signatures": USE_TIME_SIGNATURE,
    "use_programs": USE_PROGRAMS,
    "nb_tempos": NB_TEMPOS,
    "tempo_range": TEMPO_RANGE,
}
config = TokenizerConfig(**TOKENIZER_PARAMS)
midi_tokenizer = REMI(config)

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
    df.at[file_name, 'midi'] = (' ').join(midi_tokens[0].tokens)
    # pass downstream
    df_downstream.at[file_name, 'text'] = text
    df_downstream.at[file_name, 'midi'] = (' ').join(midi_tokens[0].tokens)
    for k in downstream_keys:
        df_downstream.at[file_name, k] = df_downstream_targets.at[file_name, k]
# end for

# save results
df.to_pickle('data/' + 'texts_df.pkl')
df.to_csv('data/' + 'texts_df.csv')
# save downstream
df_downstream.to_csv('data/' + 'downstream_in_out_df.csv')


'''
# Constructs the vocabulary with BPE, from the token files
tokenizer.learn_bpe(
    vocab_size=10000,
    tokens_paths=list(Path(path_to_tokens).glob("**/*.json")),
    # tokens_paths=list(Path(path_to_tokens).glob("**/*.json")),
    start_from_empty_voc=False,
)

# Saving our tokenizer, to retrieve it back later with the load_params method
tokenizer.save_params(Path(path_to_tokenizer_config))

# Applies BPE to the previous tokens
tokenizer.apply_bpe_to_dataset(Path(path_to_tokens), Path(path_to_tokens_bpe))

==============================================

# load tokenizer
PREFIX = "/data/scratch/efthygeo/midi/giant"
saved_tokenizer_path = f'{PREFIX}/GiantMIDI-PIano_BPE_tokenizer.json'
tokenizer = REMI(params=Path(saved_tokenizer_path))

encoder midi max length: 512

'''

'''
gpt2 tokenization

max length = 

import tiktoken

enc = tiktoken.get_encoding("gpt2")
# pad, sos, eos --> 
# "<|endoftext|>"

'''