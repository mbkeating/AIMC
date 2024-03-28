# Code to generate a version of the data with sliding window slicing
# [A, B, C, D, E] cut into slices of 3 would be
# [A, B, C], [B, C, D], [C, D, E]

from ParseData import get_data_from_file

# Make a new data point to avoid overwriting array contents
def new_data_point(name, fingerings, chords, chunk_size):
    data_point = dict()
    data_point["fingerings"] = [f for f in fingerings]
    data_point["chords"] = [c for c in chords]
    data_point["name"] = [name] + ['' for _ in range(chunk_size - 1)]
    return data_point

# Cut the data into chunks of size chunk_size and return the new data
def chunk(data, chunk_size):
    new_data = []
    for d in data:
        cur_fingerings_chunk = [d["fingerings"][i] for i in range(chunk_size)]
        cur_chords_chunk = [d["chords"][i] for i in range(chunk_size)]

        new_data.append(new_data_point(d["name"] + '_slice', cur_fingerings_chunk, cur_chords_chunk, chunk_size))

        for right_pointer in range(chunk_size, len(d["fingerings"])):
            cur_fingerings_chunk.pop(0)
            cur_chords_chunk.pop(0)

            cur_fingerings_chunk.append(d["fingerings"][right_pointer])
            cur_chords_chunk.append(d["chords"][right_pointer])

            new_data.append(new_data_point(d["name"] + '_slice', cur_fingerings_chunk, cur_chords_chunk, chunk_size))
    
    return new_data

# copied from explode data
def write_data(data, file):
    with open(file, "w") as f:
        for d in data:
            f.write(','.join(d["name"]) + '\n')
            f.write(','.join(d["chords"]) + '\n')
            f.write(','.join(d["fingerings"]) + '\n')

if __name__ == "__main__":
    # File you want to chunk
    d = get_data_from_file("../AnonVoiceLeadingExploded.csv")
    d = chunk(d, 3)
    # Output file with chunks
    write_data(d, '../AnonVoiceLeadingChunked.csv')