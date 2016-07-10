from __future__ import division
import csv
import sys

import pickle

print "Loading brain..."
with open('brain.dump', 'rb') as dump:
    brain = pickle.load(dump)

print "Classifing input from "+sys.argv[1]+" and writing to "+sys.argv[2]+"..."

with open(sys.argv[1], 'rb') as input, open(sys.argv[2], 'w+') as output:

    reader = csv.reader(input)
    writer = csv.writer(output)

    writer.writerow(("Row ID", "#status", "Status Category"))

    for row in reader:
        if reader.line_num > 1:
            category = brain.classify(row[1])
            writer.writerow((row[0], row[1], category))

print "Done!"
