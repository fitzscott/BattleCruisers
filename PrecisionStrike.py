# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 15:29:06 2017

@author: bushnelf
"""

import Card as C


class PrecisionStrike(C.Card):
    """
    Precision Strike:
    Choose an opponent, look at hand, force one discard.
    Can force discard of precision strike unless it is the only
    card in their hand.
    Clash:  Discard this card.
    """

    def __init__(self):
        C.Card.__init__(self, "Precision Strike", 34)
        self.add_symbol(C.Card.Symbols[4])          # Weapons

    def main_effect(self, game, pbidx):
        pb = game.playerboards[pbidx]
        tgtpl = pb.player.chooseplayertodiscard(game, pbidx, ["hand"])
        if tgtpl is not None:
            tgtpb = game.playerboards[tgtpl]
            tgthand = []
            foundthiscard = False
            for card in tgtpb.hand:
                if card.title != self.title:
                    tgthand.append(card)
                else:
                    foundthiscard = True
            if len(tgthand) == 0 and foundthiscard:   # only precision strike
                card = pb.player.choosecardtodiscard(game, tgtpl, ["hand"])
            elif len(tgthand) > 0:
                # Switch out real hand, restore later
                orighand = tgtpb.hand
                tgtpb.hand = tgthand
                card = pb.player.choosecardtodiscard(game, tgtpl, ["hand"])
                tgtpb.hand = orighand
                pb.discard(card, ["hand"])

    def clash_effect(self, game, pbidx):
        game.playerboards[pbidx].discard(self, ["inplay"])
