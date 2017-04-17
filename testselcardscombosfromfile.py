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
if len(sys.argv) < 7:
    print("Usage: " + sys.argv[0] +
          " combo_file num_cards iterations splits split2run " +
          "cardrank1 [cardrank2 ...]")
    sys.exit(-1)

combo_file_name = sys.argv[1]
num_cards = int(sys.argv[2])
num_players = num_cards - 3
num_iters = int(sys.argv[3])
num_splits = int(sys.argv[4])
split_to_run = int(sys.argv[5])
cardrank = [int(n) for n in sys.argv[6:]]
sys.stderr.write("Want to match ranks: " + str(cardrank) + "\n")

num_possible_cards = len(CS.CardSet.cards)
# print("Total card count is " + str(num_possible_cards))
# combos = (M.factorial(num_possible_cards) / (M.factorial(num_cards) *
#           M.factorial(num_possible_cards - num_cards)))
# sys.stderr.write("Number of combos: " + str(combos) + "\n")
selcardcount = len(cardrank)
numremaining = num_possible_cards - selcardcount
remainingtochoose = num_cards - selcardcount
combos = (M.factorial(numremaining) / (M.factorial(remainingtochoose) *
          M.factorial(numremaining - remainingtochoose)))
sys.stderr.write("Number of combos for selected: " + str(combos) + "\n")

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

cs = CS.CardSet(num_players)
clidxs = [n for n in cs.cards.keys()]
cardlist = [clidxs.index(cr) for cr in cardrank]
sys.stderr.write("   So match indices: " + str(cardlist) + "\n")

combo_file = open(combo_file_name, "r")
# arrarr = []
recnum = 1
found = 0
played = 0
for line in combo_file:
    cardidxs = line.strip().split()
    idxs = [int(n) for n in cardidxs]
    allfound = True
    for selc in cardlist:        # these are indices, not card ranks
        if selc not in idxs:
            allfound = False
            break
    if allfound:
        found += 1
        if found >= startsplit and found < startsplit + splitsize:
            sys.stderr.write("    Match: " + str(idxs) + "\n")
            for j in range(num_iters):
                playcardlist(idxs)
            played += 1
    if recnum % 100000 == 0:
        sys.stderr.write("Checked against " + str(recnum) + " entries.\n")
    recnum += 1
combo_file.close()

sys.stderr.write("Played " + str(played) + " of " + str(found) +
                 " card sets.\n")
sys.stderr.write("Total records checked: " + str(recnum - 1) + "\n")
