# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 21:11:07 2017

@author: bushnelf
"""

# import PlayerBoard
# import Game


class Player(object):
    """Player - do all the decision-making that a player would do,
    e.g. pick a card to play, pick a card to discard, pick a
    player to take victory points from, etc.
    """

    def __init__(self, name):
        self._name = name

    def getmyboard(self, game, myphbidx):
        return game.playerboards[myphbidx]

    def choosecardtoplay(self, game, myphbidx):
        pass

    def choosecardtodiscard(self, game, myphbidx, deck="hand"):
        pass

    def choosecardtoretrievefromdiscard(self, game, myphbidx):
        pass

    def choosecardtoremovefromdiscard(self, game, myphbidx):
        pass

    def choosecardtoswap(self, game, myphbidx, deck="hand"):
        pass

    def choosecardtotake(self, game, myphbidx):
        pass

    def choosecardtotrade(self, game, myphbidx):
        pass

    def chooseplayertotakevictoryfrom(self, game, myphbidx):
        pass

    def chooseplayertotakecardfrom(self, game, myphbidx, deck="hand"):
        pass

    def chooseeffecttoignore(self, game, myphbidx):
        pass
