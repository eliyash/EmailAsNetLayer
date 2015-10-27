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

    def __init__(self, json_file = 'prog_data.json'):
        with open(json_file) as data_file:
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

    def process_mailbox(self):
        rv, data = self.M.select(self.this_user)
        if rv != 'OK':
            raise MailException('ERROR: Unable to open mailbox ')

        rv, data = self.M.uid('SEARCH',None, 'ALL')
        if rv != 'OK':
            raise MailException("No messages found!")

        #TODO: what happens when new mail arrives?
        for msg_uid in data[0].split():
            rv, data = self.M.uid("FETCH", msg_uid, "(RFC822)")
            #rv, data = M.fetch(msg_uid, '(RFC822)')
            if rv != 'OK':
                raise MailException("ERROR getting message " + str(msg_uid))

            msg_str = data[0][1].decode('utf-8') #decode for python 3
            result = self.M.uid('COPY', msg_uid, self.other_user + '_received')
            if result[0] == 'OK':
                mov, data = self.M.uid('STORE', msg_uid , '+FLAGS', '\\Deleted')

            #iterator
            yield msg_str

    def open_read(self):
        self.M = imaplib.IMAP4_SSL('imap.gmail.com')
        try:
            # rv, data = M.login(login, getpass.getpass())
            rv, data = self.M.login(self.login, self.password)
        except imaplib.IMAP4.error:
            raise MailException("LOGIN FAILED!!! ")
        rv, mailboxes = self.M.list() #do we need that?

    def close_read(self):
        self.M.expunge()  # not need if auto-expunge enabled
        self.M.close()
        #M.logout()?

    #TODO: more parsing options?
    def parseMsg(self, msg):
        Massage = msg[(msg.find("Data:")+5):]
        address = msg[(msg.find("From:<*>")+8):]#TODO special tag
        [machin_other,email_other] = address.split("\r\n")[0].split(" ")
        return {'Massage':  Massage,
                'machin_other' : machin_other,
                'email_other' : email_other,
                }

    def readMessages(self):            # print( "Processing mailbox...\n")
        for msg in self.process_mailbox():
            msg_parse = self.parseMsg(msg)
            print ('%s(%s) says: %s' %(msg_parse['machin_other'],
                                        msg_parse['email_other'],
                                        msg_parse['Massage'],
                                        ))
        # M.select('[Gmail]/Trash')  # select all trash
        # M.store("1:*", '+FLAGS', '\\Deleted')  #Flag all Trash as Deleted


class MailException(Exception):
    pass


if __name__ == '__main__':
    if (len(sys.argv) < 2 or (sys.argv[1]!="read" and sys.argv[1]!="send")):
        print("add read/send ")
    else:
        mail = MessageNet()
        if(sys.argv[1]=="read"):
            mail.open_read()
            mail.readMessages()
            mail.close_read()
        else:
            if(len(sys.argv) == 2):  mail.sendMessage(raw_input("message:"))
            else :  mail.sendMessage(sys.argv[2])
