## make dir
import os
import numpy as np

converter_script = 'mscore'

import subprocess

os.makedirs('data/midis20pc_wavs', exist_ok=True)
os.makedirs('data/midis20pc_wavs/test', exist_ok=True)
for file in os.listdir('data/midis20pc'):
    if 'mid' in file:
        midi = 'data/midis20pc/' + file
        wav = 'data/midis20pc_wavs/test/' + file.replace('mid', 'flac')
        print(f'{converter_script} "{midi}" -o "{wav}"')
        subprocess.Popen(f'export QT_QPA_PLATFORM=offscreen; {converter_script} "{midi}" -o "{wav}"', shell=True).wait()