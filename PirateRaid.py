# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 18:26:08 2017

@author: bushnelf
"""

import Card as C


class PirateRaid(C.Card):
    """
    Pirate Raid:
    Discard this card.
    Each opponent gives you a card from their hand.
    Clash: Discard 2 cards.
    """

    def __init__(self):
        C.Card.__init__(self, "Pirate Raid", 32)
        self.add_symbol(C.Card.Symbols[5])      # Space
        self.add_symbol(C.Card.Symbols[4])      # Weapons

    def main_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        # cards that prevent main effects from causing discards
        # also cause this card's main effect not to discard itself.
        if not mypb.defense(game, pbidx, ["card_discard"]):
            mypb.discard(self, ["inplay"])
        for pboi in range(len(game.playerboards)):
            if pboi != pbidx:
                pbo = game.playerboards[pboi]
                # This applies to all opponents, but they may have a defense
                if pbo.protected != 0 or \
                        pbo.ignore_main_effect(game, pboi, ["card_theft"]):
                    continue
                card = pbo.player.choosecardtogiveaway(game, pboi, ["hand"])
                if card is not None:
                    mypb.hand.append(card)
                    pbo.hand.remove(card)

    def clash_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        for dsc in range(2):
            card = mypb.player.choosecardtodiscard(game, pbidx,
                                                   ["hand", "recovery"])
            mypb.discard(card, ["hand", "recovery"])

if __name__ == '__main__':
    pr = PirateRaid()
    print("Created " + pr.title)
