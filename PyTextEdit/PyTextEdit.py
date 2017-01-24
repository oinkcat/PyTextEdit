# coding: utf-8

from Tkinter import *
import tkFileDialog as dialogs
import tkMessageBox as msgs
import os.path as path

NAME = u'Text editor'

wnd = None
modified = False
txt = None

def createUI():
    global wnd, txt

    wnd = Tk()
    wnd.title(NAME)
    wnd.protocol('WM_DELETE_WINDOW', exit)

    mainMenu = Menu(wnd)
    fileMenu=Menu(mainMenu,tearoff=0)
    fileMenu.add_command(label=u'New', command=newFile)
    fileMenu.add_command(label=u'Open...', command=openFile)
    fileMenu.add_command(label=u'Save as...', command=saveFile)
    fileMenu.add_separator()
    fileMenu.add_command(label=u'Exit', command=exit)
    mainMenu.add_cascade(label=u'File', menu=fileMenu)
    wnd.config(menu=mainMenu)

    txt = Text(wnd, width=100, height=40)
    yscrollbar = Scrollbar(wnd, orient=VERTICAL, command=txt.yview)
    yscrollbar.pack(side=RIGHT, fill=Y)
    txt['yscrollcommand'] = yscrollbar.set
    txt.bind('<<Modified>>', setModified)
    txt.pack(fill=BOTH, anchor=S, expand=YES)

def exit():
    if askSaveIfModified():
        wnd.destroy()

def askSaveIfModified():
    canContinue = True
    if modified:
        answer = msgs.askyesnocancel(u'Text has been modified', 
                                     u'Text has been modified. Save changes?')
        if answer == True:
            canContinue = saveFile()
        else:
            canContinue = answer is not None
    return canContinue

def clear():
    txt.delete('1.0', END)
    clearModified()

def newFile():
    if askSaveIfModified():
        clear()

def openFile():
    if askSaveIfModified():
        fileName = dialogs.askopenfilename(
            title=u'Open text file',
            filetypes=[(u'Plain text files', '*.txt')]
            )
        if path.exists(fileName):
            clear()
            readFile = open(fileName)
            text = readFile.read()
            readFile.close()
            txt.insert('1.0', text)
            txt.mark_set('insert', '1.0')
            clearModified()

def saveFile():
    saved = False
    if modified:
        fileName = dialogs.asksaveasfilename(
            title=u'Save text file',
            filetypes=[(u'Plain text files', '*.txt')],
            defaultextension='.txt'
            )
        if path.exists(fileName):
            writeFile = open(fileName, 'w')
            text = txt.get('1.0', END)
            writeFile.write(text)
            writeFile.close()
            saved = True
            clearModified()
    return saved

def clearModified():
    global modified
    txt.edit_modified(False)
    modified = False

def setModified(event):
    global modified
    modified = True

if __name__ == '__main__':
    createUI()
    mainloop()