'''A simple shitty little script to help you cheat at Scrabble'''

import argparse, string, os, csv, itertools, time

# CONSTANTS 
WILDCARD = '@'
PATH_TO_DICT = 'dictionaries/sowpods.txt'
VALID_CHARS = string.uppercase + WILDCARD
MAX_NUM_CHARS = 7

SCORES = {"A": 1, "C": 3, "B": 3, "E": 1, "D": 2, "G": 2,
         "F": 4, "I": 1, "H": 4, "K": 5, "J": 8, "M": 3,
         "L": 1, "O": 1, "N": 1, "Q": 10, "P": 3, "S": 1,
         "R": 1, "U": 1, "T": 1, "W": 4, "V": 4, "Y": 4,
         "X": 8, "Z": 10}

# EXCEPTIONS
class InvalidInputException(Exception):
    pass


#INPUT PROCESSING 
try:
    parser = argparse.ArgumentParser(
        description='Helping people cheat at scrabble.')

    parser.add_argument(
        'letters',help='The tiles on your rack. Use \'{0}\' for a wildcard.'.format(
                                                 WILDCARD))
    parser.add_argument('--dict',default=PATH_TO_DICT)

    parser.add_argument('--num_results',help='The number of words to show',
            type=int,default=100)

    args = parser.parse_args()
    args.letters = args.letters.upper()

    invalid_chars = {c for c in args.letters if c not in VALID_CHARS}
    if invalid_chars:
        raise InvalidInputException(
            'The following are invalid characters for this cheater: {0}'.format(
                ' '.join(invalid_chars)))
    
    if len(args.letters) > MAX_NUM_CHARS:
        raise InvalidInputException(
            'Too many letters were provided. The max is {0}'.format(MAX_NUM_CHARS))

    if not os.path.exists(args.dict):
        raise InvalidInputException(
            'Cannot find the dictionary located at {0}'.format(args.dict))
    
except InvalidInputException:    
    print InvalidInputException.message
    pass

# FUNCTIONS
def get_lazy_list_from_csv(filename):
    with open(filename,mode='r') as f:
        reader = csv.reader(f)
        for line in reader:
            word = line[0] 
            yield word

def filter_for_length(word_gen):
    for word in word_gen:
        if len(word) <= MAX_NUM_CHARS:
            yield word

def match_test(word,tame_rack,num_wildcards):
    available_chars = tame_rack
    counter = 0
    for c in word:
        if c not in available_chars:
            counter += 1
            if counter > num_wildcards:
                return False
        else:
            available_chars = available_chars.replace(c,'',1)
    return True

def score_word(word,tame_rack):
    summation = 0
    for c in word: 
        if c in tame_rack:
            summation += SCORES[c]
            tame_rack.replace(c,'',1)
    return summation

# DERIVE ALL POSSIBLE CHARACTER SETS AND SCORING PROCEDURES
num_wildcards = args.letters.count(WILDCARD)
tame_rack = args.letters.replace(WILDCARD,'')

words_scores = []

for word in filter_for_length(get_lazy_list_from_csv(args.dict)):
    if match_test(word,tame_rack,num_wildcards):
        words_scores.append((word,score_word(word,tame_rack)))

sorted_word_scores = sorted(words_scores,key=lambda x:x[1],reverse=True)[:args.num_results]

for i, (word, score) in enumerate(sorted_word_scores):
    print '{0}. "{1}" = {2} points'.format(i+1,word,score)

