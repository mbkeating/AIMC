# This was the original alphabet one hot encoding generation
# The alphabet here only included the bass note of the chord
# Was used as a proof of concept for the model
# NOTE: that this is not used in our current model

from numpy import array

note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
chord_types = [
        'min',
        'min7',
        'min6',
        '6',
        'maj6',
        '7',
        '9',
        '',
        'min7f5',
        '7f9',
        '7f5',
        'aug',
        'dim7',
        'maj7']

all_chords = [n + t for n in note_names for t in chord_types]

# Lets say there's 18 viable frets + open position
positions = [str(i) + '-x-x' for i in range(19)] + ['x-' + str(i) + '-x' for i in range(19)] + ['x-x-' + str(i) for i in range(19)]

num_chords = len(positions)

alphabet = [''] + all_chords + positions

def pad_data(data):
        max_len = 0
        for d in data:
                if len(d['chords']) > max_len:
                        max_len = len(d['chords'])

        for d in data:
                while len(d['chords']) < max_len:
                        d['chords'].append('')
                        d['fingerings'].append('')

        return max_len
        

def one_hot_encode(data):
        alph_dictionary = dict()
        for i in range(len(alphabet)):
                alph_dictionary[alphabet[i]] = i

        X = []
        y = []
        for d in data:
                X_pattern = []
                y_pattern = []
                for i in range(len(d['chords'])):
                        chord_name = d['chords'][i]
                        chord_fingering = d['fingerings'][i]
                        
                        name_alph_index = alph_dictionary[chord_name]
                        X_pattern.append([1 if i == name_alph_index else 0 for i in range(len(alphabet))])

                        # For right now, chop the chord fingering to the first two chords
                        notes_in_fingering = chord_fingering.split('-')
                        truncated_chord = ''
                        added_note = False
                        for n in range(3):
                                if not added_note:
                                        truncated_chord += notes_in_fingering[n]
                                else:
                                        truncated_chord += 'x'

                                if notes_in_fingering[n] != 'x':
                                        added_note = True

                                if n < 2:
                                        truncated_chord += '-'
                                
                        # truncated_chord = '-'.join(chord_fingering.split('-')[0:2])
                        fingering_alph_index = alph_dictionary[truncated_chord]
                        y_pattern.append([1 if i == fingering_alph_index else 0 for i in range(len(alphabet))])
                X.append(X_pattern)
                y.append(y_pattern)

        return array(X), array(y)