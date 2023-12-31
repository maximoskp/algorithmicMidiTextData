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
    # replace sharp
    message = message.replace('#', ' sharp')
    # explanations
    mode_explainer = {
        'major': [
            'Since it is in a major scale it has major third, major sixth and major seventh.',
            'The difference of its scale in comparison to a natural minor, is that it has major third, sixth and seventh.',
            'The fact that it is in the major scale makes this ' + phrase_segment + ' have a happy feeling, mainly expressed through the presence of the major third.'
        ],
        'natural_minor': [
            'Since it is in a natural minor scale it has minor third, minor sixth and minor seventh.',
            'The difference of its scale in comparison to major, is that it has minor third, sixth and seventh.',
            'The fact that it is in the natural minor scale makes this ' + phrase_segment + ' have a sad feeling, mainly expressed through the presence of the minor third and sixth.'
        ],
        'harmonic_minor': [
            'Since it is in a harmonic minor scale it has minor third, minor sixth but a major seventh.',
            'The difference of its scale in comparison to major, is that it has minor third and sixth while it retains the major seventh.',
            'The fact that it is in the harmonic minor scale makes this ' + phrase_segment + ' have a sad feeling, mainly expressed through the presence of the minor third and sixth, with strong resolution to the tonic, as an effect of the major seventh.'
        ],
        'dorian': [
            'Since it is in a dorian scale it has minor third and minor seventh but a major sixth.',
            'The difference of its scale in comparison to major, is that it has minor third and seventh while it retains the major seventh.',
            'The fact that it is in the dorian scale makes this ' + phrase_segment + ' have a mildly sad feeling, as it has a minor third, but the major sixth has a happinnes element.'
        ]
    }
    d3 = np.random.randint(3)
    message += ' ' + mode_explainer[mode][d3]
    return message
# end construct_message