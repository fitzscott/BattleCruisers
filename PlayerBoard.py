# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 21:48:40 2017

@author: bushnelf
"""

import random

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
        self._last_round_card = None
        self._vp_lost_this_round = 0

    @property
    def inplay(self):
        return self._inplay

    @property
    def discards(self):
        return self._discards

    @property
    def recoveryzone(self):
        if self.checkredalert():
            return self._inplay
        else:
            return self._recovery

    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, val):
        self._hand = val

    @property
    def redalert(self):
        return self._redalert

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        if val < 0:
            val = 0
        self._disabled = val

    @property
    def protected(self):
        return self._protected

    @protected.setter
    def protected(self, val):
        if val < 0:
            val = 0
        self._protected = val

    @property
    def victorypoints(self):
        return self._victorypoints

    @victorypoints.setter
    def victorypoints(self, val):
        if val < 0:
            val = 0
        if val < self._victorypoints:
            self.vp_lost_this_round += self._victorypoints - val
        self._victorypoints = val

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, val):
        self._player = val

    # To do:  last round's card can have a continuing effect, so
    # keep track of it, and implement methods to handle it in the
    # individual card classes.
    @property
    def lastroundcard(self):
        return(self._last_round_card)

    @lastroundcard.setter
    def lastroundcard(self, val):
        self._last_round_card = val

    @property
    def vp_lost_this_round(self):
        return self._vp_lost_this_round

    @vp_lost_this_round.setter
    def vp_lost_this_round(self, val):
        self._vp_lost_this_round = val

    def defense(self, game, pbidx, effect):
        """
        Check whether the card in play or from last round have a defense
        against opponents' attacks.
        effect:  main_effect, vp_theft, card_discard, card_theft
        """
        defense = False
        if len(self.inplay) > 0:
            defense = self.inplay[0].defense(game, pbidx, effect, "this")
        if not defense:   # if we've already established a defense, we're done
            if self.lastroundcard is not None:
                defense = \
                    self.lastroundcard.defense(game, pbidx, effect, "last")
        if self.player is not None:
            plnm = self.player.name
        else:
            plnm = "Nohbody"
        print("Player " + plnm + " defense is " + str(defense))
        return(defense)

    def ignore_main_effect(self, game, attkpbidx, addl_fx):
        fx = ["main_effect"]
        if addl_fx is not None:
            fx.extend(addl_fx)
        return(self.defense(game, attkpbidx, fx))

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
        if self.checklost():
            if self.player is None:
                plnm = "Nohbody"
            else:
                plnm = self.player.name
            print("Player " + plnm + " lost!")
            self.victorypoints = 0
        elif self.checkredalert():
            if len(self._hand) == 0:
                lastcard = self.inplay[0]
                self.hand.append(lastcard)
                self.inplay.remove(lastcard)
        else:
            if len(self.inplay) == 0:
                self.lastroundcard = None
            for card in self.recoveryzone:
                self.hand.append(card)
                self.recoveryzone.remove(card)
            for card in self.inplay:
                self.lastroundcard = card
                self.recoveryzone.append(card)
                self.inplay.remove(card)
        self.protected -= 1
        self.disabled -= 1
        self.vp_lost_this_round = 0

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
            if self.player is None:
                plynm = "Nohbody"
            else:
                plynm = self.player.name
            print(plynm + " discarding " + card.title)
            # First, check if we have a redirect for discards
            if len(self.inplay) == 0 or len(self.inplay) > 0 and not \
                    self.inplay[0].redirect(self, "discard"):
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
        self._hand.append(card)

    def checkredalert(self):
        """ If there is only 1 card in the combined piles of
        In Play, Recovery Zone, and Hand, then the board is in
        red alert mode.
        """
        # Want to use hidden fields instead of properties, since
        # hand & recovery properties mutate when only one card
        # is left (i.e. board is in red alert state).
        totalcards = len(self._hand) + len(self._inplay) \
            + len(self._recovery)
        if totalcards == 1:
            self._redalert = True
            if len(self._recovery) > 0:
                # can be only one - ship to inplay
                card = self._recovery[0]
                self._inplay.append(card)
                self._recovery.remove(card)
                print("Red Alert " + self.player.name + "-> recovery 2 play")
        elif totalcards > 1:
            # This covers "recovering" from red alert - back to normal
            self._redalert = False
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

    def removerandomcardfromgame(self, game, pbidx, deck):
        """
        Remove the specified card from the specified deck and do
        not place it anywhere else.
        """
        # Might re-work this later to allow multiple entries in deck.
        # Not clear it's needed.
        if "hand" in deck:
            pickfrom = self.hand
        elif "recovery" in deck:
            pickfrom = self.recoveryzone
        elif "inplay" in deck:
            pickfrom = self.inplay
        elif "discards" in deck:
            pickfrom = self.discards
        rng = len(pickfrom)
        if rng > 0:
            remvidx = random.randint(0, rng-1)
            del pickfrom[remvidx]

    def cardbyindex(self, cardidx, deck="hand"):
        card = None
        if cardidx >= 0:
            if deck == "hand":
                card = self.hand[cardidx]
            elif deck == "recovery":
                card = self.recoveryzone[cardidx]
        return(card)

    def handresoltot(self):
        """
        This is needed in case we have a tie among victory
        points and hand size.
        """
        tot = 0
        # print("    Starting handresoltot")
        for card in self._hand:
            # print("handresoltot adding " + card.title + "(" +
            #      str(card.rank) + ")")
            tot += card.rank
        return(tot)

#    def printinplay(self):
#        retstr = "    ----  In play:\n"
#        for card in self.inplay:
#            retstr += card.title + ": " + str(card.rank) + "\n"
#        return(retstr)
#
#    def printhand(self):
#        retstr = "    ----  Hand:\n"
#        for card in self.hand:
#            retstr += card.title + ": " + str(card.rank) + "\n"
#        return(retstr)
#
#    def printrecover(self):
#        retstr = "    ----  Recovery Zone:\n"
#        if self.checkredalert():
#            retstr += "    [same as in play]\n"
#            # remove this later
#            for card in self._recovery:
#                retstr += card.title.upper() + ", " + str(card.rank) + "\n"
#        else:
#            for card in self.recoveryzone:
#                retstr += card.title + ": " + str(card.rank) + "\n"
#        return(retstr)
#
#    def printdiscards(self):
#        retstr = "    ----  Discards:\n"
#        for card in self.discards:
#            retstr += card.title + ": " + str(card.rank) + "\n"
#        return(retstr)

    def shortprint(self, deck):
        if deck == "hand":
            deckstr = "H"
            cardlist = self.hand
        elif deck == "recovery":
            deckstr = "RZ"
            cardlist = self.recoveryzone
        elif deck == "inplay":
            deckstr = "IP"
            cardlist = self.inplay
        elif deck == "discards":
            deckstr = "D"
            cardlist = self.discards
        retstr = deckstr + ": "
        for card in cardlist:
            retstr += str(card.rank) + " "
        return(retstr)

    def printinplay(self):
        return(self.shortprint("inplay"))

    def printhand(self):
        return(self.shortprint("hand"))

    def printrecover(self):
        return(self.shortprint("recovery"))

    def printdiscards(self):
        return(self.shortprint("discards"))

    def __str__(self):
        if self.checkredalert():
            ramsg = "Red Alert\n"
        else:
            ramsg = "Normal\n"
        return(ramsg + "VP: " + str(self.victorypoints) + "\n" +
               self.printinplay() + self.printhand() +
               self.printrecover() + self.printdiscards())

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
    # assert(not pb.checkredalert())
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
