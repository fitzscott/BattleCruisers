# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 19:48:05 2017

@author: bushnelf
"""

import Card as C


class AttackWing(C.Card):
    """
    AttackWing:
    Choose an opponent to discard 2 cards.
    Clash:  Discard 1 card + lose 1 VP.
    """

    def __init__(self):
        C.Card.__init__(self, "Attack Wing", 33)
        self.add_symbol(C.Card.Symbols[4])      # Weapons

    def main_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        tgtpbidx = mypb.player.chooseplayertodiscard(game, pbidx,
                                                     ["hand", "recovery"])
        if tgtpbidx is not None:
            pbo = game.playerboards[tgtpbidx]
            for disc in range(2):
                card = pbo.player.choosecardtodiscard(game, tgtpbidx,
                                                      ["hand", "recovery"])
                pbo.discard(card, ["hand", "recovery"])
        else:
            print("No target for " + self.title)

    def clash_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        card = mypb.player.choosecardtodiscard(game, pbidx,
                                               ["hand", "recovery"])
        mypb.discard(card, ["hand", "recovery"])
        mypb.victorypoints -= 1

if __name__ == '__main__':
    aw = AttackWing()
    print("Created " + aw.title + ", rank " + str(aw.rank))
