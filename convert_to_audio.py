## make dir
import os
import numpy as np

os.makedirs('midis/test', exist_ok=True)
converter_script = 'mscore'

import subprocess

os.makedirs('data/midis_wavs', exist_ok=True)
for file in os.listdir('data/midis'):
    if 'mid' in file:
        midi = 'data/midis/' + file
        wav = 'data/midis_wavs/' + file.replace('mid', 'flac')
        print(f'{converter_script} "{midi}" -o "{wav}"')
        subprocess.Popen(f'export QT_QPA_PLATFORM=offscreen; {converter_script} "{midi}" -o "{wav}"', shell=True).wait()

os.makedirs('data/midis10pc_wavs', exist_ok=True)
for file in os.listdir('data/midis10pc'):
    if 'mid' in file:
        midi = 'data/midis10pc/' + file
        wav = 'data/midis10pc_wavs/' + file.replace('mid', 'flac')
        print(f'{converter_script} "{midi}" -o "{wav}"')
        subprocess.Popen(f'export QT_QPA_PLATFORM=offscreen; {converter_script} "{midi}" -o "{wav}"', shell=True).wait()

os.makedirs('data/midis20pc_wavs', exist_ok=True)
for file in os.listdir('data/midis20pc'):
    if 'mid' in file:
        midi = 'data/midis20pc/' + file
        wav = 'data/midis20pc_wavs/' + file.replace('mid', 'flac')
        print(f'{converter_script} "{midi}" -o "{wav}"')
        subprocess.Popen(f'export QT_QPA_PLATFORM=offscreen; {converter_script} "{midi}" -o "{wav}"', shell=True).wait()