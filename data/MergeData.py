# Helper script to combine all the data into a result csv

def merge_data(data1, data2, data_result):
    total = ""

    with open(data1, "r") as file:
        for line in file:
            total += line

    with open(data2, "r") as file:
        for line in file:
            total += line

    write_data(total, data_result)

def write_data(data, file):
    with open(file, "w") as f:
        f.write(data)

if __name__ == "__main__":
    merge_data("../AnonVoiceLeadingChunked.csv", "../AllBluesVoiceLeadingChunked.csv", "../CombinedVoiceLeadingChunked.csv")