import argparse, pprint

WILDCARD = '@'
PATH_TO_DICT = 'dictionaries/sowpods.txt'

parser = argparse.ArgumentParser(description='Helping people cheat at scrabble.')
parser.add_argument('letters',
                    help='The tiles on your rack. Use \'{0}\' for a wildcard.'.format(WILDCARD))


parser.add_argument('--dict',default=PATH_TO_DICT)
arguments = parser.parse_args()
pprint.pprint(arguments.dict)
pprint.pprint(arguments.letters)
