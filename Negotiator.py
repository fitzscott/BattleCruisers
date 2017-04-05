# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 17:41:18 2017

@author: bushnelf
"""

import Card as C


class Negotiator(C.Card):
    """
    Negotiator:
    Least VP -> gain 4VP
    if Space symbol in RZ + not least VP -> gain 3VP
    No clash
    """
    def __init__(self):
        C.Card.__init__(self, "Negotiator", 12)
        self.add_symbol(C.Card.Symbols[2])       # People

    def main_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        myvp = mypb.victorypoints

        leastvp = True
        for pboi in range(len(game.playerboards)):
            if pboi != pbidx:
                if game.playerboards[pboi].victorypoints < myvp:
                    leastvp = False
                    break
        if leastvp:
            mypb.victorypoints += 4
        elif mypb.checkrecoveryforsymbol(C.Card.Symbols[5]):
            mypb.victorypoints += 3

if __name__ == '__main__':
    n = Negotiator()
    print("Created " + n.title)
