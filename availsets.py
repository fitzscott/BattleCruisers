# -*- coding: utf-8 -*-

# import os
import sys

cards = {}
cardfile = open(sys.argv[1], "r")
availcards = [1, 3, 9, 11, 13, 17, 19, 20, 22, 29, 31, 39, 43]

for line in cardfile:
    line.strip()
    nums = line.split()
    matches = 0
    for num in nums:
        if int(num) in availcards:
            matches += 1
    if matches >= 6:
        print("Set [" + line + "] can be played up to " + str(matches-3) +
              " players.")
