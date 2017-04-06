# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 21:14:22 2017

@author: bushnelf
"""

import Card as C


class Decoy(C.Card):
    """
    Decoy:
    Gain 1VP per Technology symbol in play + RZs.
        If you have the single most cards in your discard pile, ignore
        oppenents' main effects this round.
    No Clash effect
    """

    def __init__(self):
        C.Card.__init__(self, "Decoy", 6)
        self.add_symbol(C.Card.Symbols[3])      # Technology
        self.add_symbol(C.Card.Symbols[0])      # Negation
        self._ignore_main_effect = False

    def main_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        maxdiscs = -1
        for pballi in range(len(game.playerboards)):
            # do not exclude this player's board
            pb = game.playerboards[pballi]
            # Check both inplay and recovery zone
            for card in pb.inplay:
                if C.Card.Symbols[3] in card.symbols:
                    mypb.victorypoints += 1
            for card in pb.recoveryzone:
                if C.Card.Symbols[3] in card.symbols:
                    mypb.victorypoints += 1
            if pbidx != pballi and maxdiscs < len(pb.discards):
                maxdiscs = len(pb.discards)
            self._ignore_main_effect = maxdiscs < len(mypb.discards)

    def defense(self, game, pbidx, effect=["main_effect"], thisorlast="this"):
        if thisorlast == "this":
            return(self._ignore_main_effect)
        else:
            return(False)

if __name__ == '__main__':
    d = Decoy()

