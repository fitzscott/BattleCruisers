# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 22:54:42 2017

@author: bushnelf
"""

import Card


class SpyDrone(Card.Card):
    """
    Spy Drone - swap w/ card in your hand.
    """

    def __init__(self):
        Card.Card.__init__(self, "Spy Drone", 1)
        self.add_symbol(Card.Card.Symbols[3])
        self.add_symbol(Card.Card.Symbols[5])

    def main_effect(self, game, pbidx):
        """
        main_effect -
        Swap spy drone w/ another card in hand.
        Inform game to re-figure card ordering.
        """
        myboard = game.playerboards[pbidx]
        card = myboard.player.choosecardtoswap(game, pbidx, ["hand"])
        if card is not None:
            print("----- before SpyDrone swap")
            print(myboard.printinplay())
            print(myboard.printhand())
            myboard.hand.append(self)
            myboard.inplay.remove(self)
            myboard.inplay.append(card)
            myboard.hand.remove(card)
            print("----- after SpyDrone swap")
            print(myboard.printinplay())
            print(myboard.printhand())
            game.playallcards()     # works because SpyDrone is #1

    def end_of_turn_effect(self, game, pbidx):
        """
        end_of_turn_effect -
        If this is the last card, discard it.
        """
        myboard = game.playerboards[pbidx]
        if myboard.checkredalert():
            myboard.discard(self, ["inplay"])
            # print("Last card! Red alert!")

if __name__ == '__main__':
    import Game

    sd = SpyDrone()
    print("Created card " + sd.title)
    g = Game.Game(1)
    # Need to figure out how to get the cards listed on the player
    # board to register in our tests.
    # g.addtocardlist(sd)
    # g.sendcardlisttoboards()
    sd.main_effect(g, 0)
    sd.end_of_turn_effect(g, 0)
