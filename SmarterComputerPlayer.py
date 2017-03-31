# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 21:25:00 2017

@author: bushnelf
"""

import random

import RandomComputerPlayer as rcp


class SmarterComputerPlayer(rcp.RandomComputerPlayer):
    """
    SmarterComputerPlayer - weight card plays toward cards seen
    in other players' recovery zones.
    Only slightly smarter, as it'd be better still to keep
    track of everything played, so you'd (eventually) know what
    was in all of the other players' decks.
    """

    def __init__(self, name):
        rcp.RandomComputerPlayer.__init__(self, "Smarter " + name)

    def choosecardtoplay(self, game, myphbidx):
        """ We'll start out making it twice as likely the player will
        pick a card in another player's recovery zone as other cards
        in our hand.  Count cards in multiple other RZs multiple times.
        """
        choosefrom = []
        card = None
        myboard = game.playerboards[myphbidx]
        ranksinhand = []
        for mycard in myboard.hand:
            ranksinhand.append(mycard.rank)
            # include our hand's ranks in the choices
            choosefrom.append(mycard.rank)
        print(self.name + " initial options: " + str(choosefrom))

        for pbidx in range(len(game.playerboards)):
            if pbidx != myphbidx:
                for theirrzcard in game.playerboards[pbidx].recoveryzone:
                    if theirrzcard.rank in ranksinhand:
                        choosefrom.append(theirrzcard.rank)
        print(self.name + " final options: " + str(choosefrom))

        if len(choosefrom) > 0:
            idx = random.randint(0, len(choosefrom)-1)
            for mycard in myboard.hand:
                if mycard.rank == choosefrom[idx]:
                    card = mycard
        return(card)

if __name__ == '__main__':
    scp = SmarterComputerPlayer("idiot player")
    print("Created " + scp.name)
