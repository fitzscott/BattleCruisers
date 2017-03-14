# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 22:05:57 2017

@author: bushnelf
"""

import Card


class RecklessPilot(Card.Card):
    """
    Reckless Pilot - discard a card, get 4 VP
    """

    def __init__(self):
        Card.Card.__init__(self, "Reckless Pilot", 11)
        self.add_symbol(self.Symbols[2])

    def main_effect(self, game, pbidx):
        """
        Discard 1 card + get 4 VP
        """
        myboard = game.playerboards[pbidx]
        card = myboard.player.choosecardtodiscard(["hand", "recovery"])
        myboard.discard(card, ["hand", "recovery"])
        myboard.victorypoints += 4

    def clash_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        card = myboard.player.choosecardtodiscard(["hand", "inplay"])
        myboard.discard(card, ["hand", "inplay"])

    def end_of_turn_effect(self, game, pbidx):
        pass

if __name__ == '__main__':
    rp = RecklessPilot()
    print("Created " + rp.title + " card.")
    if "People" in rp.symbols:
        print("Contains People symbol.")
