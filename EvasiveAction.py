# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 21:14:22 2017

@author: bushnelf
"""

import Card as C


class EvasiveAction(C.Card):
    """
    EvasiveAction:
    Do not lose cards to forced discards to main effects this round and next.
    If there is a Space symbol in your RZ, gain 2 VP.
    No Clash effect
    """

    def __init__(self):
        C.Card.__init__(self, "EvasiveAction", 8)
        self.add_symbol(C.Card.Symbols[5])      # Space
        self.add_symbol(C.Card.Symbols[0])      # Negation

    def main_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        for card in mypb.recoveryzone:
            # Space symbol in RZ = 2VP
            if C.Card.Symbols[5] in card.symbols:
                mypb.victorypoints += 2
                break        # but only once
            
    def defense(self, game, pbidx, effect=["main_effect"], thisorlast="this"):
        """ prevents discards for this round and next round """
        return("card_discard" in effect)

if __name__ == '__main__':
    d = EvasiveAction()

