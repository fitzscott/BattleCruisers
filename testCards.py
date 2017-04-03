# -*- coding: utf-8 -*-

import sys

import SmarterGame as SG
import SimpleHumanPlayer as SHP
import RandomComputerPlayer as RCP
import CardSet as CS

# expected parameters: # players, # human players, list of cards to test
num_players = int(sys.argv[1])
num_human_players = int(sys.argv[2])
cards = []
for argidx in range(len(sys.argv) - 3):
    cards.append(int(sys.argv[3+argidx]))

print("Playing with " + str(num_players) + " players.")
sg = SG.SmarterGame(num_players)
for hp in range(num_human_players):
    shp = SHP.SimpleHumanPlayer("Hoomin Player " + str(hp+1))
    sg.playerboards[hp].player = shp
for dp in range(num_players - num_human_players):
    rcp = RCP.RandomComputerPlayer("Random Player " + str(dp+1))
    sg.playerboards[dp+num_human_players].player = rcp
cs = CS.CardSet(num_players)
sg.cardlist = cs.getcardsetbylist(cards)
sg.sendcardlisttoboards()
for dnr in range(num_players):
    pb = sg.playerboards[dnr]
    print(pb)
    c = pb.player.choosecardtodiscard(sg, dnr, ["hand"])
    pb.discard(c, ["hand"])
    print(pb)
    c = pb.player.choosecardtosendtorecovery(sg, dnr)
    pb.sendtorecovery(c)
sg.playrounds(100)
