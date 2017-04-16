# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 18:27:50 2017

@author: bushnelf
"""

import Card as C


class TechOfficer(C.Card):
    """
    Tech Officer:
    Cards are resolved in the order you choose.
    Clash: Lose 2 VP
    """

    def __init__(self):
        C.Card.__init__(self, "Tech Officer", 2)
        self.add_symbol(C.Card.Symbols[2])      # People
        self.add_symbol(C.Card.Symbols[1])      # Anti-negation

    def main_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        #  figure out how the remaining cards should be re-ranked
        realeffrankmap = myboard.player.chooserankingforcards(game, pbidx)
        for card in game.cardlist:
            if card.rank in realeffrankmap:
                card.effectiverank = realeffrankmap[card.rank]

    def clash_effect(self, game, pbidx):
        game.playerboards[pbidx].victorypoints -= 2

if __name__ == '__main__':
    import Game as G
    import RandomComputerPlayer as RCP
    import SimpleHumanPlayer as SHP

    plyrs = 5
    g = G.Game(plyrs)
    t_o = TechOfficer()
    print("Created card " + t_o.title)
    # 5 players, 5 other cards - no particular reason
    othercards = []
    for cnt in range(plyrs):
        othercards.append(C.Card("Swap Me " + str(cnt), cnt + 10))
        g.addtocardlist(othercards[cnt])
        if cnt != 0:
            rcp = RCP.RandomComputerPlayer("RCP " + str(cnt))
        else:
            rcp = SHP.SimpleHumanPlayer("Tech Off Player")
        # rcp = RCP.RandomComputerPlayer("RCP " + str(cnt))
        g.playerboards[cnt].player = rcp
    g.addtocardlist(t_o)
    g.sendcardlisttoboards()
    g.playerboards[0].readytoplay(t_o)
    for op in range(plyrs-1):
        g.playerboards[op+1].readytoplay(othercards[op])
    g.playcards()
