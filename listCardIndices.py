# -*- coding: utf-8 -*-

import sys
import random

import CardSet as CS

num_players = 5
cs = CS.CardSet(num_players)
i = 0
for crank in cs.cards:
    c = cs.cards[crank]()
    print(str(i) + ": " + str(c))
    i += 1

