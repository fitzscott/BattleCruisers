# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 22:58:40 2017

@author: bushnelf
"""

import Card


class LaserCannons(Card.Card):
    """
    Laser Cannons - each opponent discards 1 card.
        Clash:  This board discards 1 card.
    """

    def __init__(self):
        Card.Card.__init__(self, "Laser Cannons", 31)
        self.add_symbol(Card.Card.Symbols[4])   # Weapons

    def main_effect(self, game, pbidx):
        for pbothidx in range(len(game.playerboards)):
            pbo = game.playerboards[pbothidx]
            if pbothidx != pbidx and pbo.protected == 0:
                card = pbo.player.choosecardtodiscard(game, pbothidx,
                                                      ["hand", "recovery"])
                pbo.discard(card, ["hand", "recovery"])

    def clash_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        card = myboard.player.choosecardtodiscard(game, pbidx,
                                                  ["hand", "recovery"])
        print("Discarding card " + card.title)
        myboard.discard(card, ["hand", "recovery"])

if __name__ == '__main__':
    import Game
    import Player

    g = Game.Game(3)
    lc = LaserCannons()

    class ZeroPlayer(Player.Player):
        """
        ZeroPlayer - just return zero
        """
        def choosecardtodiscard(self, game, myphbidx, deck):
            # return((0, "hand"))
            pb = game.playerboards[myphbidx]
            if "hand" in deck and len(pb.hand) > 0:
                return(pb.hand[0])
            elif "recovery" in deck and len(pb.recoveryzone) > 0:
                return(pb.recoveryzone[0])
            else:
                return(None)

    zp = ZeroPlayer("Zero to hero")
    g.playerboards[0].player = zp
    g.playerboards[1].player = zp
    g.playerboards[2].player = zp
    c1 = Card.Card("No such card", 88)
    c2 = Card.Card("Still no such card", 89)
    c3 = Card.Card("Again no such card", 90)
    g.addtocardlist(lc)
    g.addtocardlist(c1)
    g.addtocardlist(c2)
    g.addtocardlist(c3)
    g.sendcardlisttoboards()
    g.playerboards[2].readytoplay(lc)
    print("++++++    All cards should be in hand:")
    print(g.playerboards[0])
    print(g.playerboards[1])
    g.playallcards()
    print("++++++    1st card should be in discards:")
    print(g.playerboards[0])
    print(g.playerboards[1])
    g.endturn()
    print("####    Test 2 start    ####")
    for pb in g.playerboards:
        print(pb)
    # manually move the LC card from RZ to hand
    g.playerboards[2].hand.append(lc)
    g.playerboards[2].recoveryzone.remove(lc)
    # print("Player 1's hand has " + str(len(g.playerboards[1].hand)))
    # and manually move the 2nd player's hand to RZ
    tomv = []
    for card in g.playerboards[1].hand:
        # print("Checking card " + card.title)
        if card.title != "Laser Cannons":
            tomv.append(card)
    for card in tomv:
        g.playerboards[1].recoveryzone.append(card)
        g.playerboards[1].hand.remove(card)
    # for players 0 & 1, move the LC from discards to hand
    for pidx in range(2):
        g.playerboards[pidx].discards.remove(lc)
        g.playerboards[pidx].hand.append(lc)
    print("####    1 w/all hand, 1 w/ all RZ    ####")
    for pb in g.playerboards:
        pb.readytoplay(lc)
        print(pb)
    g.playallcards()    # should all be clashes
    print("####    1 card from hand or RZ -> discards   ####")
    for pb in g.playerboards:
        print(pb)
