# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 20:14:25 2017

@author: bushnelf
"""

import sys
import Player


class SimpleHumanPlayer(Player.Player):
    """
    SimpleHumanPlayer - present choices the player must make to
    the terminal, then collect feedback to pass back to
    calling routine.
    """

    def __init__(self, name):
        Player.Player.__init__(self, name)

    @property
    def name(self):
        return(self._name)

    def choosecard(self, game, phbidx, deck):
        """
        Pick a card, any card
        """
        card = None
        mb = self.getmyboard(game, phbidx)
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
            for cidx in range(decksize):
                print("    " + str(cidx) + ") " + pickfrom[cidx].title +
                      " (rank " + str(pickfrom[cidx].rank) + ")")
            # gather input here
            chosenidx = input("!!  Choose a card by number (higher if none):")
            if chosenidx < decksize:
                card = pickfrom[chosenidx]
        return(card)

    def choosecardtoplay(self, game, myphbidx):
        """
        Pick a card from your hand to play
        """
        print(self.name + ", choose a card to play:")
        return(self.choosecard(game, myphbidx, ["hand"]))

    def choosecardtodiscard(self, game, myphbidx, deck):
        print(self.name + ", choose a card to discard:")
        return(self.choosecard(game, myphbidx, deck))

    def choosecardtoretrievefromdiscard(self, game, myphbidx):
        print(self.name + ", choose a card to retrieve from discards:")
        return(self.choosecard(game, myphbidx, ["discards"]))

    def choosecardtoremovefromdiscard(self, game, myphbidx):
        print(self.name + ", choose a card to remove from discards:")
        return(self.choosecard(game, myphbidx, ["discards"]))

    def choosecardtosendtorecovery(self, game, myphbidx):
        print(self.name + ", choose a card to send to recovery:")
        return(self.choosecard(game, myphbidx, ["hand"]))

    def choosecardtoswap(self, game, myphbidx, deck):
        print(self.name + ", choose cards to swap:")
        return(self.choosecard(game, myphbidx, deck))

    def choosecardtogiveaway(self, game, myphbidx, deck):
        print("..... " + self.name + " choosing card to give away")
        return(self.choosecard(game, myphbidx, deck))

    def choosecardtotrade(self, game, myphbidx, deck):
        print("..... " + self.name + " choosing card to trade")
        return(self.choosecard(game, myphbidx, deck))

    def choosecardtotake(self, game, myphbidx):
        pass

    def randomcardfromplayer(self, game, myphbidx, deck, tgtpbidx):
        return(self.chooserandomcard(game, tgtpbidx, deck))

    def choosecardfromplayer(self, game, myphbidx, deck, tgtpbidx):
        # Pass in the target player's board instead of our own.
        return(self.choosecard(game, tgtpbidx, deck))

    def choosecardbyname(self, game, myphbidx):
        optnum = 0
        for card in game.cardlist:
            print(str(optnum) + ") " + card.title + ", rank " + str(card.rank))
            optnum += 1
        cidx = input("!!  Choose a card by option number:")
        return(game.cardlist[cidx])

    def chooseplayertotakevictoryfrom(self, game, myphbidx):
        print(self.name + ", choose a player to take VP from:")
        pbilist = []
        optnum = 0
        chosenpb = None
        print(self.name + ", other players to choose from:")
        for pbidx in range(len(game.playerboards)):
            thispb = game.playerboards[pbidx]
            if pbidx != myphbidx and thispb.victorypoints > 0 \
                    and thispb.protected == 0 and \
                    not thispb.ignore_main_effect(game, myphbidx,
                                                  ["vp_theft"]):
                pbilist.append(pbidx)
                print("    " + str(optnum) + ")  " + thispb.player.name +
                      " (VP: " + str(thispb.victorypoints) + ")")
                optnum += 1
        if len(pbilist) > 0:
            chosenidx = input("!!  Choose another player by number:")
            chosenpb = game.playerboards[pbilist[chosenidx]]
        else:
            chosenpb = None
        return(chosenpb)

    def chooseplayertotakecardfrom(self, game, myphbidx, deck):
        print(self.name + ", choose a player to take a card from:")
        tgtpblist = []
        plidx = None
        optnum = 0
        for pbidx in range(len(game.playerboards)):
            if pbidx != myphbidx:
                tgtboard = game.playerboards[pbidx]
                if tgtboard.protected == 0 and not \
                        tgtboard.ignore_main_effect(game, myphbidx,
                                                    ["card_theft"]):
                    pickfrom = self.combinedecks(tgtboard, deck)
                else:
                    pickfrom = []
                if len(pickfrom) > 0:
                    tgtpblist.append(pbidx)
                    print(str(optnum) + ") " + tgtboard.player.name + ":")
                    for card in pickfrom:
                        print("-> " + card.title + " (" + str(card.rank) + ")")
                    optnum += 1
        tgtlistsize = len(tgtpblist)
        # print("Target list for " + str(deck) + " is " + str(tgtpblist))
        if tgtlistsize > 0:
            chosenplidx = input("!!  Choose another player by number: ")
            plidx = tgtpblist[chosenplidx]

        return(plidx)

    def chooseplayertodisable(self, game, myphbidx):
        print(self.name + ", choose a player to disable:")
        tgtpblist = []
        optnum = 0
        plidx = None
        for pbidx in range(len(game.playerboards)):
            pb = game.playerboards[pbidx]
            if pbidx != myphbidx and pb.disabled == 0 and \
                    pb.protected == 0 and not \
                    pb.ignore_main_effect(game, myphbidx, ["disable"]):
                tgtpblist.append(pbidx)
                print("    " + str(optnum) + ")  " + pb.player.name)
                optnum += 1
        tgtlistsize = len(tgtpblist)
        print("Disable list is " + str(tgtpblist))
        if tgtlistsize > 0:
            chosenplidx = input("!!  Choose another player by number: ")
            plidx = tgtpblist[chosenplidx]
        return(plidx)

    # This is essentially similar to chooseplayertotakecardfrom. Fix.
    def chooseplayertodiscard(self, game, myphbidx, deck=["hand", "recover"]):
        print(self.name + ", choose a player to discard:")
        tgtpblist = []
        plidx = None
        optnum = 0
        for pbidx in range(len(game.playerboards)):
            if pbidx != myphbidx:
                tgtboard = game.playerboards[pbidx]
                if tgtboard.protected == 0 and not \
                        tgtboard.ignore_main_effect(game, myphbidx,
                                                    ["card_discard"]):
                    pickfrom = self.combinedecks(tgtboard, deck)
                else:
                    pickfrom = []
                if len(pickfrom) > 0:
                    tgtpblist.append(pbidx)
                    print(str(optnum) + ") " + tgtboard.player.name + ":")
                    for card in pickfrom:
                        print("-> " + card.title + " (" + str(card.rank) + ")")
                    optnum += 1
        tgtlistsize = len(tgtpblist)
        # print("Target list for " + str(deck) + " is " + str(tgtpblist))
        if tgtlistsize > 0:
            chosenplidx = input("!!  Choose another player by number: ")
            plidx = tgtpblist[chosenplidx]

        return(plidx)

    def chooseeffecttoignore(self, game, myphbidx, card):
        tgtranklist = []
        fxrank = -1
        optnum = 0
        for pbidx in range(len(game.playerboards)):
            pb = game.playerboards[pbidx]
            if pbidx != myphbidx:
                if len(pb.inplay) > 0 and card.rank < pb.inplay[0].rank:
                    tgtranklist.append(pb.inplay[0].rank)
                    print("    " + str(optnum) + ")  " + pb.inplay[0].title)
                    optnum += 1
        tgtlistsize = len(tgtranklist)
        print("Effects list is " + str(tgtranklist))
        if tgtlistsize > 0:
            chosenfxidx = input("!!  Choose effect by number: ")
            fxrank = tgtranklist[chosenfxidx]
        return(fxrank)

    def chooserankingforcards(self, game, myphbidx):
        # scramble the rankings of cards after my card
        realrankpb = game.getcardstoplay()
        rankset = set([])        # just want the unique ranks
        for (rank, pb) in realrankpb:
            if (pb != myphbidx):
                rankset.add(rank)
        effranks = list(rankset)
        print("rankset = " + str(rankset) + ", eff = " + str(effranks))
        rcnt = len(effranks)
        print("rcnt = " + str(rcnt))
        # get the full card list, so we'll have descriptions for cards
        optnum = 0
        optranks = []
        neworder = None
        for card in game.cardlist:
            if card.rank in effranks:
                print("    " + str(optnum) + ") " + str(card))
                optranks.append(card.rank)
                optnum += 1
        if optnum > 0:
            print("!!  Choose new ordering by option number: ")
            chosenorder = sys.stdin.readline().strip().split()
            neworder = [int(co) for co in chosenorder]
        # now produce a mapping from real rank to effective rank
        realeffmap = {}
        if neworder is not None:
            idx = 0
            for newidx in neworder:
                realeffmap[effranks[newidx]] = effranks[idx]
                idx += 1
            print("Real: effective rank map: " + str(realeffmap))
        return(realeffmap)

if __name__ == '__main__':
    import Game
    import Card

    g = Game.Game(1)
    shp = SimpleHumanPlayer("George")
    g.playerboards[0].player = shp
    for i in range(5):
        c = Card.Card("Some card " + str(i), 10+i)
        g.addtocardlist(c)
    g.sendcardlisttoboards()
    # shp.choosecardtoplay(g, 0)
    c = shp.choosecard(g, 0, ["hand", "recovery"])
    print("You picked " + c.title)
