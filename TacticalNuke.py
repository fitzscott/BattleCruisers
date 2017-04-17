# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 13:55:27 2017

@author: bushnelf
"""

import Card as C


class TacticalNuke(C.Card):
    """
    Tactical Nuke:
    Discard 1 card, opponents discard 2 cards.
    Clash: Discard 3 cards, w/ this card among options to discard.
    """

    def __init__(self):
        C.Card.__init__(self, "Tactical Nuke", 38)
        self.add_symbol(C.Card.Symbols[4])

    def main_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        mycard = mypb.player.choosecardtodiscard(game, pbidx, ["hand",
                                                               "recovery"])
        # per the rules & Board Game Geek, you can play this even if
        # you have no cards to discard.
        if mycard is not None:
            # cards that prevent main effects from causing discards
            # also cause this card's main effect not to discard itself.
            if not mypb.defense(game, pbidx, ["card_discard"]):
                mypb.discard(mycard, ["hand", "recovery"])
        # Other players discard 2 cards each.  Boom.
        for opbidx in range(len(game.playerboards)):
            if opbidx != pbidx:
                opb = game.playerboards[opbidx]
                for discidx in range(2):
                    card = opb.player.choosecardtodiscard(game, opbidx,
                                                          ["hand", "recovery"])
                    opb.discard(card, ["hand", "recovery"])

    def clash_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        # Discard 3, including in play card (this one)
        for discidx in range(3):
            mycard = mypb.player.choosecardtodiscard(game, pbidx,
                                                     ["hand", "inplay",
                                                      "recovery"])
            if mycard is not None:
                mypb.discard(mycard, ["hand", "inplay", "recovery"])

if __name__ == '__main__':
    tn = TacticalNuke()
    print("Created " + tn.title + ", rank " + str(tn.rank))
