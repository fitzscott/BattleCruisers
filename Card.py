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
               "People",          # black/yellow - people
               "Technology",      # yellow/green - circuit (was Equipment)
               "Weapons",         # yellow/red - bullets (was Attack)
               "Space"            # white/purple - ring planet (was Maneuver)
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

    def defense(self, game, pbidx, effect=["main_effect"], thisorlast="this"):
        """
        parameters:
            effect:
                main_effect:  Opponents' main effects
                vp_theft: Stealing your victory points
                card_discard: Forcing a card to be discarded
                card_theft: Stealing your card
            Can have combinations of effects, e.g. stealing victory
                points as a main effect, as some defenses only apply
                against, e.g. VP theft as a main effect, rather than
                all main effects.
            thisorlast:  Whether it applies to the card played this
                round or last round.
        """
        return False

    def redirect(self, pb, effect, thisorlast="this"):
        """
        Much like defense, but instead of disallowing an attack, it
        redirects it toward another target.
        Parameters are similar, but we only need our player board.
        """
        return False

if __name__ == '__main__':
    c = Card("Spy Drone", 1)
    c.add_symbol("Technology")
    print("The " + c.title + "'s rank is " + str(c.rank))
    print(c.title + " has symbol " + c.symbols[0])
