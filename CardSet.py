# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 22:08:56 2017

@author: bushnelf
"""

import random

# import all the types of cards here
import Ambassador
import ArmorPlating
import AttackBots
import Captain
import CombatTactics
import DisruptorRay
import Electropulse
import EscapePod
import LaserCannons
import RecklessPilot
import Salvage
import Shields
import SpecialOps
import SpyDrone
import TacticalNuke
import TargetingCPU


class CardSet(object):
    """
    CardSet - take a list of ranks and create a set (dictionary) of
    Card classes for instantiation.
    """

    cards = {
        1:  SpyDrone.SpyDrone,
        3:  Shields.Shields,
        9:  DisruptorRay.DisruptorRay,
        11: RecklessPilot.RecklessPilot,
        13: Captain.Captain,
        17: Ambassador.Ambassador,
        19: CombatTactics.CombatTactics,
        20: ArmorPlating.ArmorPlating,
        22: SpecialOps.SpecialOps,
        23: TargetingCPU.TargetingCPU,
        29: AttackBots.AttackBots,
        31: LaserCannons.LaserCannons,
        38: TacticalNuke.TacticalNuke,
        39: Salvage.Salvage,
        40: Electropulse.Electropulse,
        43: EscapePod.EscapePod
    }

    cardsets = {
        "Basic": [3, 11, 13, 22, 31, 43, 29, 17],
        "The Big Bang": [2, 3, 6, 12, 15, 31, 33, 34]
        # more to come
    }

    def __init__(self, numplayers):
        self._numcards = numplayers + 3

    def getcardset(self, setname="Basic"):
        loccardset = []
        if setname != "Random":
            for num in range(self._numcards):
                # print("Creating card " + str(num) + " from set " + setname)
                cardidx = CardSet.cardsets[setname][num]
                card = (CardSet.cards[cardidx])()
                loccardset.append(card)
        else:       # put together a random set
            keyset = []
            for cardnum in CardSet.cards.keys():
                keyset.append(cardnum)
            for swp in range(10000):
                idx1 = random.randint(0, len(CardSet.cards)-1)
                idx2 = random.randint(0, len(CardSet.cards)-1)
                # swap 2 enries
                tmp = keyset[idx1]
                keyset[idx1] = keyset[idx2]
                keyset[idx2] = tmp
            for num in range(self._numcards):
                # call the constructor for each card in the set
                card = (CardSet.cards[keyset[num]])()
                loccardset.append(card)
        return(loccardset)

    def getcardsetbylist(self, ranklist):
        loccardset = []
        for rank in ranklist:
            # call the constructor for each card in the set
            card = (CardSet.cards[rank])()
            loccardset.append(card)
        return(loccardset)

if __name__ == '__main__':
    cs = CardSet(3)
    print("CardSet")
    cards = cs.getcardset()
    print("0th card is " + cards[0].title)
    print("    Random set:")
    cards = cs.getcardset("Random")
    for card in cards:
        print(card.title + " " + str(card.rank))
    print("    Set from list:")
    cards = cs.getcardsetbylist([3, 11, 13, 43, 39, 38])
    for card in cards:
        print(card.title + " " + str(card.rank))
