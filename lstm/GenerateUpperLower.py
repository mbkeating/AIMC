# This file gets the upper and lower bounds on the model evaluation
# Upper bounds are defined if:
#   the sorted output (predictions) of the model from high -> low 
#   contains all valid chords before some cutoff (iterator) up to the size of the model output
# Lower bounds are defined if:
#   the rank of the true prediction in the model is at least the cutoff

import sys
sys.path.insert(1, '../data/')
from CheckData import get_notes_in_chord, position_to_note

class GenerateUpperLower:
    def __init__(self, alphabet, num_chords, data):
        self.alphabet = alphabet
        self.num_chords = num_chords
        self.data = data
        self.pred = []
        self.true = []

    # Called where model predict is called in LstmModel.py
    def append(self, y_pred, y_true):
        self.pred.append([y_pred[0][0][len(y_pred[0][0]) - self.num_chords:], y_pred[0][1][len(y_pred[0][1]) - self.num_chords:], y_pred[0][2][len(y_pred[0][2]) - self.num_chords:]])
        self.true.append([y_true[0][0][len(y_true[0][0]) - self.num_chords:], y_true[0][1][len(y_true[0][1]) - self.num_chords:], y_true[0][2][len(y_true[0][2]) - self.num_chords:]])

    # Get the upper and lower bounds and print them in Latex format
    def upper_lower(self):

        alph_rel = self.alphabet[len(self.alphabet) - self.num_chords:]

        # preprocess dictionary to keep track of rank
        rank_memoize = [[0 for _ in prediction] for prediction in self.pred]

        # Calculate rank for each point
        for i in range(len(self.pred)):
            for j in range(len(self.pred[i])):
                true_index = -1
                for t in range(len(self.true[i][j])):
                    if self.true[i][j][t] == 1.0:
                        true_index = t

                true_predicted_prob = self.pred[i][j][true_index]
                rank = 0
                for p in range(len(self.pred[i][j])):
                    if self.pred[i][j][p] >= true_predicted_prob:
                        rank += 1
                rank_memoize[i][j] = rank

        lower = []
        for i in range(len(alph_rel)):
            sum_i = 0
            for j in range(len(rank_memoize)):
                rank_j = max(rank_memoize[j])
                if rank_j <= i + 1:
                    sum_i += 1
            lower.append(sum_i)

        # preprocess predictions to keep track of when the first valid chord fingering appears
        valid_memoize = [[0 for _ in prediction] for prediction in self.pred]

        # need to zip up probabilities for each chord (self.pred[current prediction][i]) with the alphabet and 
        # then sort 
        # then check those against data[current prediction]["chords"][i]
        
        for i in range(len(self.pred)):
            for j in range(len(self.pred[i])):
                current_prediction = self.pred[i][j]
                current_chord = self.data[i]["chords"][j]

                # zip up cur_pred with alphabet
                zip = [(current_prediction[w], alph_rel[w]) for w in range(len(current_prediction))]
                # sort for high proba -> low proba
                zip.sort(key=lambda x:x[0], reverse=True)
                sorted_proba_fingerings = [z[1] for z in zip]

                # now check if they're the chord
                for pf in range(len(sorted_proba_fingerings)):
                    valid_notes = get_notes_in_chord(current_chord)
                    fingering = sorted_proba_fingerings[pf].split("-")
                    bad_chord = False
                    for w in range(len(fingering)):
                        if fingering[w] == "x":
                            continue
                        data_note = position_to_note(int(fingering[w]), w)
                        if data_note == -1 or data_note not in valid_notes:
                            bad_chord = True

                    if not bad_chord:
                        valid_memoize[i][j] = pf + 1
                        break

        upper = []
        for i in range(len(alph_rel)):
            sum_i = 0
            for j in range(len(valid_memoize)):
                valid_j = max(valid_memoize[j])
                if valid_j <= i + 1:
                    sum_i += 1
            upper.append(sum_i)

        # Print out all the points in Latex syntax to include in paper
        l_string = ""
        u_string = ""
        for i in range(len(alph_rel)):
            l_string += ("(" + str(i + 1) + "," + str(lower[i]) + ")")
            u_string += ("(" + str(i + 1) + "," + str(upper[i]) + ")")

        print(l_string)
        print(u_string)