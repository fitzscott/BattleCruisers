# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 15:38:36 2017

@author: bushnelf
"""

import Card as C


class Electropulse(C.Card):
    """
    Electropulse - like Disruptor Ray, but one turn deferred.
    Gain 2 VP.
    Pick target to be disabled next round.  No disabling that
    target again the following round.
    Clash - playing board disabled instead.
    """

    def __init__(self):
        C.Card.__init__(self, "Electropulse", 40)
        self.add_symbol(C.Card.Symbols[4])      # Weapons
        self.add_symbol(C.Card.Symbols[0])      # Negation

    def main_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        mypb.victorypoints += 2
        plidx = mypb.player.chooseplayertodisable(game, pbidx)
        print("Chose player " + str(plidx) + " (I am " + str(pbidx) + ")")
        if plidx >= 0:
            # This effect will apply next turn, so the disable count
            # must be at 2 then, so it needs to be 3 now.
            game.playerboards[plidx].disabled = 3

    def clash_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        mypb.disabled = 3

if __name__ == '__main__':
    e = Electropulse()
    print("Created " + e.title + ", rank " + str(e.rank))
