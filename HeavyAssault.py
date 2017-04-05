# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 18:04:58 2017

@author: bushnelf
"""

import Card as C


class HeavyAssault(C.Card):
    """
    Heavy Assault:
    Take 3VP from each opponent.  Heavy.
    Clash:  Discard two cards.  Heavy.
    """
    def __init__(self):
        C.Card.__init__(self, "Heavy Assault", 24)
        self.add_symbol(C.Card.Symbols[4])          # Weapons

    def main_effect(self, game, pbidx):
        """ This is partly taken from player board.  Maybe refactor. """
        mypb = game.playerboards[pbidx]
        for pboi in range(len(game.playerboards)):
            if pboi != pbidx:
                tgtpb = game.playerboards[pboi]
                if tgtpb.protected == 0 and not \
                        tgtpb.ignore_main_effect(game, pbidx, ["vp_theft"]):
                    availvp = tgtpb.victorypoints
                    if availvp > 3:
                        availvp = 3
                    tgtpb.victorypoints -= availvp
                    mypb.victorypoints += availvp

    def clash_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        for dsc in range(2):
            card = mypb.player.choosecardtodiscard(game, pbidx,
                                                   ["hand", "recovery"])
            mypb.discard(card, ["hand", "recovery"])

if __name__ == '__main__':
    ha = HeavyAssault()
    print("Created " + ha.title)
