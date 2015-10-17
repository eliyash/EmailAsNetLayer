#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from getpass         import getpass
import smtplib
import sys

if  len(sys.argv)<3:
    print("error: run 'python *.py email password' ")
    sys.exit(1)

login, password = sys.argv[1] , sys.argv[2]
fromaddr = '%s@gmail.com'%login
toaddrs  = fromaddr
msg = 'Data:Now you see me?'
username = fromaddr
password = password
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
