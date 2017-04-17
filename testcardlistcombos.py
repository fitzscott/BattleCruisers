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
# expected parameters: combo file, # cards [iterations]
if len(sys.argv) < 5:
    print("Usage: " + sys.argv[0] +
          " combo_file num_cards iterations cardidx1 [cardidx2 ...]")
    sys.exit(-1)

combo_file_name = sys.argv[1]
num_cards = int(sys.argv[2])
num_players = num_cards - 3
num_iters = int(sys.argv[3])
cardlist = [int(n) for n in sys.argv[4:]]
sys.stderr.write("Want to match indices: " + str(cardlist) + "\n")

num_possible_cards = len(CS.CardSet.cards)
indexes = [n for n in range(num_possible_cards)]
li = len(indexes)
combos = M.factorial(li) / (M.factorial(num_cards) *
                            M.factorial(li - num_cards))

combo_file = open(combo_file_name, "r")
# arrarr = []
recnum = 1
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
            sys.stderr.write("    Match: " + str(idxs) + "\n")
            for j in range(num_iters):
                playcardlist(idxs)
            played += 1
    if recnum % 100000 == 0:
        sys.stderr.write("Checked against " + str(recnum) + " entries.\n")
    recnum += 1
combo_file.close()

sys.stderr.write("Played " + str(played) + " card sets.\n")
sys.stderr.write("Total records processed: " + str(recnum - 1) + "\n")
li = len(indexes)
combos = M.factorial(li) / (M.factorial(num_cards) *
                            M.factorial(li - num_cards))
sys.stderr.write("Number of combos: " + str(combos) + "\n")
