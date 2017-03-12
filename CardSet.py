# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 22:08:56 2017

@author: bushnelf
"""

# import all the types of cards here


class CardSet:
    """
    CardSet - take a list of ranks and create a set (dictionary) of
    Card classes for instantiation.
    """

    cards = {
    }

    def __init__(self, numplayers):
        self._numcards = numplayers + 3

if __name__ == '__main__':
    cs = CardSet(3)
    print("CardSet")
