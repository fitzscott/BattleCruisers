# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 21:48:40 2017

@author: bushnelf
"""

# import Player


class PlayerBoard(object):
    """
    PlayerBoard - where a player's "in play", "recovery zone", and
    discarded cards are kept, along with the player's victory points
    and any special tokens (disabled et al).  Oh, and the player's
    hand.
    """

    def __init__(self, name):
        self._name = name
        # These are all lists of cards.
        self._inplay = []
        self._discards = []
        self._recovery = []
        self._hand = []
        self._redalert = False
        self._disabled = 0
        self._protected = 0
        self._victorypoints = 1    # everyone starts with 1
        self._player = None

    @property
    def inplay(self):
        return self._inplay

    @property
    def discards(self):
        return self._discards

    @property
    def recoveryzone(self):
        return self._recovery

    @property
    def hand(self):
        return self._hand

    @property
    def redalert(self):
        return self._redalert

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val

    @property
    def protected(self):
        return self._protected

    @protected.setter
    def protected(self, val):
        self._protected = val

    @property
    def victorypoints(self):
        return self._victorypoints

    @victorypoints.setter
    def victorypoints(self, val):
        if val < 0:
            val = 0
        self._victorypoints = val

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, val):
        self._player = val

    def readytoplay(self, card):
        """ Move a card from your hand to the "in play" area.
        Not quite the same as playing, since the card is put in the
        "in play" area face down & not revealed till all players
        have placed their chosen card in their respective "in play"
        areas.
        """
        if not self.checklost() and card is not None:
            self.hand.remove(card)
            self.inplay.append(card)

    def endplay(self):
        """ The card in the "in play" area has been played,
        so move it to the "recovery" area.  Make sure this is
        done after the recover step, as we don't want the card
        going directly to the player's hand.
        """
        for card in self.recoveryzone:
            self.hand.append(card)
            self.recoveryzone.remove(card)
        for card in self.inplay:
            self.recoveryzone.append(card)
            self.inplay.remove(card)
        if self.protected > 0:
            self.protected = self.protected - 1
        if self.disabled > 0:
            self.disabled = self.disabled - 1

    def recover(self):
        """ Move the card(s) from the recovery zone to the
        player's hand.
        """
        for card in self.recoveryzone:
            self.hand.append(card)
            self.recoveryzone.remove(card)

    def sendtorecovery(self, card):
        if card is not None:
            self.recoveryzone.append(card)
            self.hand.remove(card)

    def discard(self, card, piledescr):
        """ Discarding may be done from either the hand or the
        recovery zone.
        """
        if card is not None:
            if ("hand" in piledescr) and (card in self.hand):
                self.hand.remove(card)
            elif ("inplay" in piledescr) and (card in self.inplay):
                self.inplay.remove(card)
            elif ("recovery" in piledescr) and (card in self.recoveryzone):
                self.recoveryzone.remove(card)
            else:
                print("Throw an exception here - trying to discard " +
                      card.title)    # to do
            self.discards.append(card)

    def addtohand(self, card):
        self.hand.append(card)

    def checkredalert(self):
        """ If there is only 1 card in the combined piles of
        In Play, Recovery Zone, and Hand, then the board is in
        red alert mode.
        """
        if len(self.hand) + len(self.inplay) + len(self.recoveryzone) == 1:
            self._redalert = True
        return(self._redalert)

    def checklost(self):
        """ No cards except in discard pile => you have lost """
        return (len(self.hand) + len(self.inplay) +
                len(self.recoveryzone) == 0)

    def checkrecoveryforsymbol(self, symbol):
        """ If a card in the recovery zone has a given symbol, return true
        """
        inrec = False
        for card in self.recoveryzone:
            #    for sym in card.symbols:
            #        if sym == symbol:
            if symbol in card.symbols:
                inrec = True
                break
        return(inrec)

    def returndiscardtohand(self, game, pbidx):
        """
        For random computer players, we will just grab a card at random
        and return it to our hand.  For human players, this will be
        more involved, most likely.
        """
        card = self.player.choosecardtoretrievefromdiscard(game, pbidx)
        if card is not None:
            self.hand.append(card)
            self.discards.remove(card)

    def cardbyindex(self, cardidx, deck="hand"):
        card = None
        if cardidx >= 0:
            if deck == "hand":
                card = self.hand[cardidx]
            elif deck == "recovery":
                card = self.recoveryzone[cardidx]
        return(card)

    def printinplay(self):
        retstr = "----  In play:\n"
        for card in self.inplay:
            retstr += card.title + ": " + str(card.rank) + "\n"
        return(retstr)

    def printhand(self):
        retstr = "----  Hand:\n"
        for card in self.hand:
            retstr += card.title + ": " + str(card.rank) + "\n"
        return(retstr)

    def printrecover(self):
        retstr = "----  Recovery Zone:\n"
        for card in self.recoveryzone:
            retstr += card.title + ": " + str(card.rank) + "\n"
        return(retstr)

    def printdiscards(self):
        retstr = "----  Discards:\n"
        for card in self.discards:
            retstr += card.title + ": " + str(card.rank) + "\n"
        return(retstr)

    def __str__(self):
        return("VP: " + str(self.victorypoints) + "\n" + self.printinplay() +
               self.printhand() + self.printrecover() + self.printdiscards())

if __name__ == '__main__':
    import Card

    c1 = Card.Card("Precision Strike", 34)
    c1.add_symbol("Weapons")
    c2 = Card.Card("Shields", 3)
    c3 = Card.Card("Cloaking Device", 4)
    pb = PlayerBoard("Player 1")
    if pb.checklost():
        print("No cards => you lost")
    pb.addtohand(c1)
    if pb.checkredalert():
        print("One card => red alert")
    pb.addtohand(c2)
    pb.addtohand(c3)
    print(pb)
    print("++++++++++++  Playing Precision Strike")
    pb.readytoplay(c1)
    print(pb)
    print("++++++++++++  Ending play / recovering")
    pb.endplay()    # get it in the recovery area
    print(pb)
    if pb.checkrecoveryforsymbol("Weapons"):
        print("Recovery zone has symbol Weapons (expected)")
    if pb.checkrecoveryforsymbol("People"):
        print("Recovery zone has symbol People (NOT expected)")
    print("++++++++++++  Discarding from recovery zone")
    pb.discard(c1, ["recovery"])
    print(pb)
    print("++++++++++++  Playing Shields")
    pb.readytoplay(c2)
    print(pb)
    print("++++++++++++  Ending play / recovering")
    pb.endplay()    # get it in the recovery area
    print(pb)
    print("++++++++++++  Recovering from recovery zone")
    pb.recover()    # get it back in the hand
    print(pb)
    print("++++++++++++  This should fail.")
    try:
        c4 = Card.Card("Evasive Action", 8)
        # This should fail
        pb.readytoplay(c4)
        print(pb)
    except Exception:
        print("Caught exception as expected")
    pb.victorypoints = 5
    print("VP: " + str(pb.victorypoints))
    pb.victorypoints = -1
    print("VP: " + str(pb.victorypoints) + " (should be 0)")
