'''
Created on Dec 30, 2015

@author: sgorse
'''
import sys
from Tkinter import * 
import tkMessageBox
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
from xml.dom import minidom
import tkFileDialog


buttons = []
entries = []

def prettyPrintET(etNode):
    reader = Sax2.Reader()
    docNode = reader.fromString(ET.tostring(etNode))
    tmpStream = StringIO()
    PrettyPrint(docNode, stream=tmpStream)
    return tmpStream.getvalue()

def createElement(elementName,value,root):
    name = Element(elementName)
    root.append(name)
    name.text = value

def getInfo(entry, element,root, buttonIndex):
    info = entry.get()
    if info:
        if element == "detectorfilereference":
            info = info.replace('/','\\\\')
        else:
            info = info.replace('/','\\')
        buttons[buttonIndex].config(state = DISABLED)
        createElement(element,info,root)
    
def callback():
    path = tkFileDialog.askopenfile()
    print path

def getInfoAndName(entry, element,root, buttonIndex):
    info = entry.get()
    realPath = info.replace('/','\\')
    index = len(realPath) - 1
    while realPath[index] != "\\":
        index = index - 1
    path = realPath[:index]
    if path:
        createElement(element,path,root)
    
    name = realPath[index+1:]
    elementName = element[:-4]
    elementName = elementName + "filename"
    if name:
        buttons[buttonIndex].config(state = DISABLED)
        createElement(elementName,name,root)

def save():
    global savePath
    savePath = tkFileDialog.askdirectory()

def finish(app):
    app.destroy()

def createGUI(root, savePath):
    
    app = Tk()
    app.title("Create Testconfig File")
    app.geometry("650x500+200+200")
    
    frame = Frame(app, width = 800, height = 600, bd = 3)
    frame.pack()
    
    
    
    Label(frame, text="Software Version*").grid(row=0)
    e1 = Entry(frame)
    e1.grid(row=0, column=1)
    button1 = Button(frame, text="Enter", width=20,command = lambda: getInfo(e1, 'softwareversion', root, 0))
    button1.grid(row=0,column = 2)
    buttons.append(button1)
    
    Label(frame, text="Domain*").grid(row=1)
    e2 = Entry(frame)
    e2.grid(row=1, column=1)
    button2 = Button(frame, text="Enter", width=20,command = lambda: getInfo(e2, 'domain', root, 1))
    button2.grid(row=1,column = 2)
    buttons.append(button2)
    
    var1 = StringVar()
    Label(frame, text="Browser Path*").grid(row=2)
    e3 = Entry(frame, textvariable=var1)
    e3.grid(row=2, column=1)
    Button(frame, text="Browse", width=20,command=lambda:var1.set(tkFileDialog.askopenfilename())).grid(row=2,column = 2)
    button3 = Button(frame, text="Enter", width=20,command = lambda: getInfoAndName(e3, 'browserpath', root, 2))
    button3.grid(row=2,column = 3)
    buttons.append(button3)
    
    var2 = StringVar()
    Label(frame, text="CommServer Path*").grid(row=4)
    e5 = Entry(frame, textvariable=var2)
    e5.grid(row=4, column=1)
    Button(frame, text="Browse", width=20,command=lambda:var2.set(tkFileDialog.askopenfilename())).grid(row=4,column = 2)
    button4 = Button(frame, text="Enter", width=20,command = lambda: getInfoAndName(e5, 'commserverpath', root, 3))
    button4.grid(row=4,column = 3)
    buttons.append(button4)
    
    var3 = StringVar()
    Label(frame, text="Detector File Reference").grid(row=6)
    e7 = Entry(frame, textvariable=var3)
    e7.grid(row=6, column=1)
    Button(frame, text="Browse", width=20,command=lambda:var3.set(tkFileDialog.askopenfilename())).grid(row=6,column = 2)
    button5 = Button(frame, text="Enter", width=20,command = lambda: getInfo(e7, 'detectorfilereference', root, 4))
    button5.grid(row=6,column = 3)
    buttons.append(button5)
    
    Label(frame, text="CPU ID*").grid(row=7)
    e8 = Entry(frame)
    e8.grid(row=7, column=1)
    button6 = Button(frame, text="Enter", width=20,command = lambda: getInfo(e8, 'cpuid', root, 5))
    button6.grid(row=7,column = 2)
    buttons.append(button6)
    
    Label(frame, text="IP Address*").grid(row=8)
    e9 = Entry(frame)
    e9.grid(row=8, column=1)
    button7 = Button(frame, text="Enter", width=20,command = lambda: getInfo(e9, 'ipaddress', root, 6))
    button7.grid(row=8,column = 2)
    buttons.append(button7)
    
    var4 = StringVar()
    Label(frame, text="Oplog File Name").grid(row=9)
    e10 = Entry(frame, textvariable=var4)
    e10.grid(row=9, column=1)
    Button(frame, text="Browse", width=20,command=lambda:var4.set(tkFileDialog.askopenfilename())).grid(row=9,column = 2)
    button8 = Button(frame, text="Enter", width=20,command = lambda: getInfo(e10, 'oplogfilename', root, 7))
    button8.grid(row=9,column = 3)
    buttons.append(button8)
    
    Label(frame, text="").grid(row=10)
    
    saveButton = Button(frame, text="Save", width=15,command= (lambda: save()))
    saveButton.grid(row=11,column = 1)
    buttons.append(saveButton)
    
    finishButton = Button(frame, text = "Finish", width = 15, command= (lambda: finish(app)))
    finishButton.grid(row=11, column = 2)
    buttons.append(finishButton)
    app.mainloop()

    
savePath = ""
if __name__ == "__main__":
    root = Element("root")
    tree = ElementTree(root)
    global savePath
    createGUI(root,savePath)
    print minidom.parseString(etree.tostring(root)).toprettyxml(encoding="us-ascii")
    filehandler = open(savePath+"/testconfig.xml","w")
    filehandler.write(minidom.parseString(etree.tostring(root)).toprettyxml(encoding="us-ascii"))