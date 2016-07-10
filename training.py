import csv
import sys
from collections import defaultdict

import pickle

from engine import brain

brain  = brain()
training_file = 'training.csv'
if(len(sys.argv) > 1):
    training_file = sys.argv[1]

with open(training_file, 'rb') as csvfile:
    sorted = defaultdict(list)
    multiple = defaultdict(list)

    reader = csv.reader(csvfile)
    for row in reader:
        if reader.line_num > 1 and row[1] != "" and row[2] != "":
            messages = row[1].lower()
            sorted[row[2]].append(messages)

    # learn based only on input with single status
    for key, value in sorted.items():
            brain.train(key, value)

with open('brain.dump', 'w+') as dump:
    pickle.dump(brain, dump)