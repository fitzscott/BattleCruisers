import math as M
import CardSet as CS

cl = CS.CardSet(5)
for i in range(8):
    num_cards = i+1
    totcards = len(cl.cards)
    li = totcards - num_cards + i
    combos = M.factorial(li) / (M.factorial(num_cards) *
                                M.factorial(li - num_cards))
    print(str(num_cards) + " taken out of " + str(li) + " is " + str(combos))
