from datetime import datetime
from uuid import uuid4
import numpy as np

def get_unique_name():
    return datetime.now().strftime("%y%m%d%H%M%S%f") + str(uuid4()).replace('-', '')
# end get_unique_name

def construct_message(bars_number, bars_number_key, tonic, mode, register_key, speed_key):
    d1 = np.random.randint(3)
    phrase_segment = ['phrase', 'segment', 'excerpt', 'piece'][ np.random.randint(4) ]
    notes_pitches = ['notes', 'pitches'][np.random.randint(2)]
    speed_rhythm = ['speed', 'rhythm', 'pace'][np.random.randint(3)]
    if d1 == 0:
        message = 'A ' + bars_number_key + ' ' + phrase_segment + ' that is ' + str(bars_number[bars_number_key]) + \
        ' bars long, in the key of ' + tonic + ' ' + mode + ', within the ' + register_key + \
        ' range of ' + notes_pitches + ', with ' + speed_key + ' ' + speed_rhythm + '.'
    elif d1 == 1:
        message = 'A ' + tonic + ' ' + mode + ' ' + phrase_segment + ',' + ' with a ' + bars_number_key + ' length of ' + str(bars_number[bars_number_key]) + \
        ' bars,'  + ' in ' + register_key + \
        ' range of ' + notes_pitches + ', with ' + speed_key + ' ' + speed_rhythm + '.'
    elif d1 == 2:
        message = 'A ' + tonic + ' ' + mode  + ' ' + phrase_segment + ',' + ' with a ' + bars_number_key + ' length of ' + str(bars_number[bars_number_key]) + \
        ' bars,'  + ' with ' + speed_key + ' ' + speed_rhythm + ', in the ' + register_key + \
        ' range of ' + notes_pitches + '.'
    return message
# end construct_message