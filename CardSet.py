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
import AttackWing
import Bureaucrat
import Captain
import CloakingDevice
import CombatTactics
import ComputerVirus
import Decoy
import DisruptorRay
import Electropulse
import EscapePod
import EvasiveAction
import HeavyAssault
import LaserCannons
import Navigator
import Negotiator
import PirateRaid
import PodBayDoors
import PrecisionStrike
import RecklessPilot
import Reconstruction
import RepairCrew
import Salvage
import SecurityChief
import Shields
import SpecialOps
import SpyDrone
import SupplyConvoy
import TacticalNuke
import TargetingCPU
import TechOfficer
import TimeWarp


class CardSet(object):
    """
    CardSet - take a list of ranks and create a set (dictionary) of
    Card classes for instantiation.
    """

    cards = {
        1:  SpyDrone.SpyDrone,
        2:  TechOfficer.TechOfficer,
        3:  Shields.Shields,
        4:  CloakingDevice.CloakingDevice,
        5:  Navigator.Navigator,
        6:  Decoy.Decoy,
        7:  SecurityChief.SecurityChief,
        8:  EvasiveAction.EvasiveAction,
        9:  DisruptorRay.DisruptorRay,
        11: RecklessPilot.RecklessPilot,
        12: Negotiator.Negotiator,
        13: Captain.Captain,
        15: PodBayDoors.PodBayDoors,
        16: RepairCrew.RepairCrew,
        17: Ambassador.Ambassador,
        19: CombatTactics.CombatTactics,
        20: ArmorPlating.ArmorPlating,
        22: SpecialOps.SpecialOps,
        23: TargetingCPU.TargetingCPU,
        24: HeavyAssault.HeavyAssault,
        28: Reconstruction.Reconstruction,
        29: AttackBots.AttackBots,
        30: ComputerVirus.ComputerVirus,
        31: LaserCannons.LaserCannons,
        32: PirateRaid.PirateRaid,
        33: AttackWing.AttackWing,
        34: PrecisionStrike.PrecisionStrike,
        37: SupplyConvoy.SupplyConvoy,
        38: TacticalNuke.TacticalNuke,
        39: Salvage.Salvage,
        40: Electropulse.Electropulse,
        43: EscapePod.EscapePod,
        44: Bureaucrat.Bureaucrat,
        45: TimeWarp.TimeWarp
    }

    cardsets = {
        "Basic": [3, 11, 13, 22, 31, 43, 29, 17],
        "The Big Bang": [2, 3, 6, 12, 15, 31, 33, 34],
        "Crouching Liger, Hidden Dargon": [1, 4, 19, 30, 31, 39, 43, 9],
        "Friendship Breaker": [5, 6, 11, 28, 29, 31, 39, 34],
        "Clash of Captains": [1, 3, 20, 32, 34, 40, 13, 45],
        "The Bad, the Worse, and the Ugly": [11, 16, 22, 23, 31, 43, 8, 9],
        "Politics in a Space Fight": [12, 38, 30, 33, 20, 22, 11, 9],
        "The Fast and the Fury": [6, 37, 38, 39, 19, 20, 23, 34],
        "A Leaf on the Wind": [1, 5, 13, 22, 30, 40, 2, 7],
        "Pirate Cove": [1, 4, 20, 32, 34, 40, 30, 17],
        "Scorched Space": [9, 20, 23, 33, 38, 39, 28, 16],
        "Final Mission": [11, 15, 16, 19, 22, 31, 44, 9],
        "Glorious Victory": [7, 12, 13, 17, 23, 37, 5, 22],
        "Tech Warefare": [6, 16, 29, 30, 33, 43, 1, 9],
        "High Stakes": [1, 13, 17, 38, 39, 43, 8, 9],
        "Race for the Cosmos": [2, 11, 12, 17, 22, 28, 7, 9],
        "One Trick Pony": [2, 15, 19, 29, 32, 40, 8, 34],
        "The Hot Potato": [1, 11, 20, 28, 40, 43, 45, 9],
        "Fireflight": [5, 19, 22, 23, 37, 39, 15, 9],
        "Slow Burn": [5, 8, 31, 43, 43, 45, 4, 2],
        "The Nushura Contingency": [9, 20, 22, 33, 38, 39, 44, 17]
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

    def getcardsetbyindices(self, indexlist):
        loccardset = []
        for idx in indexlist:
            # call the constructor for each card in the set
            rank = CardSet.cards.keys()[idx]
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
    cards = cs.getcardsetbyindices([14, 15, 16, 17, 18, 19])
    print("    Set by indices (start w/ rank 20):")
    for card in cards:
        print(card.title + " " + str(card.rank))
