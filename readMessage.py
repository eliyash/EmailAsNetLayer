#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from getpass         import getpass
import sys
import imaplib
import json
import email


from pdb import set_trace as debug
# import email
# import email.header
# import datetime
# import getpass


# if  len(sys.argv)<4:
#     print("error: run 'python *.py <email> <password> <target-pc-id>' ")
#     sys.exit(1)

class readMessage:

    def __init__(self):
        with open('prog_data.json') as data_file:
            data = json.load(data_file)
        self.login, self.password = data["email"] , data["password"]
        self.name_of_machin = data["this user"]
        self.EMAIL_FOLDER = self.name_of_machin

    def process_mailbox(self, M):


        #rv, data = M.search(None,'ALL')
        rv, data = M.uid('SEARCH',None, 'ALL')
        if rv != 'OK':
            raise MailException("No messages found!")

        for msg_uid in data[0].split():
            rv, data = M.uid("FETCH", msg_uid, "(RFC822)")
            #rv, data = M.fetch(msg_uid, '(RFC822)')
            if rv != 'OK':
                raise MailException("ERROR getting message " + str(msg_uid))

            # msg = email.message_from_string(data[0][1])
            # debug()
            msg_str = data[0][1].decode('utf-8') #decode for python 3
            # decode = email.header.decode_header(msg['Data'])[0]
            # data = unicode(decode[0])
            # M.store(num,'+X-GM-LABELS', '%s_received'%self.name_of_machin)

            result = M.uid('COPY', msg_uid, self.name_of_machin + '_received')
            if result[0] == 'OK':
                mov, data = M.uid('STORE', msg_uid , '+FLAGS', '\\Deleted')

            #M.store(num,'-X-GM-LABELS', '%s'%self.name_of_machin)
            #iterator
            yield msg_str[(msg_str.find("Data:")+5):]

    def readMessages(self):
        M = imaplib.IMAP4_SSL('imap.gmail.com')

        try:
            # rv, data = M.login(login, getpass.getpass())
            rv, data = M.login(self.login, self.password)
        except imaplib.IMAP4.error:
            raise MailException("LOGIN FAILED!!! ")

        # print(rv, data)

        rv, mailboxes = M.list()
        # if rv == 'OK':
        #     print("Mailboxes:")
        #     print(mailboxes)

        rv, data = M.select(self.EMAIL_FOLDER)
        if rv == 'OK':
            # print( "Processing mailbox...\n")
            for msg in self.process_mailbox(M):
                print ('Massage: %s' %msg)

            # M.select('[Gmail]/Trash')  # select all trash
            # M.store("1:*", '+FLAGS', '\\Deleted')  #Flag all Trash as Deleted
            M.expunge()  # not need if auto-expunge enabled
            M.close()
            #M.logout()?
        else:
            raise MailException("ERROR: Unable to open mailbox ", rv)



    class MailException(Exception):
        pass

if __name__ == '__main__':
    inbox = readMessage()
    inbox.readMessages()
