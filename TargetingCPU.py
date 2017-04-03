# -*- coding: utf-8 -*-

import Card as C


class TargetingCPU(C.Card):
    """
    Targeting CPU -
    Take 3 VP from any opponent
    Clash:  Lose 1 VP.  Players who played other cards _gain_ 1 VP total,
        so need to keep track of which copy of TargetingCPU was played
        first and only apply the +1 VP then. Or something similar.
    """

    def __init__(self):
        C.Card.__init__(self, "Targeting CPU", 23)
        self.add_symbol(C.Card.Symbols[4])      # Weapons
        self._clashedthisturn = False

    def main_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        tgtpb = mypb.player.chooseplayertotakevictoryfrom(game, pbidx)
        if tgtpb is not None:
            vptotake = tgtpb.victorypoints
            if vptotake > 3:
                vptotake = 3
            mypb.victorypoints += vptotake
            tgtpb.victorypoints -= vptotake

    def clash_effect(self, game, pbidx):
        mypb = game.playerboards[pbidx]
        mypb.victorypoints -= 1
        if not self._clashedthisturn:       # give everyone else VP
            for opbidx in range(len(game.playerboards)):
                if opbidx != pbidx:
                    opb = game.playerboards[opbidx]
                    # This is a clash effect, so players ignoring main
                    # effects would still get their 1 VP.
                    if len(opb.inplay) > 0 and opb.inplay[0].rank != self.rank:
                        opb.victorypoints += 1
        self._clashedthisturn = True

    def end_of_turn_effect(self, game, pbidx):
        """
        We will keep track of whether the Targeting CPU has clashed this
        turn with an instance variable. The cards should only be instantiated
        once each, so we do not need to use a class variable.
        """
        self._clashedthisturn = False

if __name__ == '__main__':
    tc = TargetingCPU()
    print("Created " + tc.title)
