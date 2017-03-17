# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 20:33:41 2017

@author: bushnelf
"""

import random

import Player


class RandomComputerPlayer(Player.Player):
    """
    RandomComputerPlayer -
    Implement the methods in Player, randomizing all the choices.
    Not the smartest bulb in the chandelier.
    """

    def __init__(self, name):
        Player.Player.__init__(self, name)

    def getmyboard(self, game, myphbidx):
        return game.playerboards[myphbidx]

    def chooserandomcard(self, game, myphbidx, deck):
        """
        Pick a card, any card
        """
        card = None
        mb = self.getmyboard(game, myphbidx)
        pickfrom = []
        if "hand" in deck:
            pickfrom.extend(mb.hand)
        if "recovery" in deck:
            pickfrom.extend(mb.recoveryzone)
        if "inplay" in deck:
            pickfrom.extend(mb.inplay)
        if "discards" in deck:
            pickfrom.extend(mb.discards)

        decksize = len(pickfrom)
        if decksize > 0:
            cardidx = random.randint(0, decksize-1)
            card = pickfrom[cardidx]
        return(card)

    def choosecardtoplay(self, game, myphbidx):
        return(self.chooserandomcard(game, myphbidx, ["hand"]))

    def choosecardtodiscard(self, game, myphbidx, deck):
        return(self.chooserandomcard(game, myphbidx, deck))

    def choosecardtoretrievefromdiscard(self, game, myphbidx):
        return(self.chooserandomcard(game, myphbidx, ["discards"]))

    def choosecardtoremovefromdiscard(self, game, myphbidx):
        return(self.chooserandomcard(game, myphbidx, ["discards"]))

    def choosecardtosendtorecovery(self, game, myphbidx):
        return(self.chooserandomcard(game, myphbidx, ["hand"]))

    def choosecardtoswap(self, game, myphbidx, deck):
        return(self.chooserandomcard(game, myphbidx, deck))

    def choosecardtotake(self, game, myphbidx):
        """ Which card needs this?  """
        pass

    def choosecardtotrade(self, game, myphbidx):
        """ Which card needs this?  """
        pass

    def chooseplayertotakevictoryfrom(self, game, myphbidx):
        """
        Only randomize over the other players that actually
        have VP.  It's random, but not _that_ random.  ;-)
        """

        pbilist = []
        for pbidx in range(len(game.playerboards)):
            if pbidx != myphbidx and \
                    game.playerboards[pbidx].victorypoints > 0:
                pbilist.append(pbidx)
        pbichoice = random.randint(0, len(pbilist))
        return(game.playerboards[pbilist[pbichoice]])

    def choosecardfromplayer(self, game, myphbidx, deck, tgtpbidx):
        pass

    def chooseplayertotakecardfrom(self, game, myphbidx, deck="hand"):
        """
        Only randomize over the other players that actually
        have cards in appropriate deck.
        """
        # This needs to be re-written
        tgtpblist = []
        plidx = -1
        for pbidx in game.playerboards:  # s/b range(len...)
            if pbidx != myphbidx:
                tgtboard = game.playerboards[pbidx]
                if deck == "hand":
                    pickfrom = tgtboard.hand
                elif deck == "recovery":
                    pickfrom = tgtboard.recoveryzone
                elif deck == "inplay":
                    pickfrom = tgtboard.inplay
                elif deck == "discards":
                    pickfrom = tgtboard.discards
                if len(pickfrom) > 0:
                    tgtpblist.append(pbidx)
        tgtlistsize = len(tgtpblist)
        if tgtlistsize > 0:
            plidx = random.randint(0, tgtlistsize-1)
        return(plidx)

    def chooseeffecttoignore(self, game, myphbidx):
        pass

if __name__ == '__main__':
    import Game
    import CardSet

    g = Game.Game(3)
    for rcpi in range(3):
        rcp = RandomComputerPlayer("Random Player " + str(rcpi+1))
        g.playerboards[rcpi].player = rcp
    cs = CardSet.CardSet(3)
    g.cardlist = cs.getcardset()
    g.sendcardlisttoboards()
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
