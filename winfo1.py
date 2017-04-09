# -*- coding: utf-8 -*-

# import os
import sys

if len(sys.argv) < 2:
    print("Need a game ID parameter")
    sys.exit(-1)

gameid = sys.argv[1]
losers = {}

for line in sys.stdin:
    line.strip()
    flds = line.split()
    fldcnt = len(flds)
    if fldcnt >= 2:
        if flds[1] == "Round":
            rnd = flds[2]
    if fldcnt >= 5:
        if flds[1] == "Player":
            if flds[3] == "playing":
                plnum = flds[2]
                cardnum = flds[4]
                print("|".join([gameid, "P", rnd, plnum, cardnum]))
        elif flds[4] == "lost!":
            plnm = flds[3]
            if plnm not in losers:
                losers[plnm] = rnd
        elif fldcnt >= 8 and flds[7] == "winner!":
            if flds[6] == "surviving":
                meth = "S"
            elif flds[6] == "victorious":
                meth = "V"
            else:
                meth = "U"
            for pl in losers:
                lastround = losers[pl]
                print("|".join([gameid, "L", lastround, pl]))
            print("|".join([gameid, "W", rnd, plnum, meth]))
