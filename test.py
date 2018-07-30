#!/usr/bin/env python
from time import sleep

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString

class DjangoInsertionObserver(CardObserver):
    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            print("+Inserted: ", toHexString(card.atr))
        for card in removedcards:
            print("-Removed: ", toHexString(card.atr))

if __name__ == '__main__':
    cardmonitor = CardMonitor()
    cardobserver = DjangoInsertionObserver()
    cardmonitor.addObserver(cardobserver)
    while True:
        sleep(1)
