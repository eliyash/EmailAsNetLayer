#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from getpass         import getpass
import sys
import imaplib
import json
# import email
# import email.header
# import datetime
# import getpass


# if  len(sys.argv)<4:
#     print("error: run 'python *.py <email> <password> <target-pc-id>' ")
#     sys.exit(1)


with open('prog_data.json') as data_file:
    data = json.load(data_file)
login, password = data["email"] , data["password"]
name_of_machin = data["this user"]






EMAIL_FOLDER = name_of_machin


def process_mailbox(M):

    rv, data = M.search(None,'ALL')#BCC', '"eliyashaddget@gmail.com"')
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

        M.store(num,'+X-GM-LABELS', '%s_received'%name_of_machin)

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
    process_mailbox(M)
    # M.select('[Gmail]/Trash')  # select all trash
    # M.store("1:*", '+FLAGS', '\\Deleted')  #Flag all Trash as Deleted
    M.expunge()  # not need if auto-expunge enabled
    M.close()
else:
    print("ERROR: Unable to open mailbox ", rv)
