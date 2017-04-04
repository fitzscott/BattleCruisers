# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 18:42:24 2017

@author: bushnelf
"""

import Card as C


class Salvage(C.Card):
    """
    Salvage - gain 3VP, steal random card from discard of chosen player.
    Clash - destroy (i.e. out of game) 2 cards from your discard pile.
    """

    def __init__(self):
        C.Card.__init__(self, "Salvage", 39)
        self.add_symbol(C.Card.Symbols[5])      # Space
        self.add_symbol(C.Card.Symbols[4])      # Weapons

    def main_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        # 1st get 3VP
        myboard.victorypoints += 3
        # Now handle stealing discards
        pl = myboard.player.chooseplayertotakecardfrom(game, pbidx,
                                                       ["discards"])
        print("Chose player " + str(pl) + " (I am " + str(pbidx) + ")")
        if pl is not None:
            targetpb = game.playerboards[pl]
            print("Chosen RZ: " + targetpb.printrecover())
            card = myboard.player.randomcardfromplayer(game, pbidx,
                                                       ["discards"], pl)
            if card is not None:
                print("Got random card: " + card.title + ", rank: " +
                      str(card.rank))
                # player chooser should not choose a protected opponent,
                # but if it does, disallow the effect.
                if targetpb.protected == 0:
                    myboard.hand.append(card)
                    targetpb.discards.remove(card)
                else:
                    print("Cannot steal a card from a protected player")
        else:
            print("No target for " + self.title)

    def clash_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        # Must destroy 2 cards from discards
        for todel in range(2):
            myboard.removerandomcardfromgame(game, pbidx, ["discards"])
#            rzcard = myboard.player.choosecardtodiscard(game, pbidx,
#                                                        ["discards"])
#            if rzcard is not None:
#                print(myboard.player.name + " discarding " + rzcard.title)
#                myboard.discard(rzcard, ["discards"])

if __name__ == '__main__':
    s = Salvage()
    print("Created " + s.title + ", rank " + str(s.rank))
