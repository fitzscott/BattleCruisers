# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 19:53:32 2017

@author: bushnelf
"""

import Card as C


class ArmorPlating(C.Card):
    """
    Armor Plating -
    Gain 3 VP
    Redirect card discard attacks to reduce VP instead.
    Clash - lose 1 VP
    """

    def __init__(self):
        C.Card.__init__(self, "Armor Plating", 20)
        self.add_symbol(C.Card.Symbols[3])      # Technology
        self.add_symbol(C.Card.Symbols[0])      # Negation

    def main_effect(self, game, pbidx):
        game.playerboards[pbidx].victorypoints += 3

    def clash_effect(self, game, pbidx):
        game.playerboards[pbidx].victorypoints -= 1

    def redirect(self, pb, effect, thisorlast="this"):
        ret = False
        if "discard" == effect:
            pb.victorypoints -= 1
            ret = True
        return(ret)

if __name__ == '__main__':
    ap = ArmorPlating()
    print("Created " + ap.title + ", rank " + str(ap.rank))
