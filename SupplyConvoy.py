# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 15:13:44 2017

@author: bushnelf
"""

import Card as C


class SupplyConvoy(C.Card):
    """
    SupplyConvoy:
    Gain VP = lost VP so far in round.
    If none, gain 3VP.
    Clash:
    No Weapons symbol in RZ, discard 1 card.
    """

    def __init__(self):
        C.Card.__init__(self, "Supply Convoy", 37)
        self.add_symbol(C.Card.Symbols[5])      # Space
        self.add_symbol(C.Card.Symbols[0])      # Negation

    def main_effect(self, game, pbidx):
        pb = game.playerboards[pbidx]
        if pb.vp_lost_this_round > 0:
            pb.victorypoints += pb.vp_lost_this_round
        else:
            pb.victorypoints += 3

    def clash_effect(self, game, pbidx):
        pb = game.playerboards[pbidx]
        if not pb.checkrecoveryforsymbol(C.Card.Symbols[4]):
            card = pb.player.choosecardtodiscard(game, pbidx, ["hand",
                                                               "recovery"])
            pb.discard(card, ["hand", "recovery"])
