# -*- coding: utf-8 -*-

# import os
import sys

cards = {}
cardfile = open(sys.argv[1], "r")
if len(sys.argv) > 2:
    maxchk = int(sys.argv[2])
else:
    maxchk = 100

for line in cardfile:
    line.strip()
    nums = line.split()
    cnt = 1
    for num in nums:
        if cnt > maxchk:
            break
        if num in cards:
            cards[num] += 1
        else:
            cards[num] = 1
        cnt += 1

# print(cards)
for cardnum in cards:
    print(str(cards[cardnum]) + " occurrences for card #: " + str(cardnum))
