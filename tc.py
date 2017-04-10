# -*- coding: utf-8 -*-

import sys

#   main   #
# expected parameters: # cards, # splits, which split to test
if len(sys.argv) < 4:
    print("Usage: " + sys.argv[0] +
          " #_cards #_splits split_to_run [iterations]")
    sys.exit(-1)

num_cards = int(sys.argv[1])
num_players = num_cards - 3
num_splits = int(sys.argv[2])
split_to_run = int(sys.argv[3])
if len(sys.argv) > 4:
    num_iters = int(sys.argv[4])
else:
    num_iters = 100

combos = 7888725
# We will likely get fractional splits, so allow some overlap.
splitsize = int(combos / num_splits + num_splits / 2)
# splitsize = int(combos / num_splits) + 2
startsplit = int((split_to_run - 1) * float(combos / num_splits))
print("Starting at combination " + str(startsplit))
print("    Running for " + str(splitsize) + " entries (till " +
      str(startsplit + splitsize) + ").")
if startsplit + splitsize > combos:
    startsplit = combos - splitsize
    print("Revised starting at combination " + str(startsplit))
    print("    Running for " + str(splitsize) + " entries (till " +
          str(startsplit + splitsize) + ").")
