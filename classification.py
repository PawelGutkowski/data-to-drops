from __future__ import division
import csv
import sys

import training
from engine import brain

brain = brain()
training.train(brain)

print "Classifing input from "+sys.argv[1]+" ..."

with open(sys.argv[1], 'rb') as csvfile:

    reader = csv.reader(csvfile)
    rows = 0
    matched = 0
    for row in reader:
        if reader.line_num > 1 and row[2] != "":
            status = brain.classify(row[1])
            if(status.lower() == row[2].lower()):
                matched+=1
            elif(len(row[2].split(", "))==1):
                print row[0] + " : " + status + " should be " + row[2] + ": "+row[1]+"\n"
            rows+=1
    print "result: "+str(matched)+"/"+str(rows)+" = "+str(matched/rows)

print brain.classify("Water point dry/ drawdown|Water Point Pump Problem|")
