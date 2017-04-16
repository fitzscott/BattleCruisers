# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:34:25 2017

@author: bushnelf
"""

import Card


class EscapePod(Card.Card):
    """
    EscapePod -
    No cards in hand => pick 3 cards from discard pile
    Clash - discard this card
    """

    def __init__(self):
        Card.Card.__init__(self, "Escape Pod", 43)
        self.add_symbol(Card.Card.Symbols[3])
        self.add_symbol(Card.Card.Symbols[2])

    def main_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        myboard.victorypoints += 1
        if len(myboard.hand) == 0:
            for num in range(3):
                myboard.returndiscardtohand(game, pbidx)

    def clash_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        myboard.discard(self, ["inplay"])

if __name__ == '__main__':
    import Game
    import Player

    ep = EscapePod()
    print("Created " + ep.title)

    class ZeroPlayer(Player.Player):
        """
        ZeroPlayer - just return zero
        """

        def choosecardtoretrievefromdiscard(self, game, pbidx):
            return(game.playerboards[pbidx].discards[0])

    g = Game.Game(1)
    zp = ZeroPlayer("Zero Discard")
    for cidx in range(4):
        card = Card.Card("Null Card " + str(cidx), cidx + 50)
        g.addtocardlist(card)
        g.playerboards[0].addtohand(card)
        g.playerboards[0].discard(card, ["hand"])
    g.addtocardlist(ep)
    g.playerboards[0].addtohand(ep)
    g.playerboards[0].player = zp
    g.playerboards[0].readytoplay(ep)
    print("Before playing " + ep.title + ":")
    print(g.playerboards[0])
    # g.playallcards()
    g.playcards()
    print("After playing " + ep.title + ":")
    print(g.playerboards[0])
