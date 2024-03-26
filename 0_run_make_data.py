from geniartor_mod import piece, optimization, rendering, utils
import yaml
import os
import numpy as np
import pandas as pd
from copy import deepcopy
from tqdm import tqdm
import pickle

cwd = os.getcwd()
config_path = cwd + '/configs/two_parts_template.yml'

os.makedirs('data', exist_ok=True)
os.makedirs('data/midis', exist_ok=True)
os.makedirs('data/texts', exist_ok=True)

with open(config_path) as config_file:
    initial_settings = yaml.load(config_file, Loader=yaml.FullLoader)

# lenght in bars
bars_number = {
    'small': 4,
    'medium': 8,
    'large': 16
}
# define tonality
tonics = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
modes = ['major', 'natural_minor', 'harmonic_minor', 'dorian']
# define register
registers = {
    'full': ['G2', 'G5'],
    'low': ['G2', 'D4'],
    'high': ['D4', 'G5'],
}
# rhythm speed
config_speed_keys = [0.125, 0.25, 0.5, 1]
speeds = {
    'fast': [0.4, 0.4, 0.1, 0.1],
    'medium': [0.1, 0.4, 0.4, 0.1],
    'slow': [0.1, 0.1, 0.4, 0.4]
}

# for downstream classification tasks
name = []
bars_number_key_idxs = []
tonic_idxs = []
mode_idxs = []
register_key_idxs = []
speed_idxs = []
# downstream info
downstream_info = {
    'bars_number_key_idxs': bars_number,
    'tonic_idxs': tonics,
    'mode_idxs': modes,
    'register_key_idxs': registers,
    'speed_idxs': speeds
}

bars_keys = list(bars_number.keys())
bars_keys_number = len(bars_keys)
tonics_number = len(tonics)
modes_number = len(modes)
register_keys = list(registers.keys())
register_keys_number = len(register_keys)
speed_keys = list(speeds.keys())
speed_keys_number = len(speed_keys)
reps = 10
current_rep = 0

number_of_trials = bars_keys_number*tonics_number*modes_number*register_keys_number*speed_keys_number*reps
for bars_idx in range(bars_keys_number):
    for tonic_idx in range(tonics_number):
        for mode_idx in range(modes_number):
            for register_idx in range(register_keys_number):
                for speed_idx in range(speed_keys_number):
                    for rep in range(reps):
                        current_rep += 1
                        print('current_rep = ' + str(current_rep) + '/' + str(number_of_trials), end='\r')
                        settings = deepcopy(initial_settings)
                        # bars
                        bars_number_key = bars_keys[bars_idx]
                        settings['piece']['n_measures'] = bars_number[bars_number_key]
                        # tonic and mode
                        tonic = tonics[tonic_idx]
                        mode = modes[mode_idx]
                        settings['piece']['tonic'] = tonic
                        settings['piece']['scale_type'] = mode
                        # register
                        register_key = register_keys[register_idx]
                        settings['piece']['lowest_note'] = registers[register_key][0]
                        settings['piece']['highest_note'] = registers[register_key][1]
                        # speed
                        speed_key = speed_keys[speed_idx]
                        for i, k in enumerate(config_speed_keys):
                            settings['piece']['duration_weights'][k] = speeds[speed_key][i]
                        message = utils.construct_message(bars_number, bars_number_key, tonic, mode, register_key, speed_key)
                        generated_piece = piece.generate_random_piece(**settings['piece'])
                        n_passes = settings['optimization']['n_passes']
                        settings['optimization']['n_passes'] = n_passes
                        generated_piece = optimization.run_variable_neighborhood_search(
                            generated_piece, settings['evaluation'], **settings['optimization']
                        )
                        # make name code
                        tmp_name = 'b' + str(bars_idx) + '_t' + str(tonic_idx) + '_m' + \
                            str(mode_idx) + '_r' + str(register_idx) + '_s' + \
                                str(speed_idx) + '_r' + str(rep)
                        name.append(tmp_name)

                        results_dir = settings['rendering']['dir']
                        settings['rendering']['midi_name'] = tmp_name + '.mid'
                        if not os.path.isdir(results_dir):
                            os.mkdir(results_dir)
                        rendering.render(generated_piece, settings['rendering'])

                        # save for downstream tasks
                        bars_number_key_idxs.append( bars_idx )
                        tonic_idxs.append( tonic_idx )
                        mode_idxs.append( mode_idx )
                        register_key_idxs.append( register_idx )
                        speed_idxs.append( speed_idx )

                        # save text
                        text_output_path = 'data/texts/'
                        text_filen_name = tmp_name + '.txt'
                        text_file = open( text_output_path + text_filen_name , 'w')
                        text_file.write( message )
                        text_file.close()
# end fors
                        
# save dataframe for downstream tasks
d = {
    'name': name,
    'bars_number_key_idxs': bars_number_key_idxs,
    'tonic_idxs': tonic_idxs,
    'mode_idxs': mode_idxs,
    'register_key_idxs': register_key_idxs,
    'speed_idxs': speed_idxs
}

downstram_df = pd.DataFrame.from_dict(d)
downstram_df.to_csv('data/' + 'downdstream_df.csv')

with open('downstream_info.pickle', 'wb') as handle:
    pickle.dump(downstream_info, handle, protocol=pickle.HIGHEST_PROTOCOL)