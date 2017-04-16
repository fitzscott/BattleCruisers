# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 22:07:57 2017

@author: bushnelf
"""

import Card as C


class Bureaucrat(C.Card):
    """
    Bureaucrat:
    Discard this card.Name a card and take all copiees of that card
    from oppenents' hands into your hand.
    Clash:  Discard 1 card.
    """
    def __init__(self):
        C.Card.__init__(self, "Bureaucrat", 44)
        self.add_symbol(C.Card.Symbols[2])      # People

    def main_effect(self, game, pbidx):
        pb = game.playerboards[pbidx]
        # Not clear if cards that prevent main effects from causing discards
        # would also cause this card's main effect not to discard itself.
        pb.discard(self, ["inplay"])
        picked = pb.player.choosecardbyname(game, pbidx)
        for pboi in range(len(game.playerboards)):
            if pboi != pbidx:
                pbo = game.playerboards[pboi]
                for hcard in pbo.hand:
                    if hcard.title == picked.title:
                        pb.hand.append(hcard)
                        pbo.hand.remove(hcard)

    def clash_effect(self, game, pbidx):
        pb = game.playerboards[pbidx]
        card = pb.player.choosecardtodiscard(game, pbidx, ["hand", "recovery"])
        pb.discard(card, ["hand", "recovery"])

if __name__ == '__main__':
    import Game as G
    import SimpleHumanPlayer as SHP

    b = Bureaucrat()
    g = G.Game(3)
    for p in range(3):
        shp = SHP.SimpleHumanPlayer("SHP " + str(p+1))
        g.playerboards[p].player = shp
    c1 = C.Card("Not this one", 500)
    c2 = C.Card("Not this one either", 501)
    c3 = C.Card("Yes this one", 503)
    g.addtocardlist(c1)
    g.addtocardlist(c2)
    g.addtocardlist(c3)
    g.addtocardlist(b)
    g.sendcardlisttoboards()
    g.playerboards[0].readytoplay(b)
    print("When prompted, choose one of the cards.")
    # g.playallcards()
    g.playcards()
    print("Should show Bureaucrat in discards, plus")
    print("    the chosen card thrice in hand.")
    print(g.playerboards[0])
