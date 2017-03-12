# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 20:03:14 2017

@author: bushnelf
"""

import Card
import PlayerBoard


class Game:
    """
    Game class:
    1)  Set up the player boards and allocate sets of cards
    to each board.
    2)  Associate each PlayerBoard with a Player.
    3)  Instruct each player to pick a card to play.
    4)  Determine turn order.
    5)  Determine clashes.
    6)  Call each PlayerBoard's appropriate function.
    """

    def __init__(self, numplayers):
        self._numplayers = numplayers
        self._cardlist = []
        self._playerboards = []
        for pbidx in range(numplayers):
            pb = PlayerBoard.PlayerBoard("Player " + str(pbidx + 1))
            self._playerboards.append(pb)

    @property
    def playerboards(self):
        return(self._playerboards)

    @property
    def cardlist(self):
        return(self._cardlist)

    def addtocardlist(self, card):
        self._cardlist.append(card)

    def sendcardlisttoboards(self):
        for pbidx in range(self._numplayers):
            for cardidx in range(len(self._cardlist)):
                self.playerboards[pbidx].addtohand(self.cardlist[cardidx])

    def playallcards(self):
        """
        Create a tuple for each playerboard's card in play,
        put them all in a list, and sort them.
        Then determine whether there are duplicates & evaluate
        each card.
        """
        cardstoplay = []
        for pbidx in range(self._numplayers):
            cardstoplay.append((self.playerboards[pbidx].inplay[0].rank,
                                pbidx))
        cardstoplay.sort()
        # print(cardstoplay)
        # Determine duplicates, if any, in chosen cards
        carddupes = {}
        for (cardrank, pbidx) in cardstoplay:
            # print("Card rank: " + str(cardrank) + " for player " +
            #      str(pbidx))
            if cardrank in carddupes:
                carddupes[cardrank] = "dupe"
            else:
                carddupes[cardrank] = "single"
        for (cardrank, pbidx) in cardstoplay:
            if self.playerboards[pbidx].disabled == 0:
                if carddupes[cardrank] == "single":
                    self.playerboards[pbidx].inplay[0].main_effect(self,
                                                                   pbidx)
                else:
                    self.playerboards[pbidx].inplay[0].clash_effect(self,
                                                                    pbidx)

    def endturn(self):
        pass

if __name__ == '__main__':
    c1 = Card.Card("Not a Card", 1)
    c2 = Card.Card("Not Really a Card", 2)
    c3 = Card.Card("Not Really a Card Either", 3)
    c4 = Card.Card("Still Not Really a Card", 4)
    g = Game(4)
    g.addtocardlist(c1)
    g.addtocardlist(c2)
    g.addtocardlist(c3)
    g.addtocardlist(c4)
    # This isn't enough cards for a real hand, but...
    g.sendcardlisttoboards()
    g.playerboards[0].readytoplay(c4)
    g.playerboards[1].readytoplay(c4)       # induce a clash
    g.playerboards[2].readytoplay(c2)
    g.playerboards[3].readytoplay(c3)
    g.playallcards()
