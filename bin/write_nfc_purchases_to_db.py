#!/usr/bin/env python
import django
from django.conf import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coffeemachine.settings")
django.setup()

from time import sleep

from smartcard.CardType import AnyCardType
from smartcard.CardMonitoring import CardMonitor, CardObserver, CardRequest
from smartcard.util import toHexString
from smartcard.ATR import ATR

from coffeelist.models import Tag, Purchase, Price, User
from coffeelist.views import get_user_totals
from django.utils.timezone import now

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
            card.connection = card.createConnection()
            card.connection.connect()
            res, s1, s2 = card.connection.transmit(cmdMap["getuid"])
            print("Tag registered: {}".format(toHexString(res)))
            if res:
                card.connection.transmit(cmdMap["blinkGreenWithSound"])
                tag, created = Tag.objects.get_or_create(tag_value=toHexString(res))
                purchase = Purchase(tag=tag, date=now(), price=Price.objects.latest('id'))
                purchase.save()
                # Print out balance, TODO: to screen
                if tag.owner:
                    print("{}: {}".format(tag.owner, get_user_totals().loc[tag.owner.id]["balance"]))
                else:
                    print("Please associate tag with user in web interface. Unknown balance.")
            else:
                print("Failure reading the thing")
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

def main():
    print("{} Starting NFC Monitor. Waiting for input.".format(now()))
    init()
    cardmonitor = CardMonitor()
    cardobserver = DjangoInsertionObserver()
    cardmonitor.addObserver(cardobserver)
    while True:
        sleep(1)

if __name__ == '__main__':
    main()
