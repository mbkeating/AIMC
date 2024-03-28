# This file can generate all possible "playable" chords for a finger span
# NOTE: this is not used in the LSTM model that we are publishing. 
#   It is here for potential future work on a different alphabet of fingerings

import sys
sys.path.insert(1, '../data/')
from CheckData import get_notes_in_chord

span = 4

guitar_notes = [[0 for i in range(22)] for j in range(6)]

def fill_guitar():
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    open_notes = [7, 0, 5, 10, 2, 7]
    for i in range(6):
        cur_note = open_notes[i]
        guitar_notes[i][0] = notes[cur_note]
        for j in range(1, len(guitar_notes[i])):
            cur_note = (cur_note + 1) % 12
            guitar_notes[i][j] = notes[cur_note]


# For now leave out duplicate notes
def generate_chords(chord_notes, chords, current_chord):
    min_fret_in_cur_chord = 22
    max_fret_in_cur_chord = -1
    current_string = 0

    if len(current_chord) > 0:
        # Iterate through the chord and get max fret, min fret, and also see if the chord notes are all satisfied
        current_chord_notes = current_chord.split('-')
        current_string = len(current_chord_notes)
        
        checking_cur_chord_notes = set()
        for i in range(len(current_chord_notes)):
            c = current_chord_notes[i]
            if c == 'x':
                continue
            c = int(c)
            if c < min_fret_in_cur_chord:
                min_fret_in_cur_chord = c
            if c > max_fret_in_cur_chord:
                max_fret_in_cur_chord = c
            c_note = guitar_notes[i][c]
            if c_note in chord_notes:
                checking_cur_chord_notes.add(c)

        # Are we done?
        if len(checking_cur_chord_notes) == len(chord_notes):
            # Make sure it's the right length
            current_chord_notes = current_chord_notes + ['x' for _ in range(6 - len(current_chord_notes))]
            chords.append('-'.join(current_chord_notes))
            return
        elif len(current_chord_notes) == 6:
            return

    if min_fret_in_cur_chord == 22 and max_fret_in_cur_chord == -1:
        min_fret_in_cur_chord = 0
        max_fret_in_cur_chord = 21
    else:
        temp_min = max(min(max_fret_in_cur_chord - span, min_fret_in_cur_chord), 0)
        max_fret_in_cur_chord = min(max(min_fret_in_cur_chord + span, max_fret_in_cur_chord), 21)
        min_fret_in_cur_chord = temp_min

    for nex in range(min_fret_in_cur_chord, max_fret_in_cur_chord + 1):
        next_note = guitar_notes[current_string][nex]
        if next_note in chord_notes:
            # Add it in
            current_chord_copy = current_chord
            if len(current_chord) == 0:
                current_chord_copy = str(nex)
            else:
                current_chord_copy += ('-' + str(nex))
            next_chord_notes = [c for c in chord_notes if c != next_note]
            generate_chords(next_chord_notes, chords, current_chord_copy)

    if len(current_chord) == 0:
        generate_chords(chord_notes, chords, current_chord + 'x')
    elif current_chord[len(current_chord) - 1] != 'x' or len(current_chord) == 1:
        generate_chords(chord_notes, chords, current_chord + '-x')

def generate(chord_name):
    chords = []
    fill_guitar()
    chord_notes = get_notes_in_chord(chord_name)

    # Time to hard code some stuff
    # First, if it's a five note chord, take out the 5th
    if len(chord_notes) == 5:
        chord_notes = chord_notes[0:2] + chord_notes[3:]

    # Second, if it's a four note chord that doesn't modify the fifth then take out the fifth for no5 voicings (not the only thing)
    if len(chord_notes) == 4 and 'f5' not in chord_name and 'dim' not in chord_name:
        no5_chord_notes = chord_notes[0:2] + [chord_notes[3]]
        # We will still call the normal generate chords IN ADDITION to this
        generate_chords(no5_chord_notes, chords, '')

    # Third, if it's a four note minor sixth chord then remove the root (this is extrememly hacky)
    if len(chord_notes) == 4 and 'min6' in chord_name:
        no_root_chord_notes = chord_notes[1:]
        generate_chords(no_root_chord_notes, chords, '')

    generate_chords(chord_notes, chords, '')
    return chords

if __name__ == "__main__":
    chords = generate("Amin6")

    print(chords)