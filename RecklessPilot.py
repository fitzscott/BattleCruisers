# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 22:05:57 2017

@author: bushnelf
"""

import Card


class RecklessPilot(Card.Card):
    """
    Reckless Pilot - discard a card, get 4 VP
    """

    def __init__(self):
        Card.Card.__init__(self, "Reckless Pilot", 11)
        self.add_symbol(self.Symbols[2])

    def main_effect(self, game, pbidx):
        """
        Discard 1 card + get 4 VP
        """
        myboard = game.playerboards[pbidx]
        card = myboard.player.choosecardtodiscard(game, pbidx,
                                                  ["hand", "recovery"])
        myboard.discard(card, ["hand", "recovery"])
        myboard.victorypoints += 4

    def clash_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        card = myboard.player.choosecardtodiscard(game, pbidx,
                                                  ["hand", "inplay"])
        myboard.discard(card, ["hand", "inplay"])

    def end_of_turn_effect(self, game, pbidx):
        pass

if __name__ == '__main__':
    rp = RecklessPilot()
    print("Created " + rp.title + " card.")
    if "People" in rp.symbols:
        print("Contains People symbol.")
    import Game
    import RandomComputerPlayer

    g = Game.Game(3)

    zp = RandomComputerPlayer.RandomComputerPlayer("Zero to hero")
    g.playerboards[0].player = zp
    g.playerboards[1].player = zp
    g.playerboards[2].player = zp
    c1 = Card.Card("No such card", 88)
    c2 = Card.Card("Still no such card", 89)
    c3 = Card.Card("Again no such card", 90)
    g.addtocardlist(rp)
    g.addtocardlist(c1)
    g.addtocardlist(c2)
    g.addtocardlist(c3)
    g.sendcardlisttoboards()
    g.playerboards[2].readytoplay(rp)
    # g.playallcards()
    g.playcards()
    print("After 1 reckless pilot:")
    print(g.playerboards[2])
    g.playerboards[0].readytoplay(rp)
    g.playerboards[1].readytoplay(rp)
    # manually move the 2nd player's hand to RZ
    tomv = []
    for card in g.playerboards[1].hand:
        # print("Checking card " + card.title)
        if card.title != "Reckless Pilot":    # shouldn't be
            tomv.append(card)
    for card in tomv:
        # print("Moving " + card.title + " from player 1 to RZ")
        g.playerboards[1].recoveryzone.append(card)
        g.playerboards[1].hand.remove(card)
    print("Before 3 reckless pilots:")
    print(g.playerboards[0])
    print(g.playerboards[1])
    print(g.playerboards[2])
    # g.playallcards()
    g.playcards()
    print("After 3 reckless pilots:")
    print(g.playerboards[0])
    print(g.playerboards[1])
    print(g.playerboards[2])
