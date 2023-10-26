from geniartor_mod import piece, optimization, rendering, utils
import yaml
import os
import numpy as np
import pandas as pd
from copy import deepcopy

number_of_trials = 10

cwd = os.getcwd()
config_path = cwd + '/configs/two_parts_template.yml'

os.makedirs('data', exist_ok=True)
os.makedirs('data/midis', exist_ok=True)
os.makedirs('data/texts', exist_ok=True)

with open(config_path) as config_file:
    initial_settings = yaml.load(config_file, Loader=yaml.FullLoader)

for _ in range(number_of_trials):
    settings = deepcopy(initial_settings)
    # lenght in bars
    bars_number = {
        'small': 4,
        'medium': 8,
        'large': 16
    }
    bars_number_keys = list(bars_number.keys())
    bars_number_key = bars_number_keys[int(np.random.randint(len(bars_number_keys)))]
    settings['piece']['n_measures'] = bars_number[bars_number_key]

    # define tonality
    tonics = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    modes = ['major', 'natural_minor', 'harmonic_minor', 'dorian']
    tonic = tonics[int(np.random.randint(len(tonics)))]
    mode = modes[int(np.random.randint(len(modes)))]
    settings['piece']['tonic'] = tonic
    settings['piece']['scale_type'] = mode

    # define register
    registers = {
        'full': ['G2', 'G5'],
        'low': ['G2', 'D4'],
        'high': ['D4', 'G5'],
    }
    register_keys = list(registers.keys())
    register_key = register_keys[int(np.random.randint(len(register_keys)))]
    settings['piece']['lowest_note'] = registers[register_key][0]
    settings['piece']['highest_note'] = registers[register_key][1]

    # rhythm speed
    config_speed_keys = [0.125, 0.25, 0.5, 1]
    speeds = {
        'fast': [0.4, 0.4, 0.1, 0.1],
        'medium': [0.1, 0.4, 0.4, 0.1],
        'slow': [0.1, 0.1, 0.4, 0.4]
    }
    speed_keys = list(speeds.keys())
    speed_key = speed_keys[int(np.random.randint(len(speed_keys)))]
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
    # tmp_name = datetime.now().strftime("%Y%m%d-%H%M%S")
    tmp_name = utils.get_unique_name()

    results_dir = settings['rendering']['dir']
    settings['rendering']['midi_name'] = tmp_name + '.mid'
    if not os.path.isdir(results_dir):
        os.mkdir(results_dir)
    rendering.render(generated_piece, settings['rendering'])

    # save text
    text_output_path = 'data/texts/'
    text_filen_name = tmp_name + '.txt'
    text_file = open( text_output_path + text_filen_name , 'w')
    text_file.write( message )
    text_file.close()

    print(message)