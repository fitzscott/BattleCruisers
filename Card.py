# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 20:40:22 2017

@author: bushnelf
"""


class Card(object):
    """
    Card - base class.  A player playing a card causes interaction
    with one or more other players.  There are two conditions:
    1)  The title of the card is unique among currently-played cards, and
    2)  The title of the being played is shared among players.
    The first condition is called "Main" and the second "Clash".
    """

    # Names for symbols on cards, mostly guesses.  Color & description.
    Symbols = [
               "Negation",        # blue/red circle
               "Anti-negation",   # blue/red circle w/ strikethrough
               "People",          # black/yellow - looks like people
               "Equipment",       # yellow/green - looks like circuit
               "Attack",          # yellow/red - looks like bullets
               "Maneuver"         # white/purple - looks like ring planet
              ]

    def __init__(self, title, rank):
        self._title = title
        self._rank = rank
        self._symbols = []

    @property
    def title(self):
        return(self._title)

    @property
    def rank(self):
        return(self._rank)

    @property
    def symbols(self):
        return(self._symbols)

    def add_symbol(self, sym):
        self._symbols.append(sym)

    def main_effect(self, game, pbidx):
        """
        Good guess - The card chosen is unique among the players,
        so it takes beneficial action for its player.
        """
        print("Running card " + self.title + "'s main effect")

    def clash_effect(self, game, pbidx):
        """
        Bad guess - The card chosen is shared among the players,
        so bad stuff happens to its players.
        """
        print("Running card " + self.title + "'s clash effect")

    def end_of_turn_effect(self, game, pbidx):
        pass

if __name__ == '__main__':
    c = Card("Spy Drone", 1)
    c.add_symbol("Equipment")
    print("The " + c.title + "'s rank is " + str(c.rank))
    print(c.title + " has symbol " + c.symbols[0])
