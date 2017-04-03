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
    Not the brightest bulb in the chandelier.
    """

    def __init__(self, name):
        Player.Player.__init__(self, name)

    def getmyboard(self, game, myphbidx):
        return game.playerboards[myphbidx]

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
        return(self.chooserandomcard(game, myphbidx, ["hand"]))

    def choosecardtodiscard(self, game, myphbidx, deck):
        print("..... " + self.name + " choosing card to discard")
        return(self.chooserandomcard(game, myphbidx, deck))

    def choosecardtoretrievefromdiscard(self, game, myphbidx):
        print("..... " + self.name + " choosing card to retrieve from discard")
        return(self.chooserandomcard(game, myphbidx, ["discards"]))

    def choosecardtoremovefromdiscard(self, game, myphbidx):
        print("..... " + self.name + " choosing card to remove from discard")
        return(self.chooserandomcard(game, myphbidx, ["discards"]))

    def choosecardtosendtorecovery(self, game, myphbidx):
        print("..... " + self.name + " choosing card to send to recovery")
        return(self.chooserandomcard(game, myphbidx, ["hand"]))

    def choosecardtoswap(self, game, myphbidx, deck):
        print("..... " + self.name + " choosing card to swap")
        # This is a kludge - do not allow a swap for the same card
        myboard = game.playerboards[myphbidx]
        currcard = myboard.inplay[0]    # this must exist
        # You get 20 chances
        for itr in range(20):
            swapcard = self.chooserandomcard(game, myphbidx, deck)
            if swapcard is not None and swapcard.rank != currcard.rank:
                break
            else:
                swapcard = None
        return(swapcard)

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
            thispb = game.playerboards[pbidx]
            if pbidx != myphbidx and thispb.victorypoints > 0 and \
                    thispb.protected == 0:
                pbilist.append(pbidx)
        if len(pbilist) > 0:
            pbichoice = random.randint(0, len(pbilist)-1)
            tgtpb = game.playerboards[pbilist[pbichoice]]
        else:
            tgtpb = None
        return(tgtpb)

    def choosecardfromplayer(self, game, myphbidx, deck, tgtpbidx):
        # Note that this uses the target player index
        return(self.chooserandomcard(game, tgtpbidx, deck))

    def chooseplayertotakecardfrom(self, game, myphbidx, deck=["hand"]):
        """
        Only randomize over the other players that actually
        have cards in appropriate deck.
        """
        tgtpblist = []
        plidx = -1
        for pbidx in range(len(game.playerboards)):
            if pbidx != myphbidx:
                tgtboard = game.playerboards[pbidx]
                pickfrom = []
                if tgtboard.protected != 0:
                    continue
                # it isn't strictly necessary to have a card list, as we
                # could just sum up the sizes of decks to pick from, but
                # I want to check that it is working correctly.
                pickfrom = self.combinedecks(tgtboard, deck)
                if len(pickfrom) > 0:
                    tgtpblist.append(pbidx)
                    print("Target cards for " + self.name + " from " +
                          tgtboard.player.name + ":")
                    for card in pickfrom:
                        print("-> " + card.title + " (" + str(card.rank) + ")")
        tgtlistsize = len(tgtpblist)
        print("Steal card list for " + str(deck) + " is " + str(tgtpblist))
        if tgtlistsize > 0:
            chosenplidx = random.randint(0, tgtlistsize-1)
            plidx = tgtpblist[chosenplidx]
        return(plidx)

    def chooseplayertodisable(self, game, myphbidx):
        tgtpblist = []
        plidx = -1
        for pbidx in range(len(game.playerboards)):
            pb = game.playerboards[pbidx]
            if pbidx != myphbidx and pb.disabled == 0 and pb.protected == 0:
                tgtpblist.append(pbidx)
        tgtlistsize = len(tgtpblist)
        print("Disable list is " + str(tgtpblist))
        if tgtlistsize > 0:
            chosenplidx = random.randint(0, tgtlistsize-1)
            plidx = tgtpblist[chosenplidx]
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
