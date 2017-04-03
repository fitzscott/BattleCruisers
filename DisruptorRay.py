# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 19:14:04 2017

@author: bushnelf
"""

import Card as C


class DisruptorRay(C.Card):
    """
    Disruptor Ray -
    Gain 2VP
    Disable an opponent this round
    """

    def __init__(self):
        C.Card.__init__(self, "Disruptor Ray", 9)
        self.add_symbol(C.Card.Symbols[4])      # Weapons
        self.add_symbol(C.Card.Symbols[0])      # Negation

    def main_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        myboard.victorypoints += 2
        pl = myboard.player.chooseplayertodisable(game, pbidx)
        print("Chose player " + str(pl) + " (I am " + str(pbidx) + ")")
        if pl >= 0:
            # We are taking advantage of the end-of-round (endplay)
            # function in playerboard to clean up on the disabled counter.
            # A disabled player board may not be disabled the next
            # round, so there is a "cooling off" period.
            # In this case, 2 = this round & next for being immune to
            # being disabled.
            game.playerboards[pl].disabled = 2

    def clash_effect(self, game, pbidx):
        """
        Lose 1 VP
        """
        game.playerboards[pbidx].victorypoints -= 1

if __name__ == '__main__':
    dr = DisruptorRay()
    if "Weapons" in dr.symbols:
        print("Yup, the " + dr.title + " is a weapon.")
