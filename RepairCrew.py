# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 17:52:48 2017

@author: bushnelf
"""

import Card as C


class RepairCrew(C.Card):
    """
    Repair Crew:
    Return card from discard pile to hand.
    Technology symbol in RZ => 2VP
    No clash
    """
    def __init__(self):
        C.Card.__init__(self, "Repair Crew", 16)
        self.add_symbol(C.Card.Symbols[2])       # People

    def main_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        myboard.returndiscardtohand(game, pbidx)
        if myboard.checkrecoveryforsymbol(C.Card.Symbols[3]):   # Tech
            myboard.victorypoints += 2

if __name__ == '__main__':
    rc = RepairCrew()
    print("Created " + rc.title + ", rank " + str(rc.rank))
