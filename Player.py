# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 21:11:07 2017

@author: bushnelf
"""

import random

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
        if "recovery" in deck:
            pickfrom.extend(tgtboard.recoveryzone)
        if "inplay" in deck:
            pickfrom.extend(tgtboard.inplay)
        if "discards" in deck:
            pickfrom.extend(tgtboard.discards)
        return(pickfrom)

    def chooserandomcard(self, game, phbidx, deck):
        """
        Pick a card, any card
        """
        card = None
        # mb = self.getmyboard(game, myphbidx)
        mb = game.playerboards[phbidx]
        print("Choosing card from player " + mb.player.name)
        pickfrom = self.combinedecks(mb, deck)
        decksize = len(pickfrom)
        if decksize > 0:
            cardidx = random.randint(0, decksize-1)
            card = pickfrom[cardidx]
            print(self.name + " picked " + card.title + " from " + str(deck))
        return(card)

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

    def choosecardtogiveaway(self, game, myphbidx, deck):
        pass

    def choosecardtotrade(self, game, myphbidx, deck):
        pass

    def choosecardfromplayer(self, game, myphbidx, deck, tgtpbidx):
        pass

    def choosecardbyname(self, game, myphbidx):
        pass

    def randomcardfromplayer(self, game, myphbidx, deck, tgtpbidx):
        pass

    def chooseplayertotakevictoryfrom(self, game, myphbidx):
        pass

    def chooseplayertodisable(self, game, myphbidx, deck):
        pass

    def chooseplayertotakecardfrom(self, game, myphbidx, deck):
        pass

    def chooseplayertodiscard(self, game, myphbidx, deck):
        pass

    def chooseeffecttoignore(self, game, myphbidx, card):
        pass
