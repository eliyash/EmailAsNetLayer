#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pdb import set_trace as debug

import smtplib
import sys
import json

if sys.version_info.major > 2:
    raw_input = input

with open('prog_data.json') as data_file:
    data = json.load(data_file)

def sendMessage(data,message):
    login, password = data["email"] , data["password"]
    name_of_machin = data["other user 0"]

    fromaddr = '%s@gmail.com'%login
    toaddrs  = '%s+%s@gmail.com'%(login,name_of_machin)
    msg = 'Data:'+message

    username = fromaddr
    password = password
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        sendMessage(data, sys.argv[1])
    else:
        sendMessage(data, raw_input("message:"))
