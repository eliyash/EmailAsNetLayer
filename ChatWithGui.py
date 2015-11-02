#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from time import sleep
from threading import Thread
from MessageNet import MessageNet

import Tkinter

# TODO: add diffrent color for diffrent users, and paint the user other then the massage
# TODO: use FIFO for massages so there will be no mutux
def printLoop():
    # print("readLoop")
    global mail,textBox
    mail.open_read()
    print("readLoop")
    while True:
        for data in mail.readMessages():
            textBox.insert('insert',"%s @ %s: '%s'\n"%(data['machin_other'],data['email_other'],data['Massage']))
            # textBox.grid(column=2,row=2)
            # print("%s@%s: '%s'\n"%(data['machin_other'],data['email_other'],data['Massage']))
        sleep(0.1)
    mail.close_read()

def sendLoop(massage):
    mail.sendMessage(massage)

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        global mail,textBox
        self.grid()

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=1,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter text here.")

        button = Tkinter.Button(self,text=u"Send", command=self.OnButtonClick)
        button.grid(column=1,row=1)

        # NOTE: just for location
        w = 650 # width for the Tk root
        h = 450 # height for the Tk root

        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))


        self.resizable(True,False)
        # NOTE: log window
        textBox = Tkinter.Text(self)
        textBox.insert('insert',"--------------------< RECIEVED CHAT >-----------------------\n")
        textBox.grid(column=0,row=0,columnspan=2)
        # textBox.pack(anchor = "w", padx = 50, pady = 50)

    def OnButtonClick(self):#TODO: remove du
        global mail,textBox
        textBox.insert('insert',"You sent: " + self.entryVariable.get()+'\n' )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        Thread(target=sendLoop,args=(self.entryVariable.get(),)).start()

    def OnPressEnter(self,event):
        global mail,textBox
        textBox.insert('insert',"You sent: " + self.entryVariable.get()+'\n' )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        Thread(target=sendLoop,args=(self.entryVariable.get(),)).start()


if __name__ == '__main__':
    global mail,textBox
    if (len(sys.argv) < 2):
        print ("error , add json file")
    else:
        print("----------< CHAT STARTED >-------------")
        mail = MessageNet(sys.argv[1])
        app = simpleapp_tk(None)
        app.title('Chat using Gmail!')
        readingLoop = Thread(target=printLoop)
        readingLoop.start()
        app.mainloop()
