#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import imaplib
import json
import email
import smtplib

from pdb import set_trace as debug
# import email
# import email.header
# import datetime
# import getpass

class MessageNet:

    def __init__(self):
        with open('prog_data.json') as data_file:
            data = json.load(data_file)
        self.login = data["email"]
        self.password = data["password"]
        self.other_email = data['other email 0']
        self.this_user = data["this user"]
        self.other_user = data['other user 0']

    def sendMessage(self,message):

        fromaddr = '%s@gmail.com'%self.login
        toaddrs  = '%s@gmail.com'%(self.other_email)
        # toaddrs  = ['%s+%s@gmail.com'%(other_email,other_user)]
        # msg = 'From:%s\nTo:%s@gmail.com\nSubject:%s\n\nData:%s'%(fromaddr, other_email, this_user, message)
        msg = 'From:<*>%s %s\nTo:%s\nSubject:Subject\n\nData:%s'%(self.this_user, fromaddr, self.other_user, message)

        username = fromaddr
        password = self.password
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()

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
            # M.store(num,'+X-GM-LABELS', '%s_received'%self.other_user)

            result = M.uid('COPY', msg_uid, self.other_user + '_received')
            if result[0] == 'OK':
                mov, data = M.uid('STORE', msg_uid , '+FLAGS', '\\Deleted')

            #M.store(num,'-X-GM-LABELS', '%s'%self.other_user)
            #iterator
            yield msg_str

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

        rv, data = M.select(self.this_user)
        if rv == 'OK':
            # print( "Processing mailbox...\n")
            for msg in self.process_mailbox(M):
                Massage = msg[(msg.find("Data:")+5):]
                address = msg[(msg.find("From:<*>")+8):]#TODO spetial sign
                [machin_other,email_other] = address.split("\r\n")[0].split(" ")
                print ('%s(%s) says: %s' %(machin_other,email_other,Massage))
                # print ('address: %s' %address)

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
    if (len(sys.argv) < 2 or (sys.argv[1]!="read" and sys.argv[1]!="send")):
        print("add read/send ")
    else:
        mail = MessageNet()
        if(sys.argv[1]=="read"):
            mail.readMessages()
        else:
            if(len(sys.argv) == 2):  mail.sendMessage(raw_input("message:"))
            else :  mail.sendMessage(sys.argv[2])
