# -*- coding: utf-8 -*-

# Produce a list of all combinations of N cards.  Split the list into
# M parts, then run the Pth part.

import math as M
import sys

import CardSet as CS
import SmarterGame as SG
import SimpleHumanPlayer as SHP
import RandomComputerPlayer as RCP


# Take an array of arrays. For each sub-array, if it has length = num_cards,
# return it as-is. If it is shorter, replace it with set of arrays with
# itself plus each of the indexes greater than its highest.
def exparr(arrarr):
    newarrarr = []
    for arr in arrarr:
        if len(arr) == num_cards:
            newarrarr.append(arr)
        else:
            lastentry = arr[len(arr)-1]
            # this is inefficient. fix later, maybe.
            for idx in range(len(indexes)):
                if indexes[idx] > lastentry:
                    newarr = [n for n in arr]
                    newarr.append(indexes[idx])
                    newarrarr.append(newarr)
    return(newarrarr)


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

num_possible_cards = len(CS.CardSet.cards)
indexes = [n for n in range(num_possible_cards)]
# indexes = [n for n in range(12)]


arrarr = []
for i in indexes:
    arrarr.append([i])

for x in range(num_cards-1):
    arrarr = exparr(arrarr)
# for arr in arrarr2:
#     if len(arr) == num_cards:
#         print(arr)
sys.stderr.write("Length of combo arr: " + str(len(arrarr)) + "\n")
li = len(indexes)
combos = M.factorial(li) / (M.factorial(num_cards) *
                            M.factorial(li - num_cards))
sys.stderr.write("Number of combos: " + str(combos) + "\n")

# cs = CS.CardSet(num_players)
# for z in range(10):
#     testset = cs.getcardsetbyindices(arrarr[z])
#     print("\nTest set " + str(z) + ": ", )
#     for c in testset:
#         print(c,)
#     print("")

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

for i in range(startsplit, startsplit + splitsize):
    compl = i - startsplit
    if compl % 100 == 0:
        sys.stderr.write("Completed " + str(compl) +
                         ", next combo " + str(startsplit + i) + "\n")
    for j in range(num_iters):
        playcardlist(arrarr[i])

sys.stderr.write("Completed split.\n\n")
