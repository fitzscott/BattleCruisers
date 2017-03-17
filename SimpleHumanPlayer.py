# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 20:14:25 2017

@author: bushnelf
"""

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

    def choosecard(self, game, myphbidx, deck):
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
            for cidx in range(decksize):
                print("    " + str(cidx) + ") " + pickfrom[cidx].title +
                      " (rank " + str(pickfrom[cidx].rank) + ")")
            # gather input here
            chosenidx = input("!!  Choose a card by number:")
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

    def choosecardtotake(self, game, myphbidx):
        pass

    def choosecardtotrade(self, game, myphbidx):
        pass

    def chooseplayertotakevictoryfrom(self, game, myphbidx):
        print(self.name + ", choose a player to take VP from:")
        pbilist = []
        pbiidx = 0
        print(self.name + ", other players to choose from:")
        for pbidx in range(len(game.playerboards)):
            thispb = game.playerboards[pbidx]
            if pbidx != myphbidx and thispb.victorypoints > 0:
                pbilist.append(pbidx)
                print("    " + str(pbiidx) + ")  " + thispb.player.name +
                      " (VP: " + str(thispb.victorypoints) + ")")
        chosenidx = input("!!  Choose another player by number:")
        return(game.playerboards[pbilist[chosenidx]])

    def choosecardfromplayer(self, game, myphbidx, deck, tgtpbidx):
        pass

    def chooseplayertotakecardfrom(self, game, myphbidx, deck):
        print(self.name + ", choose a player to take VP from:")
        print("    (Doesn't work yet)")
        tgtpblist = []
        plidx = -1
        for pbidx in range(len(game.playerboards)):
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
                    print("    " + str(pbidx) + tgtboard.player.name)
                    print(pickfrom)
        print("Get some input here")        # to do
        return(plidx)

    def chooseeffecttoignore(self, game, myphbidx):
        pass

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