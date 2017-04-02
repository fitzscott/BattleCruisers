# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 12:15:05 2017

@author: bushnelf
"""

import Card


class Ambassador(Card.Card):
    """
    Ambassador:
    Gain 1 VP
    Opponents clashed:  Gain 2 VP
    Space symbol in RZ:  Gain 1 VP
    """

    def __init__(self):
        Card.Card.__init__(self, "Ambassador", 17)
        self.add_symbol(Card.Card.Symbols[2])
        self._nuke = 0

    def main_effect(self, game, pbidx):
        print("Running card " + self.title + "'s main effect")
        # gain 1 VP
        myboard = game.playerboards[pbidx]
        myboard.victorypoints += 1
        # check clash => gain 2 VP
        if game.numclashes >= 2:
            myboard.victorypoints += 2
        # check for maneuver symbol in recovery
        if myboard.checkrecoveryforsymbol("Space"):
            myboard.victorypoints += 1

    def clash_effect(self, game, pbidx):
        """
        Lose a VP
        """
        myboard = game.playerboards[pbidx]
        myboard.victorypoints -= 1

if __name__ == '__main__':
    import Game
    import RandomComputerPlayer as RCP

    g = Game.Game(3)
    a = Ambassador()
    pb = g.playerboards[0]
    pb.addtohand(a)
    pb.readytoplay(a)
    a.clash_effect(g, 0)
    print("VP should still be 0: " + str(pb.victorypoints))
    pb.victorypoints = 3
    a.clash_effect(g, 0)
    print("VP should be 2: " + str(pb.victorypoints))

    for rcpi in range(3):
        rcp = RCP.RandomComputerPlayer("Random Player " + str(rcpi+1))
        g.playerboards[rcpi].player = rcp

    g.addtocardlist(a)
    c = Card.Card("Test", 50)
    # add Space symbol = 1 VP if in recovery
    c.add_symbol(Card.Card.Symbols[5])
    g.addtocardlist(c)
    g.sendcardlisttoboards()
    # induce clash = 2 VP
    g.playerboards[1].readytoplay(c)
    g.playerboards[2].readytoplay(c)
    # put Space card in RZ for test board
    pb.recoveryzone.append(c)
    pb.victorypoints = 0
    g.playallcards()
    # effectively running a.main_effect(g, 0)
    print("VP should be 4: " + str(pb.victorypoints))
