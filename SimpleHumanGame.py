# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 20:59:24 2017

@author: bushnelf
"""

import Game
import CardSet
import SimpleHumanPlayer


class SimpleHumanGame(Game.Game):
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
            input("--- --- ---   Hit 0 Enter to contine")
            g.playallcards()
            print("!!!   After")
            for pbidx in range(len(g.playerboards)):
                pb = g.playerboards[pbidx]
                print("Player board " + pb.player.name + ":")
                print(pb)
            input("--- --- ---   Hit 0 Enter to contine")
            if g.endturn():     # winner winner chicken dinner
                break
            print("!!!   Post turn")
            for pbidx in range(len(g.playerboards)):
                pb = g.playerboards[pbidx]
                print("Player board " + pb.player.name + ":")
                print(pb)
                input("--- --- ---   Hit 0 Enter to contine")

if __name__ == '__main__':
    g = SimpleHumanGame(3)
    # plrz = ["Rosie", "Gennifer", "Beatrice"]
    plrz = ["Grace", "Pam", "Olivia"]
    for shpi in range(3):
        shp = SimpleHumanPlayer.SimpleHumanPlayer(plrz[shpi])
        g.playerboards[shpi].player = shp
    cs = CardSet.CardSet(3)
    g.cardlist = cs.getcardset()
    g.sendcardlisttoboards()
    for dnr in range(3):
        pb = g.playerboards[dnr]
        c = pb.player.choosecardtodiscard(g, dnr, ["hand"])
        pb.discard(c, ["hand"])
        c = pb.player.choosecardtosendtorecovery(g, dnr)
        pb.sendtorecovery(c)
    g.playrounds(30)
