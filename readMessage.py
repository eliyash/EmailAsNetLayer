#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import imaplib
import json
# import email
# import email.header
# import datetime
# import getpass



with open('prog_data.json') as data_file:
    data = json.load(data_file)



def readMassage(data):
    login, password = data["email"] , data["password"]
    name_of_machin = data["this user"]

    EMAIL_FOLDER = name_of_machin


    M = imaplib.IMAP4_SSL('imap.gmail.com')

    try:
        # rv, data = M.login(login, getpass.getpass())
        rv, data = M.login(login, password)
    except imaplib.IMAP4.error:
        print("LOGIN FAILED!!! ")
        sys.exit(1)

    # print(rv, data)

    rv, mailboxes = M.list()
    # if rv == 'OK':
    #     print("Mailboxes:")
    #     print(mailboxes)

    rv, data = M.select(EMAIL_FOLDER)
    if rv == 'OK':
        # print( "Processing mailbox...\n")

        rv, data = M.search(None,'ALL')
        if rv != 'OK':
            print("No messages found!")
            return
        for num in data[0].split():
            rv, data = M.fetch(num, '(RFC822)')
            if rv != 'OK':
                print("ERROR getting message", num)
                return

            # msg = email.message_from_string(data[0][1])
            msg = data[0][1]
            # decode = email.header.decode_header(msg['Data'])[0]
            # data = unicode(decode[0])
            print("Massage: %s"% msg[(msg.find("Data:")+5):])

            # M.store(num,'-X-GM-LABELS', name_of_machin)
            M.store(num, '+FLAGS', '\\Deleted')
            M.store(num,'+X-GM-LABELS', '%s_received'%name_of_machin)

        M.expunge()  # not need if auto-expunge enabled
        M.close()
    else:
        print("ERROR: Unable to open mailbox ", rv)



readMassage(data)
