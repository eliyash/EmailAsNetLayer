#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
import sys
import json

with open('prog_data.json') as data_file:
    data = json.load(data_file)


def sendMassage(massage,data):
    login, password = data["email"] , data["password"]
    name_of_machin = data["other user 0"]

    fromaddr = '%s@gmail.com'%login
    toaddrs  = '%s+%s@gmail.com'%(login,name_of_machin)
    msg = 'Data:'+massage
    username = fromaddr
    password = password
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


sendMassage(raw_input("massage:"),data)
