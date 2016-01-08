'''
Created on Dec 30, 2015

@author: sgorse
'''
import sys
from Tkinter import * 
import tkMessageBox
from tkMessageBox import showerror
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
from xml.dom import minidom
import tkFileDialog


buttons = []
entries = []
vars = []
elementTexts = ["","","","","","","","","",""]
uploadCounter = 0

def getElementText(element,root):
    global uploadCounter
    softwareversion = root.find(element)
    elementTexts[uploadCounter] = softwareversion.text
    uploadCounter = uploadCounter + 1

def putTextInEntry(entryIndex):
    if (entryIndex == 0) or (entryIndex == 1) or (entryIndex == 4) or (entryIndex == 5) or (entryIndex == 6) or (entryIndex == 7):
        if entryIndex == 0:
            vars[0].set(elementTexts[0])
        elif entryIndex == 1:
            vars[1].set(elementTexts[1])
        elif entryIndex == 4:
            vars[4].set(elementTexts[6])
        elif entryIndex == 5:
            vars[5].set(elementTexts[7])
        elif entryIndex == 6:
            vars[6].set(elementTexts[8])
        else:
            vars[7].set(elementTexts[9])
    else:
        if (entryIndex == 2):
            vars[2].set(elementTexts[2] + '\\' + elementTexts[3])
        else:
            vars[3].set(elementTexts[4] + '\\' + elementTexts[5])
        
            
    

def prettyPrintET(etNode):
    reader = Sax2.Reader()
    docNode = reader.fromString(ET.tostring(etNode))
    tmpStream = StringIO()
    PrettyPrint(docNode, stream=tmpStream)
    return tmpStream.getvalue()

def createElement(elementName,value,root):
    name = Element(elementName)
    root.append(name)
    if value:
        name.text = value
    else:
        name.text = " "

def getInfo(entry, element,root):
    info = entry.get()
    if element == "detectorfilereference":
        info = info.replace('/','\\\\')
    else:
        info = info.replace('/','\\')
    createElement(element,info,root)
    
def callback():
    path = tkFileDialog.askopenfile()
    print path

def getInfoAndName(entry, element,root):
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
        createElement(elementName,name,root)

def save():
    global savePath
    savePath = tkFileDialog.askdirectory()
    
def upload():
    global uploadPath
    global uploadCounter
    uploadPath = tkFileDialog.askopenfile()
    root = ET.parse(uploadPath)
    getElementText("softwareversion",root)
    getElementText("domain",root)
    getElementText("browserpath",root)
    getElementText("browserfilename",root)
    getElementText("commserverpath",root)
    getElementText("commserverfilename",root)
    getElementText("detectorfilereference",root)
    getElementText("cpuid",root)
    getElementText("ipaddress",root)
    getElementText("oplogfilename",root)
    i = 0
    uploadCounter = 0
    putTextInEntry(0)
    putTextInEntry(1)
    putTextInEntry(2)
    putTextInEntry(3)
    putTextInEntry(4)
    putTextInEntry(5)
    putTextInEntry(6)
    putTextInEntry(7)
    
    
def finish(app, root):
    if (len(entries[0].get())!=0) and (len(entries[1].get())!=0) and (len(entries[2].get())!=0 and (len(entries[3].get())!=0)) and (len(entries[5].get())!=0) and (len(entries[6].get())!=0):
        if savePath:
            getInfo(entries[0],'softwareversion', root)
            getInfo(entries[1],'domain', root)
            getInfoAndName(entries[2],'browserpath', root)
            getInfoAndName(entries[3],'commserverpath',root)
            getInfo(entries[4],'detectorfilereference',root)
            getInfo(entries[5],'cpuid',root)
            getInfo(entries[6],'ipaddress', root)
            getInfo(entries[7],'oplogfilename',root)
            app.destroy()
        else:
            showerror(title = "Error", message = "Please choose a directory to save the file to.")
        
    else:
        showerror(title = "Error", message = "All the necessary entries were not filled. Please fill in all the entries with an * in front.")
        
    

def createGUI(root, savePath):
    
    app = Tk()
    app.title("Create Testconfig File")
    app.geometry("650x500+200+200")
    
    frame = Frame(app, width = 780, height = 600, bd = 3)
    frame.pack()
    
    var1 = StringVar()
    Label(frame, text="Software Version*").grid(row=0)
    e1 = Entry(frame, textvariable=var1)
    e1.grid(row=0, column=1)
    entries.append(e1)
    vars.append(var1)
    
    var2=StringVar()
    Label(frame, text="Domain*").grid(row=1)
    e2 = Entry(frame, textvariable=var2)
    e2.grid(row=1, column=1)
    entries.append(e2)
    vars.append(var2)
    
    var3 = StringVar()
    Label(frame, text="Browser Path*").grid(row=2)
    e3 = Entry(frame, textvariable=var3)
    e3.grid(row=2, column=1)
    Button(frame, text="Browse", width=20,command=lambda:var3.set(tkFileDialog.askopenfilename())).grid(row=2,column = 2)
    entries.append(e3)
    vars.append(var3)
    
    var4 = StringVar()
    Label(frame, text="CommServer Path*").grid(row=4)
    e4 = Entry(frame, textvariable=var4)
    e4.grid(row=4, column=1)
    Button(frame, text="Browse", width=20,command=lambda:var4.set(tkFileDialog.askopenfilename())).grid(row=4,column = 2)
    entries.append(e4)
    vars.append(var4)
    
    var5 = StringVar()
    Label(frame, text="Detector File Reference").grid(row=6)
    e5 = Entry(frame, textvariable=var5)
    e5.grid(row=6, column=1)
    Button(frame, text="Browse", width=20,command=lambda:var5.set(tkFileDialog.askopenfilename())).grid(row=6,column = 2)
    entries.append(e5)
    vars.append(var5)
    
    var6 = StringVar()
    Label(frame, text="CPU ID*").grid(row=7)
    e6 = Entry(frame, textvariable=var6)
    e6.grid(row=7, column=1)
    entries.append(e6)
    vars.append(var6)
    
    var7 = StringVar()
    Label(frame, text="IP Address*").grid(row=8)
    e7 = Entry(frame, textvariable=var7)
    e7.grid(row=8, column=1)
    entries.append(e7)
    vars.append(var7)
    
    var8 = StringVar()
    Label(frame, text="Oplog File Name").grid(row=9)
    e8 = Entry(frame, textvariable=var8)
    e8.grid(row=9, column=1)
    Button(frame, text="Browse", width=20,command=lambda:var8.set(tkFileDialog.askopenfilename())).grid(row=9,column = 2)
    entries.append(e8)
    vars.append(var8)
    
    Label(frame, text="").grid(row=10)
    
    uploadButton = Button(frame, text = "Upload File", width =15, command = (lambda: upload()))
    uploadButton.grid(row=11,column = 0)
    
    saveButton = Button(frame, text="Save", width=15,command= (lambda: save()))
    saveButton.grid(row=11,column = 1)
    
    finishButton = Button(frame, text = "Finish", width = 15, command= (lambda: finish(app, root)))
    finishButton.grid(row=11, column = 2)
    app.mainloop()

    
savePath = ""
uploadPath = ""
if __name__ == "__main__":
    root = Element("root")
    tree = ElementTree(root)
    createGUI(root,savePath)
    print minidom.parseString(etree.tostring(root)).toprettyxml(encoding="us-ascii")
    filehandler = open(savePath+"/testconfig.xml","w")
    filehandler.write(minidom.parseString(etree.tostring(root)).toprettyxml(encoding="us-ascii"))