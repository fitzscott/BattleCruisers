# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 23:06:49 2017

@author: bushnelf
"""

import Card


class CombatTactics(Card.Card):
    """
    CombatTactics - card 19
    """

    def __init__(self):
        Card.Card.__init__(self, "Combat Tactics", 19)
        # super().__init__("Combat Tactics", 19)
        self.add_symbol(Card.Card.Symbols[4])    # Weapons / Combat
        self.add_symbol(Card.Card.Symbols[5])    # Space / Maneuver

    def main_effect(self, game, pbidx):
        """
        main_effect -
        1) Check victory points:  If < 5, gain 5.
        2) If Weapons symbol in recovery, get card back from discard pile.
        """
        # import PlayerBoard

        myboard = game.playerboards[pbidx]
        if myboard.victorypoints < 5:
            myboard.victorypoints += 5

        if myboard.checkrecoveryforsymbol("Weapons"):
            myboard.returndiscardtohand(game, pbidx)

if __name__ == '__main__':
    import Game

    ct = CombatTactics()
    print("Created card " + ct.title)
    g = Game.Game(1)
    ct.main_effect(g, 0)
    print("Player board now has " + str(g.playerboards[0].victorypoints) +
          " victory points.")
