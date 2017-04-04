# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 21:14:22 2017

@author: bushnelf
"""

import Card as C


class Navigator(C.Card):
    """
    Navigator:
    Gain 2 VP
    Choose main effect to ignore this round.
    No Clash effect
    """

    def __init__(self):
        C.Card.__init__(self, "Navigator", 5)
        self.add_symbol(C.Card.Symbols[2])      # People
        self.add_symbol(C.Card.Symbols[0])      # Negation
        self._effect_to_ignore = -1

    def main_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        mypb.victorypoints += 2
        # Check other boards for their main effects
        self._effect_to_ignore = mypb.player.chooseeffecttoignore(game,
                                                                  pbidx, self)
        print("Navigator has set ignore to " + str(self._effect_to_ignore))

    def defense(self, game, pbidx, effect=["main_effect"], thisorlast="this"):
        if thisorlast == "this":
            activecard = game.cardbeingplayed
            if activecard is not None:
                activerank = activecard.rank
            print("Navigator comparing its ignore rank " +
                  str(self._effect_to_ignore))
            print("    against active card's rank " + str(activerank))
            return(activerank == self._effect_to_ignore)
        else:
            return(False)

if __name__ == '__main__':
    n = Navigator()
