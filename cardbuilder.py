import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from dictmake import cardBuilder
win = tk.Tk()

def pickFile(entry):
    filename = tk.filedialog.askopenfilename(title = 'Select file to make cards from')
    entry.delete(0, 'end')
    entry.insert(0, filename)

def saveFile(entry):
    filename = tk.filedialog.asksaveasfilename(title = 'Select file to save cards to')
    entry.delete(0, 'end')
    entry.insert(0, filename)

def letsGo(infile, outfile, sep):
    if sep == 'other':
        sep = sepEntry.get()
    messagebox.showinfo("Result!", cardBuilder(infile,outfile,sep))

win.title("Let's make cards!")
win.geometry('300x450')
#file select
fileSelectFrame = tk.Frame(win)
fileSelectLabel = tk.Label(fileSelectFrame, text = '1: Select a file to make cards from')
fileEntry = tk.Entry(fileSelectFrame, width=20)
browseButton = tk.Button(fileSelectFrame, text='Browse', command=lambda: pickFile(fileEntry))
fsSep = ttk.Separator(fileSelectFrame)
fileSelectLabel.pack()
fileEntry.pack()
browseButton.pack()
fileSelectFrame.pack()
fsSep.pack(fill='x', pady=4)
#separator select
sepFrame = tk.Frame(win)
sepVar = tk.StringVar()
sepLabel = tk.Label(sepFrame, text = '2: Choose the separator the file uses')
RB1 = tk.Radiobutton(sepFrame, text = 'Tab separated', variable = sepVar, value = '\t')
RB2 = tk.Radiobutton(sepFrame, text = 'Comma separated', variable = sepVar, value = ',')
RB3 = tk.Radiobutton(sepFrame, text = 'Semicolon separated', variable = sepVar, value = ';')
RB4 = tk.Radiobutton(sepFrame, text = 'Other, please type in box below', variable = sepVar, value = 'other')
sepEntry = tk.Entry(sepFrame, width=2)
sepSep = ttk.Separator(sepFrame)
for thing in [sepLabel, RB1, RB2, RB3, RB4, sepEntry, sepFrame]:
    thing.pack()
sepSep.pack(fill='x', pady=4)
#outfile select
outFrame = tk.Frame(win)
outLabel = tk.Label(outFrame, text = '3: Choose or create an output file')
outEntry = tk.Entry(outFrame, width=20)
outButton = tk.Button(outFrame, text='Choose', command=lambda: saveFile(outEntry))
outSep = ttk.Separator(outFrame)
for thing in [outLabel, outEntry, outButton, outFrame]:
    thing.pack()
outSep.pack(fill='x', pady=4)
#go!
goFrame = tk.Frame(win)
goButton = tk.Button(goFrame, text="Let's go!", command = lambda : letsGo(fileEntry.get(),outEntry.get(), sepVar.get()))
goButton.pack()
goFrame.pack()
#cardBuilder(fileEntry.get(),
win.mainloop()

