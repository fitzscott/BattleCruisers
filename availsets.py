# -*- coding: utf-8 -*-

# import os
import sys

cards = {}
cardfile = open(sys.argv[1], "r")
# availcards = [1, 3, 9, 11, 13, 17, 19, 20, 22, 29, 31, 39, 43]
# availcards = [1, 3, 5, 9, 11, 13, 17, 19, 20, 22, 23, 29, 30, 31, 33, 38, 39, 40, 43]
availcards = [1, 3, 4, 5, 6, 9, 11, 12, 13, 16, 17, 19, 20, 22, 23, 24, 29, 30, 31, 32, 33, 34, 37, 38, 39, 40, 43, 44, 45]

for line in cardfile:
    cs = line.strip().split("|")
    matches6 = matches7 = matches8 = 0
    setname = cs[0]
    for num in range(len(cs)-1):
        if int(cs[num+1]) in availcards:
            matches8 += 1
        if int(cs[num+1]) in availcards and num <= 6:
            matches7 += 1
        if int(cs[num+1]) in availcards and num <= 5:
            matches6 += 1
    if matches8 == 8:
        print("Set " + setname + " [" + str(cs[1:]) + "] can be played with " +
              "5 players.")
    if matches7 == 7:
        print("Set " + setname + " [" + str(cs[1:]) + "] can be played with " +
              "4 players.")
    if matches6 == 6:
        print("Set " + setname + " [" + str(cs[1:]) + "] can be played with " +
              "3 players.")

