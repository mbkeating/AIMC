# Check all inputted csv data for valid chord size, characters, and notes

from ParseData import get_data_from_file

notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


# Make sure that a fingering has 6 characters separated by 5 -
def check_chord_size(data):
    for d in data:
        for chord in d["fingerings"]:
            spl = chord.split('-')
            if len(spl) != 6:
                print(chord)
                return False
    return True


# Make sure that all parts of the fingering are either x, -, or a number
def check_valid_characters(data):
    valid_chars = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', 'x'}
    for d in data:
        for f in d["fingerings"]:
            for c in f:
                if c not in valid_chars:
                    print(f)
                    return False
    return True


# Get index of note in notes
def note_index(note):
    # get index
    index = -1
    for i in range(len(notes)):
        if notes[i] == note:
            index = i
    return index


# Get valid notes in a chord
def get_notes_in_chord(chord):
    chords = {
        "min": [3, 4],
        "min7": [3, 4, 3],
        "min6": [3, 4, 2],
        "6": [4, 3, 2],
        "maj6": [4, 3, 2],
        "7": [4, 3, 3],
        "9": [4, 3, 3, 4],
        "": [4, 3],
        "7f9": [4, 3, 3, 3],
        "7f5": [4, 2, 4],
        "min7f5": [3, 3, 4],
        "aug": [4, 4],
        "dim7": [3, 3, 3],
        "maj7": [4, 3, 4]
    }

    if "#" in chord:
        note = chord[0:2]
        chord_type = chord[2:]
    else:
        note = chord[0]
        chord_type = chord[1:]

    index = note_index(note)
    if index == -1:
        return []
    if chord_type not in chords:
        return []

    chord_notes = [notes[index]]
    for interval in chords[chord_type]:
        chord_notes.append(notes[(index + interval) % 12])
        index += interval

    return chord_notes


# Convert position on fretboard to note
def position_to_note(fret, string):
    strings = ["E", "A", "D", "G", "B", "E"]
    starting_note = strings[string]
    index = note_index(starting_note)
    if index == -1:
        return -1
    return notes[(index + fret) % 12]


# Make sure that these chords have the correct notes
def check_valid_chords(data):
    for d in data:
        for i in range(len(d["fingerings"])):
            chord = d["fingerings"][i]
            chord_name = d["chords"][i]

            valid_notes = get_notes_in_chord(chord_name)
            fingering = chord.split("-")
            for i in range(len(fingering)):
                if fingering[i] == "x":
                    continue
                data_note = position_to_note(int(fingering[i]), i)
                if data_note == -1 or data_note not in valid_notes:
                    print(valid_notes)
                    print(data_note)
                    print(chord_name)
                    print(chord)
                    return False
    return True


def run_test_suite(data):
    if check_chord_size(data):
        print("Checking chord fingering size: Passed")
    else:
        print("Checking chord fingering size: Failed")

    if check_valid_characters(data):
        print("Checking for valid characters: Passed")
    else:
        print("Checking for valid characters: Failed")

    if check_valid_chords(data):
        print("Checking for valid chords: Passed")
    else:
        print("Checking for valid chords: Failed")


if __name__ == "__main__":
    # Change this file to the one you want to run test suite on
    d = get_data_from_file("../AnonVoiceLeading.csv")
    run_test_suite(d)