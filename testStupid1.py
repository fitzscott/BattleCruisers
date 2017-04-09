# -*- coding: utf-8 -*-

import sys
import random

import SmarterGame as SG
import RandomComputerPlayer as RCP
import CardSet as CS

if len(sys.argv) > 1:
    num_players = int(sys.argv[1])
else:
    num_players = random.randint(3, 5)

print("Playing with " + str(num_players) + " players.")
sg = SG.SmarterGame(num_players)
for dp in range(num_players):
    rcp = RCP.RandomComputerPlayer("Random Player " + str(dp+1))
    sg.playerboards[dp].player = rcp
cs = CS.CardSet(num_players)
sg.cardlist = cs.getcardset("Random")
sg.sendcardlisttoboards()
for dnr in range(num_players):
    pb = sg.playerboards[dnr]
    c = pb.player.choosecardtodiscard(sg, dnr, ["hand"])
    pb.discard(c, ["hand"])
    c = pb.player.choosecardtosendtorecovery(sg, dnr)
    pb.sendtorecovery(c)
sg.playrounds(100)
