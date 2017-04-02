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
        pl = myboard.player.chooseplayertotakecardfrom(game, pbidx,
                                                       ["recovery"])
        print("Chose player " + str(pl) + " (I am " + str(pbidx) + ")")
        print("My RZ: " + myboard.printrecover())
        if pl >= 0:
            targetpb = game.playerboards[pl]
            print("Chosen RZ: " + targetpb.printrecover())
            card = myboard.player.choosecardfromplayer(game, pbidx,
                                                       ["recovery"], pl)
            if card is not None:
                print("Chose card: " + card.title + ", rank: " +
                      str(card.rank))
                # player chooser should not choose a protected opponent,
                # but if it does, disallow the effect.
                if targetpb.protected == 0:
                    myboard.hand.append(card)
                    targetpb.recoveryzone.remove(card)
                else:
                    print("Cannot steal a card from a protected player")
            else:
                print("How'd we get no cards?")
        else:
            print("No choices among recovery zones")

    def clash_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        rzcard = myboard.player.choosecardtodiscard(game, pbidx, ["recovery"])
        if rzcard is not None:
            myboard.discard(rzcard, ["recovery"])

if __name__ == '__main__':
    ab = AttackBots()

    import Player
    import Game

    class ZeroPlayer(Player.Player):
        """
        ZeroPlayer - just return zero
        """
        # This definition will not work in the general case -
        # need to return which deck it's being discarded from.
        def choosecardtodiscard(self, game, myphbidx, deck="hand"):
            return(game.playerboards[myphbidx].recoveryzone[0])

        def chooseplayertotakecardfrom(self, game, myphbidx, deck=["hand"]):
            return(0)

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
