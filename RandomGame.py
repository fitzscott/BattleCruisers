# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 22:24:42 2017

@author: bushnelf
"""

import Game
import CardSet
import RandomComputerPlayer


class RandomGame(Game.Game):
    def __init__(self, numplayers, numrounds=10):
        Game.Game.__init__(self, numplayers)
        self._numrounds = numrounds

    def playrounds(self, numrounds):
        for gameround in range(numrounds):
            print("**********     Round " + str(gameround) + "     ********")
            print("!!!   Before")
            for pbidx in range(len(g.playerboards)):
                pb = g.playerboards[pbidx]
                card = pb.player.choosecardtoplay(g, pbidx)
                pb.readytoplay(card)
                print("Player board " + pb.player.name + ":")
                print(pb)
            g.playallcards()
            print("!!!   After")
            for pbidx in range(len(g.playerboards)):
                pb = g.playerboards[pbidx]
                print("Player board " + pb.player.name + ":")
                print(pb)
            g.endturn()
            print("!!!   Post turn")
            for pbidx in range(len(g.playerboards)):
                pb = g.playerboards[pbidx]
                print("Player board " + pb.player.name + ":")
                print(pb)

if __name__ == '__main__':
    g = RandomGame(3)
    for rcpi in range(3):
        rcp = RandomComputerPlayer.RandomComputerPlayer("Random Player " +
                                                        str(rcpi+1))
        g.playerboards[rcpi].player = rcp
    cs = CardSet.CardSet(3)
    g.cardlist = cs.getcardset()
    g.sendcardlisttoboards()
    for dnr in range(3):
        pb = g.playerboards[dnr]
        c = pb.player.choosecardtodiscard(g, dnr, ["hand"])
        pb.discard(c, ["hand"])
        c = pb.player.choosecardtosendtorecovery(g, dnr)
        pb.sendtorecovery(c)
    g.playrounds(10)
