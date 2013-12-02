# scrabble-cheater

Takes a string of letters and finds all the possible valid Scrabble words based
on the provided SOWPODS dictionary or one of the user's picking (needs to be a
document with one word per line). Wildcards are indicated with the '@' symbol.

## usage

python cheater.py [-h] [--dict DICT] [--num_results NUM_RESULTS] letters

positional arguments:
  letters               The tiles on your rack. Use '@' for a wildcard.

optional arguments:
  -h, --help            show this help message and exit
  --dict DICT
  --num_results NUM_RESULTS
                        The number of words to show


*Thanks to Denis Garcia at https://www.github.com/denisgarci*
