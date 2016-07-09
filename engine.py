from __future__ import division
from collections import defaultdict

def tokenize(item):
    base = item.replace("-", "").replace("(", " ").replace(")", " ").replace("/", "").replace(".", " ").replace("|", " ").lower()
    base = base.split()
    tokens = []
    for i in range(len(base)):
        for j in range(7):
            if (i + j < len(base)):
                if j > 0:
                    composite_token = base[i]
                    for k in range(1, j + 1):
                        composite_token += "\s+" + base[i + k]
                    tokens.append(composite_token)
                else:
                    tokens.append(base[i])
            else:
                break

    return filter_tokens(tokens)


def filter_tokens(tokens):
    ignore = ["of", "in", "to", "a", "an", "and", "by", "on", "but", "not", "non", "are", "is"]
    result = []
    for token in tokens:
        if token not in ignore and len(token) > 1:
            result.append(token)
    return result

def match_tokens(base, input):
    weight = sum(base.values())
    result = 0
    for token in input:
        if token in base.keys():
            token_weight = measure_weight(token)
            result += (token_weight^2)*base[token]*(token_weight/len(input))

    div = (result/weight)
    return div

def measure_weight(token):
    return (token.count("\s+") + 1) * (token.count("not") + 1)

class brain:
    def __init__(self):
        self.links = {}

    def link(self, category, items):
        key = category.lower()
        if key in self.links:
            self.links[key].update(items)
        else:
            self.links[key] = item_list()
            self.links[key].update(items)

    def classify(self, input):
        # for key, value in self.links.items():
        #     if input in value.items:
        #         return key
        if input == "": return ""

        tokens = tokenize(input)
        matches = {}

        for key, value in self.links.items():
            matches[key] = match_tokens(value.tokens, tokens)

        keys = sorted(matches, key=matches.get, reverse=True)
        result = keys[0]

        for i in range(1, len(keys)):
            if matches[keys[0]] < matches[keys[i]]*1.5:
                result += ", "+keys[i]
            else: break

        return result

    def evaluate(self):
        for list in self.links.values():
            for token, occurences in list.tokens.items():
                if(measure_weight(token) < 2 and occurences < 2 ):
                    del list.tokens[token]



class item_list:
    def __init__(self):
        self.items = []
        self.tokens = defaultdict(float)

    def update(self, items):
        self.items.append(items)
        for item in items:
            splits = tokenize(item)
            for split in splits:
                self.tokens[split] += (measure_weight(split)/len(splits))
