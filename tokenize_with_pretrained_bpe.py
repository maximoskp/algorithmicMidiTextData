from miditok import REMI, TokenizerConfig
from miditoolkit import MidiFile
from pathlib import Path

# Our tokenizer's configuration
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
tokenizer = REMI(config)

### full dataset
# this folder should contain the entire dataset
# prefix = "/data/scratch/efthygeo/midi/giant/small"
# prefix = "/data/scratch/efthygeo/midi/max/midis"
# prefix = "/data/scratch/efthygeo/midi/midi_bach/midis"
# prefix = "/data/scratch/efthygeo/midi/max_new/clean/midis"
prefix = "data/midis"
path_to_dataset = prefix
path_to_tokens = f'{prefix}_noBPE/'
path_to_tokens_bpe = f'{prefix}_BPE/'
path_to_tokenizer_config = f'{prefix}_BPE_tokenizer.json'


def midi_valid(midi):
    # print(f"{midi}")
    # if any(ts.numerator != 4 for ts in midi.time_signature_changes):
    #     return False  # time signature different from 4/*, 4 beats per bar
    if midi.max_tick < 10 * midi.ticks_per_beat:
        return False  # this MIDI is too short
    return True

# [2, 1, 1] gives roughly 5.5x
# data_augmentation_offsets = [2, 1, 1]  # data augmentation on 2 pitch octaves, 1 velocity and 1 duration values
midi_paths = list(Path(path_to_dataset).glob("**/*.mid"))
print(f"Found {len(midi_paths)} midi files")

sorted_paths = sorted(midi_paths) # for debugging
# debug_midi = sorted_paths[:400]
tokenizer.tokenize_midi_dataset(
    # midi_paths=debug_midi,
    midi_paths=sorted_paths,
    out_dir=Path(path_to_tokens),
    validation_fn=midi_valid,
    # data_augment_offsets=data_augmentation_offsets,
)

# # Load pretrained tokenizer
# path_to_bpe = \
#     "data/GiantMIDI-PIano_BPE_tokenizer.json"
# bpe_tokenizer = REMI(params=path_to_bpe)
# # import pdb; pdb.set_trace()
# # Applies BPE to the previous tokens
# bpe_tokenizer.apply_bpe_to_dataset(Path(path_to_tokens), Path(path_to_tokens_bpe))