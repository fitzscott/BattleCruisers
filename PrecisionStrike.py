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
                tgtpb.discard(card, ["hand"])
            elif len(tgthand) > 0:
                # Switch out real hand, restore later
                orighand = tgtpb.hand
                tgtpb.hand = tgthand
                card = pb.player.choosecardtodiscard(game, tgtpl, ["hand"])
                tgtpb.hand = orighand
                tgtpb.discard(card, ["hand"])

    def clash_effect(self, game, pbidx):
        game.playerboards[pbidx].discard(self, ["inplay"])

if __name__ == '__main__':
    import Game
    import RandomComputerPlayer as RCP

    g = Game.Game(3)
    for rcpi in range(3):
        rcp = RCP.RandomComputerPlayer("Random Player " + str(rcpi+1))
        g.playerboards[rcpi].player = rcp

    ps = PrecisionStrike()
    for i in range(3):
        c = C.Card("No-op card " + str(i), 50+i)
        g.addtocardlist(c)
    g.addtocardlist(ps)
    g.sendcardlisttoboards()

    for pbi in range(2):
        g.playerboards[pbi].readytoplay(ps)
    g.playerboards[2].readytoplay(c)
    print("    hand size = " + str(g.playerboards[0].hand))
    print("Before playing " + ps.title + ":")
    print(g.playerboards[0])
    # g.playallcards()
    g.playcards()
    print("Two copies of " + ps.title + " (" + str(ps.rank) +
          ") should be in discards:")
    for pbi in range(3):
        print(g.playerboards[pbi])
    g.endturn()

    g.playerboards[2].readytoplay(ps)
    for pbi in range(2):
        g.playerboards[pbi].readytoplay(c)
    print("Random player 3 should force a discard in player 1 or 2")
    # g.playallcards()
    g.playcards()
    print("    Chosen target player should have 1 fewer cards in hand.")
    for pbi in range(3):
        print(g.playerboards[pbi])
    g.endturn()
