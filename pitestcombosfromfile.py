# -*- coding: utf-8 -*-

# Read a list of all combinations of N cards.  Split the list into
# M parts, then run the Pth part.

import math as M
import sys
import os

import CardSet as CS


#   main   #
# expected parameters: combo file, # cards
if len(sys.argv) < 3:
    print("Usage: " + sys.argv[0] +
          " combo_file num_cards")
    sys.exit(-1)

combo_file_name = sys.argv[1]
num_cards = int(sys.argv[2])
num_players = num_cards - 3

num_possible_cards = len(CS.CardSet.cards)
indexes = [ n for n in range(num_possible_cards) ]
li = len(indexes)
combos = M.factorial(li) / (M.factorial(num_cards) *
                            M.factorial(li - num_cards))

combo_file = open(combo_file_name, "r")
recnum = 1
for line in combo_file:
    pi = recnum % 4 + 1
    cmd = "ssh pi@pi" + str(pi) + " python_games/BattleCruisers/tCI.sh " + \
          str(num_players) + " 0 " + line.strip()
    # print(cmd)
    os.system(cmd)
    if recnum % 100 == 0:
        print("Ran " + str(recnum) + "th card set")
    recnum += 1

print("Completed all card sets")

