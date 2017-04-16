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
        # print("Checking defense in " + self.title + " vs. " + str(effect))
        if thisorlast == "this":
            # print("   Checking for this round (not last)")
            if "main_effect" in effect:
                mypb = game.playerboards[pbidx]
                # print("        Player index " + str(pbidx) + ", hand: " +
                #      str(mypb.printhand()))
                return(len(mypb.hand) <= 2)
            else:
                return(False)
        else:
            return(False)

if __name__ == '__main__':
    import HeavyAssault as HA
    import Game
    import RandomComputerPlayer as RCP

    g = Game.Game(3)
    for rcpi in range(3):
        rcp = RCP.RandomComputerPlayer("Random Player " + str(rcpi+1))
        g.playerboards[rcpi].player = rcp

    cd = CloakingDevice()
    ha = HA.HeavyAssault()
    g.addtocardlist(cd)
    g.addtocardlist(ha)
    c = C.Card("No-op card 0", 88)
    g.addtocardlist(c)
    g.sendcardlisttoboards()

    pb0 = g.playerboards[0]
    pb0.readytoplay(cd)
    pb1 = g.playerboards[1]
    pb1.readytoplay(ha)

    print("Before playing " + cd.title + " vs. " + ha.title)
    print(pb0)
    # g.playallcards()
    g.playcards()
    print("After " + cd.title + " vs. " + ha.title)
    print("    (should still have 1 VP)")
    print(pb0)
    assert(pb0.victorypoints == 1)
