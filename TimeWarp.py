# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 22:40:15 2017

@author: bushnelf
"""

import Card as C


class TimeWarp(C.Card):
    """
    Time Warp:
    Lose all VP.
    Return all discards from discard pile to hand, then discard
        this card (TimeWarp).
    Then sing, "Let's do the time warp again".
    No Clash (obviously - not their song at all)
    """
    def __init__(self):
        C.Card.__init__(self, "Time Warp", 45)
        self.add_symbol(C.Card.Symbols[5])      # Space

    def main_effect(self, game, pbidx):
        pb = game.playerboards[pbidx]
        pb.victorypoints = 0
        for card in pb.discards:
            pb.hand.append(card)
            pb.discards.remove(card)
        pb.discard(self, "inplay")
