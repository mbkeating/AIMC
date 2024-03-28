# This code generates a one hot encoding for a large alphabet
# The alphabet is the same one that is formed from GenerateChords
# NOTE: this is not used in the Lstm model we are publishing because the alphabet is too large

from numpy import array
from GenerateChords import generate

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
positions = []

for chord in all_chords:
    generated_chords = generate(chord)
    positions += generated_chords

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

                        fingering_alph_index = alph_dictionary[chord_fingering]
                        y_pattern.append([1 if i == fingering_alph_index else 0 for i in range(len(alphabet))])
                X.append(X_pattern)
                y.append(y_pattern)

        return array(X), array(y)

if __name__ == "__main__":
    sample_data = [{"chords": ["Amin7"], "fingerings": ["5-x-5-5-5-x"]}]
    X, y = one_hot_encode(sample_data)
    print(X)
    print(y)
