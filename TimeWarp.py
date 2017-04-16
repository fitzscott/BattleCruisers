# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 22:40:15 2017

@author: bushnelf
"""

import Card as C


class TimeWarp(C.Card):
    """
    Time Warp:
    Lose all VP.
    Return all discards from discard pile to hand, then discard
        this card (TimeWarp).
    Then sing, "Let's do the time warp again".
    No Clash (obviously - not their song at all)
    """
    def __init__(self):
        C.Card.__init__(self, "Time Warp", 45)
        self.add_symbol(C.Card.Symbols[5])      # Space

    def main_effect(self, game, pbidx):
        pb = game.playerboards[pbidx]
        pb.victorypoints = 0
        cpdisc = []
        for card in pb.discards:
            cpdisc.append(card)
        for card in cpdisc:
            pb.hand.append(card)
            pb.discards.remove(card)
        pb.discard(self, ["inplay"])

if __name__ == '__main__':
    import Game
    import RandomComputerPlayer as RCP

    g = Game.Game(3)
    for rcpi in range(3):
        rcp = RCP.RandomComputerPlayer("Random Player " + str(rcpi+1))
        g.playerboards[rcpi].player = rcp

    tw = TimeWarp()
    for i in range(3):
        c = C.Card("No-op card " + str(i), 50+i)
        g.addtocardlist(c)
    g.addtocardlist(tw)
    g.sendcardlisttoboards()

    pb = g.playerboards[0]
    # print("Before getting " + tw.title + "ready to play:")
    # print(pb)

    pb.readytoplay(tw)
    print("    hand size = " + str(len(pb.hand)))
    for cnt in range(len(pb.hand)):       # move them all into discards
        c = pb.hand[0]
        pb.discard(c, ["hand"])

    print("Before playing " + tw.title + ":")
    print(pb)
    # g.playallcards()
    g.playcards()
    # effectively running a.main_effect(g, 0)
    print("3 discards should be back in hand:")
    print(pb)
