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

    @property
    def name(self):
        return(self._name)

    def getmyboard(self, game, myphbidx):
        return game.playerboards[myphbidx]

    def combinedecks(self, tgtboard, deck):
        pickfrom = []
        if "hand" in deck:
            pickfrom.extend(tgtboard.hand)
        elif "recovery" in deck:
            pickfrom.extend(tgtboard.recoveryzone)
        elif "inplay" in deck:
            pickfrom.extend(tgtboard.inplay)
        elif "discards" in deck:
            pickfrom.extend(tgtboard.discards)
        return(pickfrom)

    def choosecardtoplay(self, game, myphbidx):
        """
        Pick a card from your hand to play
        """
        pass

    def choosecardtodiscard(self, game, myphbidx, deck):
        pass

    def choosecardtoretrievefromdiscard(self, game, myphbidx):
        pass

    def choosecardtoremovefromdiscard(self, game, myphbidx):
        pass

    def choosecardtosendtorecovery(self, game, myphbidx):
        pass

    def choosecardtoswap(self, game, myphbidx, deck):
        pass

    def choosecardtotake(self, game, myphbidx):
        pass

    def choosecardtotrade(self, game, myphbidx):
        pass

    def choosecardfromplayer(self, game, myphbidx, deck, tgtpbidx):
        pass

    def chooseplayertotakevictoryfrom(self, game, myphbidx):
        pass

    def chooseplayertodisable(self, game, myphbidx, deck):
        pass

    def chooseplayertotakecardfrom(self, game, myphbidx, deck):
        pass

    def chooseeffecttoignore(self, game, myphbidx):
        pass
