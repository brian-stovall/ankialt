import tkinter as tk
from tkinter import ttk
import json

def init(win):
    win.minsize(500,300)
    unihan = None
    edict = None
    edict_result = []
    with open('./dicts/unihan.json') as infile:
        unihan=json.loads(infile.read())
    with open('./dicts/edict.json') as infile:
        edict=json.loads(infile.read())
    eFrame = tk.Frame(win)
    dframe = tk.Frame(win)
    entry = tk.Entry(eFrame)
    sep = ttk.Separator(win)
    win.bind('<Return>', lambda i: lookup(entry, unihan, edict, edict_result, dframe))
    entry.pack()
    eFrame.pack()
    sep.pack(fill='x')
    entry.focus_set()

def lookup(entry, unihan, edict, edict_result, dframe):
    uni_result = {}
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
    #print(edict_result, uni_result)
    display_result(value, edict_result, uni_result, dframe)

def make_meaning_line(meaning, frame):
    line = tk.Entry(frame, state='readonly', fg='black', width=40)
    var = tk.StringVar()
    var.set(meaning)
    line.config(textvariable=var, relief='flat')
    return line

def make_unihan_lines(char, uni, frame):
    pinyin = None
    definition = None
    onyomi = None
    variations = []
    lines = []
    if 'pinyin' in uni.keys():
        pinyin = uni['pinyin']
    if 'definition' in uni.keys():
        definition = '; '.join(uni['definition'])
    if pinyin == None and 'onyomi' in uni.keys():
        onyomi = uni['onyomi']
    if 'variant-traditional' in uni.keys():
        variations.extend(uni['variant-traditional'])
    if 'variant-simplified' in uni.keys():
        variations.extend(uni['variant-simplified'])
    if len(variations) > 0:
        variations = 'Variations: ' + ' '.join(variations)
    else:
        variations = None
    for thing in [char, pinyin, onyomi, definition, variations]:
        if thing is not None and thing is not []:
            line = tk.Entry(frame, state='readonly', fg='black', width=40)
            var = tk.StringVar()
            var.set(thing)
            line.config(textvariable=var, relief='flat')
            lines.append(line)
    sep = ttk.Separator(frame)
    lines.append(sep)
    return lines

def display_result(value, edict_result, uni_result, dframe):
    maxmeanings = 3
    edictFrame = tk.Frame(dframe)
    valueline = make_meaning_line(value, edictFrame)
    meaninglines = [make_meaning_line(meaning, edictFrame) for meaning in edict_result]
    if len(meaninglines) == 0:
        meaninglines = [make_meaning_line('not in dictionary!', edictFrame)]
    if len(meaninglines) > maxmeanings:
        meaninglines = meaninglines[0:maxmeanings]
    valueline.pack()
    for line in meaninglines:
        line.pack()
    esep = ttk.Separator(edictFrame)
    esep.pack(fill='x')
    unihanFrame = tk.Frame(dframe)
    unilines = []
    for char in uni_result.keys():
        unilines.extend(make_unihan_lines(char, uni_result[char], unihanFrame))
    if len(meaninglines) == 0:
        unilines = [make_meaning_line('no chars in unihan!', unihanFrame)]
    for line in unilines:
        fill = None
        if isinstance(line, ttk.Separator):
            fill = 'x'
        line.pack(fill=fill)
    edictFrame.pack()
    unihanFrame.pack()
    dframe.pack()



def main():
    win = tk.Tk()
    win.title('dictionary!')
    init(win)
    win.mainloop()

main()
