# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 21:14:22 2017

@author: bushnelf
"""

import Card as C


class CloakingDevice(C.Card):
    """
    CloakingDevice:
    If you have a Weapon icon card in RZ, choose an opponent to
        discard 1 card.  If you have <= 2 cards in hand, ignore
        oppenents' main effects this round.
    No Clash effect
    """

    def __init__(self):
        C.Card.__init__(self, "Cloaking Device", 4)
        self.add_symbol(C.Card.Symbols[3])      # Technology
        self.add_symbol(C.Card.Symbols[0])      # Negation

    def main_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        rzweapon = False
        for card in mypb.recoveryzone:
            if C.Card.Symbols[4] in card.symbols:
                rzweapon = True
        if rzweapon:
                tgtpbidx = mypb.player.chooseplayertodiscard(game, pbidx,
                                                             ["hand",
                                                              "recovery"])
                if tgtpbidx is not None:
                    pbo = game.playerboards[tgtpbidx]
                    card = pbo.player.choosecardtodiscard(game, tgtpbidx,
                                                          ["hand", "recovery"])
                    pbo.discard(card, ["hand", "recovery"])

    def defense(self, game, pbidx, effect=["main_effect"], thisorlast="this"):
        if thisorlast == "this":
            mypb = game.playerboards[pbidx]
            return(len(mypb.hand) <= 2)
        else:
            return(False)

if __name__ == '__main__':
    c = CloakingDevice()
