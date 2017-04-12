# -*- coding: utf-8 -*-

# Produce a list of all combinations of N cards.  Print out.

import sys

import CardSet as CS


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


#   main   #
# expected parameters: # cards
if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " #_cards")
    sys.exit(-1)

num_cards = int(sys.argv[1])
num_players = num_cards - 3

num_possible_cards = len(CS.CardSet.cards)
indexes = [n for n in range(num_possible_cards)]


arrarr = []
for i in indexes:
    arrarr.append([i])

for x in range(num_cards-1):
    arrarr = exparr(arrarr)

for arr in arrarr:
    if len(arr) == num_cards:
        arr2 = [str(n) for n in arr]
        print((" ".join(arr2)))
        # print(arr)
# print("Length of combo arr: " + str(len(arrarr2)))

