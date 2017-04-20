# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 20:03:14 2017

@author: bushnelf
"""

import Card
import PlayerBoard


class Game(object):
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
        self._numclashes = 0
        for pbidx in range(numplayers):
            pb = PlayerBoard.PlayerBoard("Player " + str(pbidx + 1))
            self._playerboards.append(pb)
        self._cardbeingplayed = None

    @property
    def playerboards(self):
        return(self._playerboards)

    @property
    def cardlist(self):
        return(self._cardlist)

    @cardlist.setter
    def cardlist(self, val):
        self._cardlist = val

    @property
    def numclashes(self):
        return(self._numclashes)

    @numclashes.setter
    def numclashes(self, val):
        self._numclashes = val

    @property
    def cardbeingplayed(self):
        return(self._cardbeingplayed)

    @cardbeingplayed.setter
    def cardbeingplayed(self, val):
        self._cardbeingplayed = val

    def addtocardlist(self, card):
        self._cardlist.append(card)

    def sendcardlisttoboards(self):
        for pbidx in range(self._numplayers):
            for cardidx in range(len(self._cardlist)):
                self.playerboards[pbidx].addtohand(self.cardlist[cardidx])

    def revisedcardranking(self):
        rvsd = False
        for card in self.cardlist:
            if card.effectiverank is not None:
                rvsd = True
                break
        return(rvsd)

    def getcardstoplay(self):
        cardstoplay = []
        for pbidx in range(self._numplayers):
            pb = self.playerboards[pbidx]
            # skip disabled player boards
            if pb.disabled == 2:
                continue
            if len(pb.inplay) > 0:
                cardstoplay.append((pb.inplay[0].rank, pbidx))
                # print("gctp: player " + str(pbidx) + " has a card to play.")
        cardstoplay.sort()
        return(cardstoplay)

    def cardslefttoplay(self, lastrank=0):
        # print("last rank is " + str(lastrank))
        cardstoplay = self.getcardstoplay()
        # print("ctp: " + str(cardstoplay))
        if lastrank == 0:
            stidx = 0
            # print("stidx is 0")
        else:
            stidx = None
            for cidx in range(len(cardstoplay)-1):
                (rank, pbidx) = cardstoplay[cidx]
                if rank == lastrank:
                    stidx = cidx + 1
                    # We are not going to break here, because the same card
                    # can appear more than once.  We want next card after the
                    # last instance of the same card.
            # Make sure we aren't past the end of the playable cards
            if stidx is not None and stidx < len(cardstoplay) and \
                    cardstoplay[stidx][0] == lastrank:
                stidx = None
        if stidx is not None:
            return(cardstoplay[stidx:])
        else:
            return(None)

    def checkfordupes(self, cardstoplay):
        carddupes = {}
        self.numclashes = 0
        for (cardrank, pbidx) in cardstoplay:
            # print("Card rank: " + str(cardrank) + " for player " +
            #      str(pbidx))
            if cardrank in carddupes:
                if carddupes[cardrank] != "dupe":
                    self.numclashes = 2
                else:
                    self.numclashes += 1
                carddupes[cardrank] = "dupe"
            else:
                carddupes[cardrank] = "single"
        print("Card dupes: " + str(carddupes))
        return(carddupes)

    def playcards(self):
        """
        Revised version of playallcards, taking into account ranking changes
        that can occur for a particular card.
        """
        cardstoplay = self.cardslefttoplay()
        while cardstoplay is not None:
            carddupes = self.checkfordupes(cardstoplay)
            # produce a list of remaining card ranks
            rankset = set([])
            for (cardrank, pbidx) in cardstoplay:
                rankset.add(cardrank)
            # print("rankset is " + str(rankset))
            ranks = list(rankset)
            ranks.sort()
            # print("ranks is " + str(ranks))
            for (cardrank, pbidx) in cardstoplay:
                # print("Rank " + str(cardrank) + ", player " + str(pbidx))
                # Only run the top-ranked card; later ranks will run in
                # subsequent iterations & calls to cardsleftoplay.
                if cardrank != ranks[0]:
                    continue
                currboard = self.playerboards[pbidx]
                card = currboard.inplay[0]
                if currboard.disabled != 2:    # 2 => disabled this round
                    if currboard.player is not None:
                        plnm = currboard.player.name
                    else:
                        plnm = "Nohbody"
                    print(plnm + " playing " + str(card.rank) + " : " +
                          card.title)
                    # cards might have been pulled out of the duplicate list
                    # in checkfordupes.  If one is gone, do not play it.
                    # To do:  This might not ever occur any more - check.
                    if cardrank not in carddupes:
                        continue
                    self.cardbeingplayed = card
                    if carddupes[cardrank] == "single":
                        card.main_effect(self, pbidx)
                        # if we are doubling a play, and the same card is still
                        # in play, run it again.
                        if len(currboard.inplay) > 0 and \
                                currboard.inplay[0] == card and \
                                currboard.doubleplay == 1:
                            print("Double play on " + card.title)
                            card.main_effect(self, pbidx)
                    else:
                        card.clash_effect(self, pbidx)
                # If board is disabled, move its in-play card to the RZ
                elif not currboard.checkredalert():
                    currboard.recoveryzone.append(card)
                    currboard.inplay.remove(card)
            if len(ranks) > 0:
                cardstoplay = self.cardslefttoplay(ranks[0])
            else:
                cardstoplay = None

    def playallcards(self):
        # backward compatibility (i.e, I am lazy)
        self.playcards()

#    def playallcards(self):
#        """
#        Create a tuple for each playerboard's card in play,
#        put them all in a list, and sort them.
#        Then determine whether there are duplicates & evaluate
#        each card.
#        """
#
#        cardstoplay = self.getcardstoplay()
#        # print(cardstoplay)
#        # Determine duplicates, if any, in chosen cards
#        carddupes = self.checkfordupes(cardstoplay)
#        lastcardrank = -1
#        for (cardrank, pbidx) in cardstoplay:
#            # It's possible that a card in play at the beginning of a
#            # turn will have been discarded before it gets played.
#            currboard = self.playerboards[pbidx]
#            if len(currboard.inplay) > 0:
#                card = currboard.inplay[0]
#                if currboard.disabled != 2:    # 2 => disabled this round
#                    if currboard.player is not None:
#                        plnm = currboard.player.name
#                    else:
#                        plnm = "Nohbody"
#                    print(plnm + " playing " + str(card.rank) + " : " +
#                          card.title)
#                    # re-evaluate duplicates, as disabling or removing could
#                    # change what is duplicated.
#                    # Only do this if we have changed cards, though.  If we
#                    # are in the middle of playing, e.g., Reckless Pilot,
#                    # having player 1 discard RP does not mean that player 2's
#                    # RP is no longer a duplicate.
#                    if cardrank != lastcardrank and lastcardrank != -1:
#                        print("    end of turn comparing card ranks " +
#                              str(cardrank) + " vs. " + str(lastcardrank))
#                        newcardstoplay = self.getcardstoplay()
#                        carddupes = self.checkfordupes(newcardstoplay)
#                    lastcardrank = cardrank
#                    # cards might have been pulled out of the duplicate list
#                    # in checkfordupes.  If one is gone, do not play it.
#                    if cardrank not in carddupes:
#                        continue
#                    self.cardbeingplayed = card
#                    if carddupes[cardrank] == "single":
#                        card.main_effect(self, pbidx)
#                    else:
#                        card.clash_effect(self, pbidx)
#                # If board is disabled, move its in-play card to the RZ
#                elif not currboard.checkredalert():
#                    currboard.recoveryzone.append(card)
#                    currboard.inplay.remove(card)

    def checkgameover(self, players_win_vp, players_left):
        gameover = False
        if len(players_win_vp) >= 1:
            players_win_vp.sort(reverse=True)
            print(players_win_vp)
            if len(players_win_vp) == 1:
                winner = self.playerboards[players_win_vp[0][3]]
            else:
                p1 = self.playerboards[players_win_vp[0][3]]
                p2 = self.playerboards[players_win_vp[1][3]]
                if p1.victorypoints > p2.victorypoints or \
                    len(p1.hand) > len(p2.hand) or \
                        p1.handresoltot() > p2.handresoltot():
                    winner = p1
                else:
                    winner = None
            if winner is not None:
                print("Player " + winner.player.name +
                      " is the victorious winner!")
            else:
                print("We have a tie...  play again.")
            gameover = True
        elif players_left == 1:
            # print("We have a surviving winner!")
            for pb in self.playerboards:
                if not pb.checklost():
                    print("Player " + pb.player.name +
                          " is the surviving winner!")
            gameover = True
        elif players_left == 0:
            print("All players have failed to survive.")
            gameover = True
        return(gameover)

    def endturn(self):
        cardstoplay = self.getcardstoplay()
        for (cardrank, pbidx) in cardstoplay:
            if self.playerboards[pbidx].disabled != 2:
                self.playerboards[pbidx].inplay[0].end_of_turn_effect(self,
                                                                      pbidx)
        # In case a card changed the cards' ranking, reset it
        for card in self.cardlist:
            card.effectiverank = None
        players_left = len(self.playerboards)
        players_win_vp = []
        for pbi in range(len(self.playerboards)):
            pb = self.playerboards[pbi]
            pb.endplay()
            # endplay calls checkredalert, so don't need this
            # pb.checkredalert()
            if pb.checklost():
                players_left -= 1
            elif pb.victorypoints >= 15:
                players_win_vp.append((pb.victorypoints, len(pb.hand),
                                      pb.handresoltot(), pbi))
        gameover = self.checkgameover(players_win_vp, players_left)
        return(gameover)


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
    g.endturn()
    # test a tie
    for idx in range(4):
        pb = g.playerboards[idx]
        pb.victorypoints = 15
        print(pb)
    g.endturn()
