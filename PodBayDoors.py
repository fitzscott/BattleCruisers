# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 19:28:50 2017

@author: bushnelf
"""

import Card as C


class PodBayDoors(C.Card):
    """
    Pod Bay Doors:
    Resolve the card played next round twice.
    If this is the only card at the end of the round, discard it.
    Clash:  Lose 1VP
    """
    def __init__(self):
        C.Card.__init__(self, "Pod Bay Doors", 15)
        self.symbols.append(C.Card.Symbols[3])       # Technology

    def main_effect(self, game, pbidx):
        """ The player board will keep track of this for the next
            couple of rounds, and the game will know how to apply
            the double action. """
        game.playerboards[pbidx].doubleplay = 2

    def clash_effect(self, game, pbidx):
        game.playerboards[pbidx].victorypoints -= 1

    def end_of_turn_effect(self, game, pbidx):
        """
        end_of_turn_effect -
        If this is the last card, discard it.
        """
        myboard = game.playerboards[pbidx]
        if myboard.checkredalert():
            # cards that prevent main effects from causing discards
            # also cause this card's main effect not to discard itself.
            if not myboard.defense(game, pbidx, ["card_discard"]):
                myboard.discard(self, ["inplay"])
            print("Discarding last card " + self.title)

if __name__ == '__main__':
    pbd = PodBayDoors()
