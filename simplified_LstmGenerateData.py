# This is the actual one hot encoding generation that we used
# This code has the alphabet that is documented in the paper which comes from seen chords in the data set.

from numpy import array
from GenerateChords import generate
import sys
sys.path.insert(1, '../data/')
from ParseData import get_data_from_file

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

# We need to import the data here, I tried doing it more efficiently but I want the code to work and it doesn't really matter for the scale I'm working at right now
data = get_data_from_file('../CombinedVoiceLeadingChunked.csv')

p_set = set()
for d in data:
    for f in d['fingerings']:
        p_set.add(f)

positions = list(p_set)

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
    

# One hot encode into two arrays: X and y where X contains sequences of len(sequence in data) 
# where each is an array of len(alphabet) with a singular 1 to mark the location of this data in the alphabet and 0 everywhere else
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

            fingering_alph_index = alph_dictionary[chord_fingering]
            y_pattern.append([1 if i == fingering_alph_index else 0 for i in range(len(alphabet))])
        X.append(X_pattern)
        y.append(y_pattern)

    return array(X), array(y)
