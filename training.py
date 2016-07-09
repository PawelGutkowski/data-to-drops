import csv
from collections import defaultdict


def train(brain):
    with open('training.csv', 'rb') as csvfile:
        sorted = defaultdict(list)
        multiple = defaultdict(list)

        reader = csv.reader(csvfile)
        for row in reader:
            if reader.line_num > 1 and row[1] != "" and row[2] != "":
                messages = row[1].lower()
                sorted[row[2]].append(messages)

        for key, value in sorted.items():
            if len(key.split(", ")) == 1:
                brain.link(key, value)
            else:
                multiple[key] = value

        brain.evaluate()