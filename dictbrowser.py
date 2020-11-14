import tkinter as tk
from tkinter import ttk
import json

def init(win):
    unihan = None
    edict = None
    edict_result = []
    uni_result = {}
    with open('./dicts/unihan.json') as infile:
        unihan=json.loads(infile.read())
    with open('./dicts/edict.json') as infile:
        edict=json.loads(infile.read())
    eFrame = tk.Frame(win)
    dframe = tk.Frame(win)
    entry = tk.Entry(eFrame)
    sep = ttk.Separator(win)
    win.bind('<Return>', lambda i: lookup(entry, unihan, edict, edict_result, uni_result, dframe))
    entry.pack()
    eFrame.pack()
    sep.pack(fill='x')
    entry.focus_set()

def lookup(entry, unihan, edict, edict_result, uni_result, dframe):
    value = entry.get()
    entry.delete(0, 'end')
    for widget in dframe.winfo_children():
        widget.destroy()
    if value in edict.keys():
         edict_result = edict[value]
    else:
        edict_result=[]
    for character in value:
        if character in unihan.keys():
            uni_result[character]=unihan[character]
    print(edict_result, uni_result)
    display_result(value, edict_result, uni_result, dframe)

def make_meaning_line(meaning, frame):
    line = tk.Entry(frame, state='readonly', fg='black', width=40)
    var = tk.StringVar()
    var.set(meaning)
    line.config(textvariable=var, relief='flat')
    return line

def display_result(value, edict_result, uni_result, dframe):
    maxmeanings = 3
    edictFrame = tk.Frame(dframe)
    meaninglines = [make_meaning_line(meaning, edictFrame) for meaning in edict_result]
    if len(meaninglines) == 0:
        meaninglines = [make_meaning_line('not in dictionary!', edictFrame)]
    if len(meaninglines) > maxmeanings:
        meaninglines = meaninglines[0:maxmeanings]
    for line in meaninglines:
        line.pack()
    edictFrame.pack()
    dframe.pack()



def main():
    win = tk.Tk()
    win.title('dictionary!')
    init(win)
    win.mainloop()

main()
