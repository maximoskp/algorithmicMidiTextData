import mido
import random
import os

import mido
import random

def generate_random_pitch_variation(input_file, output_file, pitch_range=(-12, 12), change_percentage=0.5):
    # Load MIDI file
    mid = mido.MidiFile(input_file)

    # Dictionary to keep track of note states (on/off) for each note
    note_states = {}

    # Create a new MIDI file to write the modified data
    output_mid = mido.MidiFile()
    for i, track in enumerate(mid.tracks):
        output_track = mido.MidiTrack()
        output_mid.tracks.append(output_track)

        for msg in track:
            # Check if the message is a note on or note off message
            if msg.type == 'note_on':
                note = msg.note
                velocity = msg.velocity
                # Determine whether to change the pitch of this note
                if random.random() < change_percentage:
                    # Randomly adjust the pitch within the specified range
                    new_pitch = min(max(note + random.randint(*pitch_range), 0), 127)
                    # Create a new message with the adjusted pitch
                    new_msg = mido.Message('note_on', note=new_pitch, velocity=velocity)
                    output_track.append(new_msg)
                    # Update note state
                    note_states.setdefault(note, []).append(new_pitch)
                else:
                    # If not changing pitch, just copy the original message
                    output_track.append(msg)
            elif msg.type == 'note_off':
                note = msg.note
                # Check if note state exists for this note
                if note in note_states and len(note_states[note]) > 0:
                    # Pop the last pitch adjustment for this note
                    new_pitch = note_states[note].pop()
                    # Create a new message with the adjusted pitch
                    new_msg = mido.Message('note_off', note=new_pitch)
                    output_track.append(new_msg)
                else:
                    # If note state doesn't exist, just copy the message
                    output_track.append(msg)
            else:
                # For other messages, just copy them to the new track
                output_track.append(msg)

    # Save the modified MIDI file
    output_mid.save(output_file)
# end generate_random_pitch_variation

# Example usage
# input_file = "input.mid"
# output_file = "output.mid"
# generate_random_pitch_variation(input_file, output_file, change_percentage=0.3)  # Change 30% of the notes

# 10% variation
os.makedirs('data/midis10pc', exist_ok=True)
# 20% variation
os.makedirs('data/midis20pc', exist_ok=True)
i = 0
total = len(os.listdir('data/midis'))
for midi_file in os.listdir('data/midis'):
    print(str(i) + '/' + str(total), end='\r')
    i += 1
    generate_random_pitch_variation('data/midis/' + midi_file, 'data/midis10pc/' + midi_file, change_percentage=0.1)
    generate_random_pitch_variation('data/midis/' + midi_file, 'data/midis20pc/' + midi_file, change_percentage=0.2)