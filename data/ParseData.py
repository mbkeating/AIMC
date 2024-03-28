# Get the data from a csv file with every three rows in the format:
# Song Name
# Chord1, Chord2, ...
# Fingering1, Fingering2, ...

# Get those into an array of dictionaries indexed by the row type (name, chords, fingerings)

def get_data_from_file(f):
    data = []
    with open(f, "r") as file:
        # iterate in threes
        iter = 0
        cur_data = dict()
        for line in file:
            if iter == 0:
                # song name
                cur_data["name"] = line.split(',')[0]
            elif iter == 1:
                # song chords
                cur_data["chords"] = [c.strip() for c in line.split(',') if len(c.strip()) > 0]
            else:
                # if we set it to -1 now the += 1 will set it to 0
                iter = -1
                # chord fingerings
                cur_data["fingerings"] = [fin.strip() for fin in line.split(',') if len(fin.strip()) > 0]
                data.append(cur_data)
                cur_data = dict()

            iter += 1

    return data

def print_data(data):
    for song in data:
        print(song["name"])
        print(song["chords"])
        print(song["fingerings"])

# This file is usually called by other files so this main is here for testing
if __name__ == "__main__":
    # File to load into data
    d = get_data_from_file("../AllBluesVoiceLeading.csv")
    print_data(d)