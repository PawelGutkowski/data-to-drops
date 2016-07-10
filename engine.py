from __future__ import division
from collections import defaultdict

MULTI_STATUS_FACTOR = 250

def tokenize(text):
    """
    returns list of tokens created from passed text. Tokens consist of single and multiple words
    Tokens are lowercase and filtered, some non-alphanumeric chars are replaced
    '\s+' marker is placed instead of whitespaces in multi-word tokens
    :param text: string to be tokenized
    :return:
    """
    base = text.replace("-", "").replace("(", " ").replace(")", " ").replace("/", "").replace(".", " ").replace("|", " ")
    base = base.lower().split()
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
    """
    filters passed list of string, removing words which don't have semantic weight
    :param tokens: list of tokens to be filtered
    :return:
    """
    ignore = ["of", "in", "to", "an", "and", "by", "on", "but", "not", "non", "are", "is"]
    result = []
    for token in tokens:
        if token not in ignore and len(token) > 1:
            result.append(token)
    return result


def match_tokens(base, input):
    """
    returns dictionary:
    keys - tokens from input which match given base
    values - token weight
    :param base: dictionary of tokens and their weights, default taken from link of brain
    :param input: list of tokens to be matches
    :return:
    """

    weight = sum(base.values())
    result = {}
    for token in input:
        if token in base.keys():
            token_weight = measure_weight(token)
            result[token] = (token_weight ^ 2) * base[token] * (token_weight / len(input)) / weight

    return result


def measure_weight(token):
    """
    returns numeric value of token weight
    :param token:
    :return:
    """
    return (token.count("\s+") + 1) * (token.count("not") + 1)


def best_match(matches):
    results = {}
    for key, map in matches.items():
        results[key] = sum(map.values())

    if not results:
        return None
    else:
        result = sorted(results, key=results.get, reverse=True)[0]
        return result, results[result]


class brain:
    def __init__(self):
        self.links = {}

    def train(self, status, items):
        """
        updates category in brain with given items
        :param status: water source status
        :param items: messages to link with status in brain
        """
        key = status.lower()
        if key not in self.links:
            self.links[key] = link()

        if len(status.split(", ")) < 2:
            self.links[key].update(items)
        else:
            self.links[key].items.extend(items)

    def classify(self, input):
        """
        returns status based on input and previous training
        :param input: string, message to be analyzed
        :return:
        """
        if input == "": return ""
        input = input.lower()
        for key, value in self.links.items():
            if input in value.items:
                return key

        tokens = tokenize(input)
        # tuples: (status, sumaric weight)
        results = []
        # key: status, value: list of dicts(token, weight)
        matches = {}

        # find matches in learned links
        for token in tokens:
            for key, value in self.links.items():
                matches[key] = match_tokens(value.tokens, tokens)

        # find status keys based on matches
        for i in range(len(self.links)):
            match = best_match(matches)
            if match is None:
                break
            elif i == 0 or match[1] * MULTI_STATUS_FACTOR > results[i - 1][1]:
                results.append(match)
                self.strip_matches(matches, match[0])
            else:
                break

        # create status string
        status = results[0][0]
        for result in results[1:]:
            status += ", " + result[0]

        return status

    def strip_matches(self, matches, key):
        """
        deletes key from matches and all tokens matching given key in brain
        :param matches:
        :param key:
        """
        link = self.links[key]
        del matches[key]
        for tokens in matches.values():
            for token in link.tokens:
                if token in tokens:
                    tokens.pop(token)

    def evaluate(self):
        """
        delete tokens of low value
        """
        for list in self.links.values():
            for token, occurences in list.tokens.items():
                if (measure_weight(token) < 2 and occurences < 2):
                    del list.tokens[token]


class link:
    def __init__(self):
        self.items = []
        self.tokens = defaultdict(float)

    def update(self, items):
        self.items.extend(items)
        for item in items:
            tokens = tokenize(item)
            for token in tokens:
                self.tokens[token] += (measure_weight(token) / len(tokens))
