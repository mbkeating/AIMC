# Code to increase the amount of data
# Transpose into all viable keys that fit inside the fretboard frets 1-18

from ParseData import get_data_from_file

MIN_FRET = 1
MAX_FRET = 18

notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

# Get notes as a dictionary where key is the note and value is the index in the notes array
def turn_notes_to_dict():
    d = dict()
    for i in range(len(notes)):
        d[notes[i]] = i
    return d

# Copied from LstmGenerateData. Pads data with '' to make all sequences the same length
def pad_data(data):
    max_len = 0
    for d in data:
        if len(d['chords']) > max_len:
            max_len = len(d['chords'])

    for d in data:
        while len(d['chords']) < max_len:
            d['chords'].append('')
            d['fingerings'].append('')

        d["name"] = [d["name"]]
        while len(d["name"]) < max_len:
            d["name"].append('')

    return max_len

# Take the data and for each sequence transpose that sequence of fingerings and chord names into as many keys as possible
def explode(data):
    notes_dict = turn_notes_to_dict()

    new_data = []
    for d in data:
        # First add this data point to the new data
        new_data.append(d)

        # Get the first fret of the first chord to get a baseline
        first_fingering = d["fingerings"][0]
        spl = first_fingering.split('-')
        ff = spl[0]
        i = 1
        while ff == 'x':
            ff = spl[i]
            i += 1
        ff = int(ff)

        starting_offset = MIN_FRET- ff
        ending_offset = MAX_FRET - ff

        for offset in range(starting_offset, ending_offset):
            new_data_point = dict()
            new_data_point["name"] = d["name"] + "_copy"

            new_chords = []
            new_fingerings = []

            for i in range(len(d["chords"])):
                # Get the new chord name
                is_sharp = len(d["chords"][i]) > 1 and d["chords"][i][1] == '#'
                chord_letter = d["chords"][i][0] if not is_sharp else d["chords"][i][0:2]
                new_chord_letter = notes[(notes_dict[chord_letter] + offset) % len(notes)]
                new_chord_symbol = new_chord_letter + (d["chords"][i][1:] if not is_sharp else d["chords"][i][2:])
                
                # Get the new chord fingering
                fingers = d["fingerings"][i].split('-')
                overflow = False
                for fin in range(len(fingers)):
                    finger = fingers[fin]
                    if finger == 'x':
                        continue
                    new_finger = int(finger) + offset
                    if new_finger > MAX_FRET or new_finger < MIN_FRET:
                        overflow = True
                        break
                    fingers[fin] = str(new_finger)

                if overflow:
                    break

                new_chords.append(new_chord_symbol)
                new_fingerings.append('-'.join(fingers))
                
            # Need to make sure that the list got fully populated - only then should we add this new data point
            if len(new_chords) == len(d["chords"]):
                new_data_point["chords"] = new_chords
                new_data_point["fingerings"] = new_fingerings
                new_data.append(new_data_point)

    return new_data

# Write the data to a file in the same format as the input data
def write_data(data, file):
    with open(file, "w") as f:
        for d in data:
            f.write(','.join(d["name"]) + '\n')
            f.write(','.join(d["chords"]) + '\n')
            f.write(','.join(d["fingerings"]) + '\n')

if __name__ == "__main__":
    # Data to explode
    d = get_data_from_file("../AnonVoiceLeading.csv")
    d = explode(d)
    pad_data(d)

    # Result file
    write_data(d, "../AnonVoiceLeadingExploded.csv")
