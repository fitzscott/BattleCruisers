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
        # if the card has somehow left the inplay area, it cannot perform
        # its swap.
        if len(myboard.inplay) == 0:
            print(self.title + " is no longer available.")
            return
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
    import RandomComputerPlayer as RCP

    sd = SpyDrone()
    print("Created card " + sd.title)
    c = Card.Card("Swap Me", 99)
    g = Game.Game(1)
    rcp = RCP.RandomComputerPlayer("RCP 1")
    g.playerboards[0].player = rcp
    g.addtocardlist(sd)
    g.addtocardlist(c)
    g.sendcardlisttoboards()
    g.playerboards[0].readytoplay(sd)
    # g.playallcards()
    g.playcards()
    # sd.main_effect(g, 0)
    # sd.end_of_turn_effect(g, 0)
