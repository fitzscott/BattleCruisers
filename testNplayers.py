# -*- coding: utf-8 -*-

import sys
import random

import SmarterGame as SG
import SmarterComputerPlayer as SCP
import RandomComputerPlayer as RCP
import CardSet as CS

if len(sys.argv) > 1:
    num_players = int(sys.argv[1])
else:
    num_players = random.randint(3, 5)

print("Playing with " + str(num_players) + " players.")
sg = SG.SmarterGame(num_players)
scp = SCP.SmarterComputerPlayer("Zero Player")
sg.playerboards[0].player = scp
for dp in range(num_players - 1):
    rcp = RCP.RandomComputerPlayer("Random Player " + str(dp+1))
    sg.playerboards[dp+1].player = rcp
cs = CS.CardSet(num_players)
sg.cardlist = cs.getcardset()
sg.sendcardlisttoboards()
for dnr in range(num_players):
    pb = sg.playerboards[dnr]
    c = pb.player.choosecardtodiscard(sg, dnr, ["hand"])
    pb.discard(c, ["hand"])
    c = pb.player.choosecardtosendtorecovery(sg, dnr)
    pb.sendtorecovery(c)
sg.playrounds(100)
