
# This is our actual model. 
# Based off the sequence-to-sequence example in Long Short Term Memory Networks in Python
import random
import sys
sys.path.insert(1, '../data/')

from simplified_LstmGenerateData import pad_data, one_hot_encode, alphabet, num_chords
from ParseData import get_data_from_file
from GenerateUpperLower import GenerateUpperLower

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import TimeDistributed
from keras.layers import RepeatVector
import tensorflow as tf
from tensorflow_ranking.python.keras import metrics

from numpy import argmax
import numpy as np

def get_index_of_one(l):
    for i in range(len(l)):
        if l[i] == 1:
            return i


def get_fingering_from_prediction(pred):
    total = []
    for prediction in pred[0]:
        most_likely = argmax(prediction[len(prediction) - num_chords:])
        # Get it back into scale with the alphabet
        most_likely = len(alphabet) - num_chords + most_likely
        total.append(alphabet[most_likely])
   
    return total
    

# Calculate the mean reciprocal rank (mrr) for the given set of predictions and their true value
def mrr(y_true, y_pred):
    
    total = 0.0
    n = 0.0

    # Convert both to lists for easier iteration
    true_list = y_true.numpy().tolist()
    pred_list = y_pred.numpy().tolist()

    for sequence in range(len(true_list)):
        n += len(true_list[sequence])
        # Loop over all points in sequence
        for i in range(len(true_list[sequence])):
            true_point = true_list[sequence][i]
            pred_point = pred_list[sequence][i]
            # slice to only consider the fingerings
            true_point = true_point[len(true_point) - num_chords:]
            pred_point = pred_point[len(pred_point) - num_chords:]

            # get the index of the prediction
            true_index = -1
            for j in range(len(true_point)):
                if true_point[j] == 1.0:
                    true_index = j
            
            true_predicted_value = pred_point[true_index]
            rank = 1
            for j in range(len(pred_point)):
                if j == true_index:
                    continue
                if pred_point[j] > true_predicted_value:
                    rank += 1
            
            total += (1.0 / rank)
    mean_recip_rank = total / n
    return mean_recip_rank


data = get_data_from_file('../CombinedVoiceLeadingChunked.csv')

length_of_sequence = pad_data(data)

random.shuffle(data)
training = data[0:len(data) - 100]
testing = data[len(data) - 100:]
X, y = one_hot_encode(training)

# Model from Long-Short Term Memory Networks in Python book
model = Sequential()
model.add(LSTM(100, return_sequences=True, input_shape=(length_of_sequence, len(alphabet))))
model.add(LSTM(50))
model.add(RepeatVector(length_of_sequence))
model.add(LSTM(50, return_sequences=True))
model.add(LSTM(100, return_sequences=True))
model.add(TimeDistributed(Dense(len(alphabet), activation='softmax')))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=[mrr], run_eagerly=True)
print(model.summary())

model.fit(X, y, epochs=10, batch_size=5)

X, y = one_hot_encode(testing)

loss, acc = model.evaluate(X, y, verbose=0)
print( 'Loss: %f, Accuracy: %f'  % (loss, acc*100))

# Get the upper and lower bounds of "goodness"
ulGen = GenerateUpperLower(alphabet, num_chords, testing)

for i in range(len(testing)):
    X, y = one_hot_encode(testing[i:i + 1])
    yhat = model.predict(X, verbose=0)
    ulGen.append(yhat, y)

# Calculate the upper and lower bounds and print them
ulGen.upper_lower()