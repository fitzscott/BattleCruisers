# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 21:46:07 2017

@author: bushnelf
"""

import Card


class AttackBots(Card.Card):
    """
    AttackBots:
    Main: Take a card from an opponent's RZ into your hand.
    Clash: Discard card in RZ
    """

    def __init__(self):
        Card.Card.__init__(self, "Attack Bots", 29)
        self.add_symbol(Card.Card.Symbols[4])

    def main_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        (pl, cardidx) = myboard.player.chooseplayertotakecardfrom(game, pbidx,
                                                                  "recovery")
        targetpb = game.playerboards[pl]
        card = targetpb.recoveryzone[cardidx]
        myboard.hand.append(card)
        targetpb.recoveryzone.remove(card)

    def clash_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        rzcardidx = myboard.player.choosecardtodiscard(game, pbidx, "recovery")
        if rzcardidx >= 0:
            rzcard = myboard.recoveryzone[rzcardidx]
            myboard.discard(rzcard, "recovery")

if __name__ == '__main__':
    ab = AttackBots()

    import Player
    import Game

    class ZeroPlayer(Player.Player):
        """
        ZeroPlayer - just return zero
        """
        def choosecardtodiscard(self, game, myphbidx, deck="hand"):
            return(0)

        def chooseplayertotakecardfrom(self, game, myphbidx, deck="hand"):
            return((0, 0))

    g = Game.Game(2)
    zp = ZeroPlayer("Zero Player")
    testplayer = 1
    testpb = g.playerboards[testplayer]
    g.playerboards[testplayer].player = zp
    dm = Card.Card("Discard Me", 88)
    g.addtocardlist(dm)
    g.addtocardlist(ab)
    g.sendcardlisttoboards()
    testpb.readytoplay(dm)
    testpb.endplay()
    print("Before clash effect:")
    print(testpb)
    ab.clash_effect(g, testplayer)
    print("After - Discard Me to discards:")
    print(testpb)
    print("Target player, before:")
    tgtpb = g.playerboards[0]
    tgtpb.readytoplay(dm)
    tgtpb.endplay()
    print(tgtpb)
    print("Target player, after:")
    ab.main_effect(g, testplayer)
    print(tgtpb)
    print("Test player (extra card now), after:")
    print(testpb)
