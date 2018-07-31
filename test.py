#!/usr/bin/env python
from time import sleep

from smartcard.CardType import AnyCardType
from smartcard.CardMonitoring import CardMonitor, CardObserver, CardRequest
from smartcard.util import toHexString
from smartcard.ATR import ATR

cmdMap = {
    "muteCardDetection":[0xFF, 0x00, 0x52, 0x00, 0x00],
    "unmuteCardDetection":[0xFF, 0x00, 0x52, 0xFF, 0x00],
    "getuid":[0xFF, 0xCA, 0x00, 0x00, 0x00],
    "firmver":[0xFF, 0x00, 0x48, 0x00, 0x00],
    "blinkOrange": [0xFF, 0x00, 0x40, 0xCF, 0x04, 0x03, 0x00, 0x01, 0x00 ],
    "blinkOrangeWithSound": [0xFF, 0x00, 0x40, 0xCF, 0x04, 0x00, 0x01, 0x01, 0x02 ],
    "blinkGreenWithSound": [0xFF, 0x00, 0x40, 0b1010110, 0x04, 0x00, 0x01, 0x01, 0x02 ],
    "noTimeOutCheck":[0xFF, 0x00, 0x41, 0x00, 0x00],
    "fiveSecondTimeout":[0xFF, 0x00, 0x41, 0x01, 0x00],
    "waitUntilRespond":[0xFF, 0x00, 0x41, 0xFF, 0x00],
}

class DjangoInsertionObserver(CardObserver):
    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            try:
                card.connection = card.createConnection()
                card.connection.connect()
                res, s1, s2 = card.connection.transmit(cmdMap["getuid"])
                print(toHexString(res))
                if res:
                    res, s1, s2  = card.connection.transmit(cmdMap["blinkGreenWithSound"])
                else:
                    print("Failure reading the thing")
            except CardRequestTimeoutException as e:
                # TODO: Still does not catch all exceptions. Try moving cards away quickly and those errors still occur (and cause an infinite loop in our program)
                # We should probably not use the observer based approach.
                print("Error reading the thing")
                continue
        for card in removedcards:
            pass

def init():
    initialized = False
    while not initialized:
        try:
            card_request = CardRequest(timeout=None)
            card_service = card_request.waitforcard()
            card_service.connection.connect()
            card_service.connection.transmit(cmdMap["muteCardDetection"])
            initialized = True
        except:
             pass

if __name__ == '__main__':
    init()
    cardmonitor = CardMonitor()
    cardobserver = DjangoInsertionObserver()
    cardmonitor.addObserver(cardobserver)
    while True:
        sleep(1)
