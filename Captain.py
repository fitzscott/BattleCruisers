# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 11:10:10 2017

@author: bushnelf
"""

import Card


class Captain(Card.Card):
    """
    Captain - gain 3 VP, diminishing by clash
    """

    def __init__(self):
        Card.Card.__init__(self, "Captain", 13)
        self.add_symbol(Card.Card.Symbols[2])
        self.add_symbol(Card.Card.Symbols[3])

    def main_effect(self, game, pbidx):
        # print("Called " + self.title + " main_effect")
        myboard = game.playerboards[pbidx]
        myboard.victorypoints = myboard.victorypoints + 3

    def clash_effect(self, game, pbidx):
        """
        Count number of players playing "Captain" (including this player)
        and add 3 VP minus that number.
        """
        # print("Called " + self.title + " clash_effect")
        myboard = game.playerboards[pbidx]
        vptoadd = 3
        for pb in game.playerboards:
            if len(pb.inplay) > 0 and pb.inplay[0].rank == self.rank:
                vptoadd -= 1
        myboard.victorypoints += vptoadd

if __name__ == '__main__':
    import Game

    g = Game.Game(4)
    c1 = Captain()
    print("Created " + c1.title + " card.")
    # Only creating 2 to see whether the clash works
    c2 = Captain()
    g.playerboards[0].addtohand(c1)
    g.playerboards[0].readytoplay(c1)
    g.playerboards[2].addtohand(c2)
    g.playerboards[2].readytoplay(c2)
    # Set up player board with 5 VP to start
    g.playerboards[0].victorypoints = 5
    g.playallcards()
    print("Player board 0 has " + str(g.playerboards[0].victorypoints) +
          " victory points (should be 6)")
    c3 = Captain()
    g.playerboards[3].addtohand(c3)
    g.playerboards[3].readytoplay(c3)
    g.playallcards()
    print("Player board 0 has " + str(g.playerboards[0].victorypoints) +
          " victory points (should still be 6)")
    # Finally, make them all Captains
    c4 = Captain()
    g.playerboards[1].addtohand(c4)
    g.playerboards[1].readytoplay(c4)
    g.playallcards()
    print("Player board 0 has " + str(g.playerboards[0].victorypoints) +
          " victory points (should be 5)")
    # Decrease VP to zero
    g.playallcards()
    g.playallcards()
    g.playallcards()
    g.playallcards()
    g.playallcards()
    print("Player board 0 has " + str(g.playerboards[0].victorypoints) +
          " victory points (should be 0)")
    # and make sure VP can't go below zero
    g.playallcards()
    print("Player board 0 has " + str(g.playerboards[0].victorypoints) +
          " victory points (should still be 0)")
    print("Number of clashes in game = " + str(g.numclashes) + " (s/b 4)")
