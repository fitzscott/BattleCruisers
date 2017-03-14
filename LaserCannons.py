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
        myboard = game.playerboards[pbidx]
        for pb in game.playerboards:
            if pb != myboard and pb.protected == 0:
                (cardidx, deck) = \
                    pb.player.choosecardtodiscard(game, pbidx,
                                                  ["hand", "recovery"])
                card = pb.cardbyindex(cardidx, deck)
                pb.discard(card, [deck])

    def clash_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        (cardidx, deck) = myboard.player.\
            choosecardtodiscard(game, pbidx, ["hand", "recovery"])
        card = myboard.cardbyindex(cardidx, deck)
        myboard.discard(card, [deck])

if __name__ == '__main__':
    import Game
    import Player

    g = Game.Game(3)
    lc = LaserCannons()

    class ZeroPlayer(Player.Player):
        """
        ZeroPlayer - just return zero
        """
        def choosecardtodiscard(self, game, myphbidx, deck="hand"):
            return((0, "hand"))

    zp = ZeroPlayer("Zero to hero")
    g.playerboards[0].player = zp
    g.playerboards[1].player = zp
    g.playerboards[2].player = zp
    c1 = Card.Card("No such card", 88)
    c2 = Card.Card("Still no such card", 89)
    g.addtocardlist(lc)
    g.addtocardlist(c1)
    g.addtocardlist(c2)
    g.sendcardlisttoboards()
    g.playerboards[0].addtohand(c1)
    g.playerboards[1].addtohand(c2)
    g.playerboards[2].addtohand(lc)
    g.playerboards[2].readytoplay(lc)
    print("++++++    All cards should be in hand:")
    print(g.playerboards[0])
    print(g.playerboards[1])
    g.playallcards()
    print("++++++    1st card should be in discards:")
    print(g.playerboards[0])
    print(g.playerboards[1])
