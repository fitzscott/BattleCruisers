# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 18:28:00 2017

@author: bushnelf
"""

import Card as C


class Reconstruction(C.Card):
    """
    Reconstruction:
    Gain 2VP
    All players choose a card to pass to the left.
    You may swap the new card w/ one of your discards.
    Clash:  No effect
    """

    def __init__(self):
        C.Card.__init__(self, "Reconstruction", 28)
        self.add_symbol(C.Card.Symbols[5])       # Space

    def main_effect(self, game, pbidx):
        myboard = game.playerboards[pbidx]
        myboard.victorypoints += 2
        cardstoadd = {}
        for tgtidx in range(len(game.playerboards)):
            srcpbi = tgtidx - 1       # start w/ -1 index - the last
            srcpb = game.playerboards[srcpbi]
            card = srcpb.player.choosecardtotrade(game, srcpbi, ["hand"])
            if card is not None:
                tgtpb = game.playerboards[tgtidx]
                if tgtidx == pbidx:
                    print("Choose a card to swap in discards, if you like")
                    cdisc = myboard.player.\
                        choosecardtoretrievefromdiscard(game, pbidx)
                    if cdisc is not None:
                        cardstoadd[tgtidx] = cdisc
                        tgtpb.discards.remove(cdisc)
                        # card passed to you goes to discards
                        tgtpb.discards.append(card)
                    else:
                        cardstoadd[tgtidx] = card
                else:
                    cardstoadd[tgtidx] = card
                srcpb.hand.remove(card)
        # Add all the new cards at the end. You cannot pass the card you
        # just received to the next player.
        for tgtpbi in cardstoadd.keys():
            game.playerboards[tgtpbi].hand.append(cardstoadd[tgtpbi])

if __name__ == '__main__':
    import Game as G
    import RandomComputerPlayer as RCP
    import SimpleHumanPlayer as SHP

    plyrs = 5
    g = G.Game(plyrs)
    recon = Reconstruction()
    print("Created card " + recon.title)
    # 5 players, 5 other cards - no particular reason
    othercards = []
    for cnt in range(plyrs):
        othercards.append(C.Card("Swap Me " + str(cnt), cnt + 10))
        g.addtocardlist(othercards[cnt])
        if cnt != 0:
            rcp = RCP.RandomComputerPlayer("RCP " + str(cnt))
        else:
            rcp = SHP.SimpleHumanPlayer("Simpleton Player")
        # rcp = RCP.RandomComputerPlayer("RCP " + str(cnt))
        g.playerboards[cnt].player = rcp
    g.addtocardlist(recon)
    g.sendcardlisttoboards()
    g.playerboards[0].readytoplay(recon)
    # put a card in our discards, so we can test the swap
    g.playerboards[0].hand.remove(othercards[0])
    g.playerboards[0].discards.append(othercards[0])
    # for op in range(plyrs-1):
    #     g.playerboards[op+1].readytoplay(othercards[op])
    g.playcards()
    print(str(g.playerboards[0]))
    print("    Also checking one of the random player boards:")
    print(str(g.playerboards[1]))
