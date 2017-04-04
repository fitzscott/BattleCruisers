# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 20:00:30 2017

@author: bushnelf
"""

import Card as C


class ComputerVirus(C.Card):
    """
    Computer Virus:
    Gain 2 VP
    Cards in opponents' RZs w/ Technology tags are discarded
    Clash:
    If single largest hand among clashing viruses, discard 1 card.
    """

    def __init__(self):
        C.Card.__init__(self, "Computer Virus", 30)
        self.add_symbol(C.Card.Symbols[4])      # Weapons

    def main_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        mypb.victorypoints += 2
        for opbidx in range(len(game.playerboards)):
            if opbidx != pbidx:
                opb = game.playerboards[opbidx]
                if not opb.ignore_main_effect(game, pbidx, ["discard"]):
                    for card in opb.recoveryzone:
                        if C.Card.Symbols[3] in card.symbols:
                            opb.discard(card, ["recovery"])

    def clash_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        handsize = len(mypb.hand)
        highest = True
        for opbidx in range(len(game.playerboards)):
            if opbidx != pbidx:
                othpb = game.playerboards[opbidx]
                if len(othpb.inplay) > 0 and \
                        othpb.inplay[0].rank == self.rank:
                    if handsize <= len(othpb.hand):
                        highest = False
        if highest:
            card = mypb.player.choosecardtodiscard(game, pbidx,
                                                   ["hand", "recovery"])
            mypb.discard(card, ["hand", "recovery"])

if __name__ == '__main__':
    cv = ComputerVirus()
    print("Created " + cv.title + ", rank " + str(cv.rank))
