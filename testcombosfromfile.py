# -*- coding: utf-8 -*-

# Read a list of all combinations of N cards.  Split the list into
# M parts, then run the Pth part.

import math as M
import sys

import CardSet as CS
import SmarterGame as SG
# import SimpleHumanPlayer as SHP
import RandomComputerPlayer as RCP


def playcardlist(cards):
    print("Playing with " + str(num_players) + " players.")
    sg = SG.SmarterGame(num_players)
    for dp in range(num_players):
        rcp = RCP.RandomComputerPlayer("Random Player " + str(dp+1))
        sg.playerboards[dp].player = rcp
    cs = CS.CardSet(num_players)
    sg.cardlist = cs.getcardsetbyindices(cards)
    sg.sendcardlisttoboards()
    for dnr in range(num_players):
        pb = sg.playerboards[dnr]
        print(pb)
        c = pb.player.choosecardtodiscard(sg, dnr, ["hand"])
        pb.discard(c, ["hand"])
        print(pb)
        c = pb.player.choosecardtosendtorecovery(sg, dnr)
        pb.sendtorecovery(c)
    sg.playrounds(100)


#   main   #
# expected parameters: combo file, # cards, # splits, which split to test
if len(sys.argv) < 4:
    print("Usage: " + sys.argv[0] +
          " combo_file #_cards #_splits split_to_run [iterations]")
    sys.exit(-1)

combo_file_name = sys.argv[1]
num_cards = int(sys.argv[2])
num_players = num_cards - 3
num_splits = int(sys.argv[3])
split_to_run = int(sys.argv[4])
if len(sys.argv) > 5:
    num_iters = int(sys.argv[5])
else:
    num_iters = 100

num_possible_cards = len(CS.CardSet.cards)
indexes = [n for n in range(num_possible_cards)]
li = len(indexes)
combos = M.factorial(li) / (M.factorial(num_cards) *
                            M.factorial(li - num_cards))

# We will likely get fractional splits, so allow some overlap.
splitsize = int(combos / num_splits + num_splits / 2)
startsplit = int((split_to_run - 1) * float(combos / num_splits))
sys.stderr.write("Starting at combination " + str(startsplit) + "\n")
sys.stderr.write("    Running for " + str(splitsize) + " entries (till " +
                 str(startsplit + splitsize) + ").\n")
# print("Halfway is " + str(int(combos / 2)))
if startsplit + splitsize > combos:
    startsplit = combos - splitsize
    sys.stderr.write("Revised starting at combination " +
                     str(startsplit) + "\n")
    sys.stderr.write("    Running for " + str(splitsize) + " entries (till " +
                     str(startsplit + splitsize) + ").\n")

combo_file = open(combo_file_name, "r")

# arrarr = []
recnum = 0
for line in combo_file:
    cardidxs = line.strip().split()
    recnum += 1
    if recnum >= startsplit and recnum < startsplit + splitsize:
        idxs = [int(n) for n in cardidxs]
        for j in range(num_iters):
            playcardlist(idxs)
        if recnum % 100 == 0:
            sys.stderr.write("Completed " + str(recnum) + "\n")
    elif recnum >= startsplit + splitsize:
        break
combo_file.close()
sys.stderr.write("Length of combos: " + str(recnum) + "\n")
li = len(indexes)
combos = M.factorial(li) / (M.factorial(num_cards) *
                            M.factorial(li - num_cards))
sys.stderr.write("Number of combos: " + str(combos) + "\n")

sys.stderr.write("Completed split.\n\n")
