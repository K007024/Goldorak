# coding: utf-8

from Tkinter import *
from lxml import etree
import tkFileDialog
import ttk
import os

import os.path
import subprocess as sub

# size and colors
szMain = 100
szBtSelect = 10
bgcolor = "white"

# usefull
dstPath = ''
srcPath = ''
dictName = ''

def buildMessageFrame(_frame):

    global srcPath
    srcPath = StringVar()
    Label(_frame, text = 'Source').grid(row =0, column = 0, sticky=W)
    Entry(_frame, textvariable = srcPath, width = szMain).grid(row =0, column = 1)
    Button(_frame, text = 'Choose', bg = bgcolor, width = szBtSelect, command=onSrcClick).grid(row =0, column = 2)

    global dstPath
    dstPath = StringVar()
    Label(_frame, text = 'Destination').grid(row =1, column = 0, sticky=W)
    Entry(_frame, textvariable = dstPath, width = szMain).grid(row =1, column = 1)
    Button(_frame, text = 'Choose', bg = bgcolor, width = szBtSelect, command=onDstClick).grid(row =1, column = 2)

    global dictName
    dictName = StringVar()
    Label(_frame, text = 'Dictionary').grid(row =2, column = 0, sticky=W)
    dicBox = ttk.Combobox(_frame, textvariable=dictName, width = szMain - 3)
    dicBox['values'] = tuple([l[0] for l in readConfig()])
    dicBox.current(0)
    dicBox.grid(row =2, column = 1)

    global resBox
    Label(_frame, text = 'Log').grid(row =3, column = 0, sticky=W)
    resBox = Text(_frame, width = szMain - 25)
    resBox.grid(row =3, column = 1, sticky=W)

    Button(_frame, text = 'Goldorak !', bg = bgcolor, width = szBtSelect, command=doGoldorak).grid(row =3, column = 2)
    
    return _frame


def onSrcClick():
    dir = tkFileDialog.askdirectory(title='Choose source directory', initialdir='.')
    if dir:
        global srcPath
        srcPath.set(dir)


def onDstClick():
    dir = tkFileDialog.askdirectory(title='Choose destination directory', initialdir='.')
    if dir:
        global dstPath
        dstPath.set(dir)

def doGoldorak():
    global dstPath
    global srcPath
    global dictName
    global resBox

    source = srcPath.get()
    destination = dstPath.get()
    capteurs = [l[1] for l in readConfig() if l[0] == dictName.get()][0]

    # cmd = '"{} -debug {} {} {}"'.format(app, source, destination, capteurs)
    # os.system(cmd)

    cmd = 'java -cp dossier mafonction {} {} {}"'.format(source, destination, capteurs)
    process = sub.Popen(cmd, stdout=sub.PIPE,stderr=sub.PIPE)

    while True:
        out = process.stdout.readline()
        if out == '' and process.poll() is not None:
            break
        # print out
        resBox.insert(END, out)
        resBox.see(END)
        resBox.update_idletasks()
        
    print 'done'

        
def readConfig():
    tree = etree.parse("Goldorak.cfg")
    res = [(kit.get("name"), kit.text) for kit in tree.xpath("/config/dict")]
    return res
    
    
if __name__ == "__main__":

    memStdout = sys.stdout # memoire

    fenetre = Tk()
    fenetre.title("Goldorak GUI")
    fenetre.resizable(width="FALSE", height="FALSE")

    messageFrame = Frame(fenetre)
    messageFrame.grid(row = 0)
    messageFrame = buildMessageFrame(messageFrame)
    # win.update_idletasks()
    fenetre.mainloop()
   
    sys.stdout = memStdout # remise en etat