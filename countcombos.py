import math as M

for i in range(8):
    num_cards = i+1
    li = 24+i
    combos = M.factorial(li) / (M.factorial(num_cards) *
                    M.factorial(li - num_cards))
    print(str(num_cards) + " taken from " + str(li) + " is " + str(combos))

