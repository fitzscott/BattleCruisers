# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 21:18:38 2017

@author: bushnelf
"""

import Card


class SpecialOps(Card.Card):
    """
    Special Ops:  Take 1 VP from each opponent, unless the current board
    has the single most VP.
    """

    def __init__(self):
        Card.Card.__init__(self, "Special Ops", 22)
        self.add_symbol(Card.Card.Symbols[2])
        self.add_symbol(Card.Card.Symbols[4])

    def main_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        currvps = myboard.victorypoints
        # make a list of all boards' VP
        vps = []
        for pb in game.playerboards:
            vps.append(pb.victorypoints)
        vps.sort()
        maxidx = len(vps) - 1
        # if current VPs are not the most, or if there's a tie, get effect
        if currvps != vps[maxidx] or vps[maxidx] == vps[maxidx - 1]:
            for pbidxothers in range(len(game.playerboards)):
                if pbidxothers != pbidx:
                    pbother = game.playerboards[pbidxothers]
                    # make sure other board is not protected
                    if pbother.protected == 0 and pbother.victorypoints > 0:
                        pbother.victorypoints -= 1
                        myboard.victorypoints += 1

if __name__ == '__main__':
    import Game

    so = SpecialOps()
    print("Created " + so.title + " card")
    g = Game.Game(4)
    g.addtocardlist(so)
    g.sendcardlisttoboards()
    g.playerboards[1].readytoplay(so)
    for pbidx in range(len(g.playerboards)):
        g.playerboards[pbidx].victorypoints = 2 * (pbidx % 2)
        print("Board " + str(pbidx) + " has " + str(2 * (pbidx % 2)) + " VPs")
    so.main_effect(g, 1)
    print("This should be 3: " + str(g.playerboards[1].victorypoints))
    for pbidx in range(len(g.playerboards)):
        print("Board " + str(pbidx) + " has " +
              str(g.playerboards[pbidx].victorypoints))
