## make dir
import os
import numpy as np

converter_script = 'mscore'

import subprocess

os.makedirs('data/midis_wavs', exist_ok=True)
os.makedirs('data/midis_wavs/test', exist_ok=True)
for file in os.listdir('data/midis'):
    if 'mid' in file:
        midi = 'data/midis/' + file
        wav = 'data/midis_wavs/test/' + file.replace('mid', 'flac')
        print(f'{converter_script} "{midi}" -o "{wav}"')
        subprocess.Popen(f'export QT_QPA_PLATFORM=offscreen; {converter_script} "{midi}" -o "{wav}"', shell=True).wait()