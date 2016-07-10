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
    result = {}
    for token in input:
        if token in base.keys():
            token_weight = measure_weight(token)
            result[token] = (token_weight^2)*base[token]*(token_weight/len(input))/weight

    return result

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
        if input == "": return ""

        tokens = tokenize(input)
        results = []
        matches = {}

        # find all matches
        for token in tokens:
            for key, value in self.links.items():
                matches[key] = match_tokens(value.tokens, tokens)

        # find keys based on matches
        for i in range(len(self.links)):
            match = self.best_match(matches)
            if match is None:
                break
            elif i == 0 or match[1]*1.5 > results[i-1][1]:
                results.append(match)
                self.strip_matches(matches, match[0])
            else:
                break

        # create status string
        status = results[0][0]
        for result in results[1:]:
            status +=", "+result[0]

        return status

    def best_match(self, matches):
        results = {}
        for key, map in matches.items():
            results[key] = sum(map.values())

        if not results: return None
        else:
            result = sorted(results, key=results.get, reverse=True)[0]
            return (result, results[result])

    def evaluate(self):
        for list in self.links.values():
            for token, occurences in list.tokens.items():
                if(measure_weight(token) < 2 and occurences < 2 ):
                    del list.tokens[token]

    def strip_matches(self, matches, key):
        link = self.links[key]
        del matches[key]
        for tokens in matches.values():
            for token in link.tokens:
                if token in tokens:
                    tokens.pop(token)

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
