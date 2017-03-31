# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 21:48:36 2017

@author: bushnelf
"""

import RandomGame as rg


class SmarterGame(rg.RandomGame):
    """  Not sure we actually need this class...  """
    def __init__(self, numplayers):
        rg.RandomGame.__init__(self, numplayers)

if __name__ == '__main__':
    import SmarterComputerPlayer as SCP
    import RandomComputerPlayer as RCP
    import CardSet as CS

    num_players = 4

    sg = SmarterGame(num_players)
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
    sg.playrounds(20)
