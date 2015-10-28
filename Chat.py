#!/usr/bin/env python
# -*- coding: utf-8 -*-

#TODO: pin the "massage:" line to the bottom line :)
#NOTE: run this program twice, once with one config file and one with another

import sys
from time import sleep
from threading import Thread
from MessageNet import MessageNet

def printLoop(mail):
    # print("readLoop")
    mail.open_read()
    while True:
        for data in mail.readMessages():
            print("\nuser: %s, from mail: %s, sent: '%s'\n"%(data['machin_other'],data['email_other'],data['Massage']))
        sleep(0.1)
    mail.close_read()

def sendLoop(mail):
    # print("sendLoop")
    while True:
        mail.sendMessage(raw_input("massage:"))


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        # mail = MessageNet('prog_data.json')
        print ("error , add json file")
    else:
        mail = MessageNet(sys.argv[1])
        sendingLoop = Thread(target=sendLoop,args=(mail,))
        readingLoop = Thread(target=printLoop,args=(mail,))

        print("----------< CHAT STARTED >-------------")
        sendingLoop.start()
        readingLoop.start()
