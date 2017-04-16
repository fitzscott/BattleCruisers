# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 21:23:28 2017

@author: bushnelf
"""

import Card


class Shields(Card.Card):
    """
    Shields - ignore opponents' main effect 2 rounds
    """

    def __init__(self):
        Card.Card.__init__(self, "Shields", 3)
        self.add_symbol(Card.Card.Symbols[3])
        self.add_symbol(Card.Card.Symbols[0])

    def main_effect(self, game, pbidx):
        """
        Ignore opponents' main effect for this round & next.
        That effectively puts the "protected" flag on the
        player board.
        """
        myboard = game.playerboards[pbidx]
        myboard.protected = 2

    def end_of_turn_effect(self, game, pbidx):
        """
        end_of_turn_effect -
        If this is the last card, discard it.
        """
        myboard = game.playerboards[pbidx]
        if myboard.checkredalert():
            myboard.discard(self, ["inplay"])
            print("Discarding last card " + self.title)

    def defense(self, game, pbidx, effect=["main_effect"], thisorlast="this"):
        """ Shields ignore main effects for 2 rounds - this + last """
        return(True)

if __name__ == '__main__':
    import Game

    s = Shields()
    if "Negation" in s.symbols:
        print("Shields card has Negation symbol.")
    g = Game.Game(1)
    pb = g.playerboards[0]
    pb.addtohand(s)
    pb.readytoplay(s)
    # g.playallcards()
    g.playcards()
    if pb.protected > 0:
        print("Player board is protected by " + s.title)
    g.endturn()
    print(pb)
