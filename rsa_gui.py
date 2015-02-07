#! /usr/bin/python3

from tkinter import *
from rsa_nogui import *
import tkinter.filedialog as filedialog
from time import sleep
import os

computers = {
    "myself":[M, P]             #usually contains more, as if you could send to other people
}

win = Tk()
win.title("RSA encryption-python")
entrybar = Frame(win)
buttons = Frame(win)
file_list = Frame(win)

s_entry = Text(entrybar, width=25, height=5)
input_label = Label(entrybar, text="Input")
input_label.pack(pady=5)
s_entry.pack(expand=1,fill=BOTH,padx=5)

filename = StringVar()
f_entry = Entry(buttons, textvariable=filename)
people = Listbox(buttons, selectmode=BROWSE)
for person in computers:
    people.insert(END, person)

en_files = Listbox(file_list, selectmode=BROWSE)

file_path = os.getcwd()

def refresh():
    files=[]
    en_files.delete(0, END)
    global file_path
    for file in os.listdir(file_path):
        if file.endswith(".rsa"):
            files.append(file)
    for file in files:
        en_files.insert(END, file)

def refresh_path():
    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir="/", title="Select the folder with Encrypted files")
    global file_path
    file_path = str(directory)
    root.destroy()
    refresh()

file_label = Label(file_list, text="Select file:")
file_list2 = Frame(file_list)
path_refresh = Button(file_list2, text="Choose folder", command=refresh_path)
file_label.pack(pady=3)
en_files.pack()
path_refresh.pack(padx=5,pady=2)
file_list2.pack()

def encode_click():
    with open(file_path + "/" + filename.get() + ".rsa", 'w') as writefile:
        writefile.write(encode_text(s_entry.get(1.0, END)[0:len(s_entry.get(1.0, END))-1],\
                  computers[people.get(ACTIVE)][0],computers[people.get(ACTIVE)][1]))                   
    refresh()

def decode_click():
    with open(file_path + "/" + en_files.get(ACTIVE)) as readfile:
        s_entry.insert(END, decode_text( readfile.read(), M, D ))
    refresh()

encrypt = Button(buttons, text="Encode", command=encode_click)
decrypt = Button(buttons, text="Decode", command=decode_click)
encrypt.pack(padx=10, pady=2)
decrypt.pack(padx=10, pady=2)
f_entry.pack()
people.pack()

entrybar.pack(side=LEFT, expand=1, fill=BOTH, pady=5, padx=5)
buttons.pack(side=LEFT)
file_list.pack(side=LEFT, padx=5)
refresh()
win.mainloop()
quit()
