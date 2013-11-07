'''A simple shitty little script to help you cheat at Scrabble'''

import argparse, string, os, csv 
from collections import Counter

# CONSTANTS 
WILDCARD = '@'
PATH_TO_DICT = 'dictionaries/sowpods.txt'
VALID_CHARS = string.uppercase + WILDCARD
MAX_NUM_CHARS = 9

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
    
except InvalidInputException as e:    
    raise e 

# DERIVE ALL POSSIBLE CHARACTER SETS AND SCORING PROCEDURES
num_letters = len(args.letters)
num_wildcards = args.letters.count(WILDCARD)
tame_rack = args.letters.replace(WILDCARD,'')
rack_counter = Counter(tame_rack)

# FUNCTIONS
def get_lazy_list_from_csv(filename):
    with open(filename,mode='r') as f:
        reader = csv.reader(f)
        for line in reader:
            yield line[0]

def filter_for_length(word_gen):
    for word in word_gen:
        if len(word) <= num_letters:
            yield word

def original_match_test(word):
    wcs_necessary = 0
    available_chars = tame_rack 
    for c in word:
        if c not in available_chars:
            wcs_necessary += 1
            if wcs_necessary > num_wildcards:
                return False
        else:
            available_chars = available_chars.replace(c,'',1)
    return True

def original_score_word(word):
    available_chars = tame_rack 
    summation = 0
    for c in word:
        if c in available_chars:
            summation += SCORES[c]
            available_chars = available_chars.replace(c,'',1)
    return summation

# actual process
def gen_matching_words(): 
    for word in filter_for_length(get_lazy_list_from_csv(args.dict)):
        if original_match_test(word):
            yield (original_score_word(word),word)

sorted_word_scores = sorted(gen_matching_words(),
                            reverse=True)

limited = sorted_word_scores[:args.num_results]

print 'Showing {0} of {1} results...'.format(len(limited),len(sorted_word_scores))

for i,(score,word) in enumerate(limited):
    print '{0}. "{1}" = {2} points'.format(i+1,word,score)

