#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from getpass         import getpassimport sys
import imaplib
# import email
# import email.header
# import datetime
# import getpass


if  len(sys.argv)<3:
    print "error: run 'python *.py email password' "
    sys.exit(1)

login, password = sys.argv[1] , sys.argv[2]

EMAIL_FOLDER = "inbox"


def process_mailbox(M):

    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return

        # print "Real All:", data
        # print "Real All[0]:", data[0]
        # print "Real All[0[1]][1]:", data[0][1]
        # msg = email.message_from_string(data[0][1])
        msg = data[0][1]
        # print "type data:",type(data)
        # print "type msg:",type(msg)
        # print "msg['Data']:", msg['Data']
        # decode = email.header.decode_header(msg['Data'])[0]
        # data = unicode(decode[0])
        # print "All:", msg
        print "Massage:",  msg[(msg.find("Data:")+5):]

        M.store(num,'+X-GM-LABELS', '\\Trash')

M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    # rv, data = M.login(login, getpass.getpass())
    rv, data = M.login(login, password)
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!! "
    sys.exit(1)

# print rv, data

rv, mailboxes = M.list()
# if rv == 'OK':
#     print "Mailboxes:"
#     print mailboxes

rv, data = M.select(EMAIL_FOLDER)
if rv == 'OK':
    # print "Processing mailbox...\n"
    process_mailbox(M)
    M.select('[Gmail]/Trash')  # select all trash
    M.store("1:*", '+FLAGS', '\\Deleted')  #Flag all Trash as Deleted
    M.expunge()  # not need if auto-expunge enabled
    M.close()
else:
    print "ERROR: Unable to open mailbox ", rv
