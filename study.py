import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import json, random, sys

def timePasses(cards):
    for card in cards:
        card['wait'] = max(0, card['wait'] - 1)

def masterCard(card):
    card['mastery'] = card['mastery'] + 1
    card['wait'] = card['mastery'] + 1 #for timePasses

def failCard(card):
    card['wait'] = random.choice(range(5,11))
    card['mastery'] = 0

def getCorrect():
    choice = input('correct? n for no, anything else for yes: ')
    if choice.lower() == 'n':
        return False
    else:
        return True

def quitStudy(cardFile, cards):
    with open(cardFile + '-backup', 'w') as backup:
        with open(cardFile,'r') as source:
            backup.write(source.read())
    with open(cardFile,'w') as outfile:
        outfile.write(json.dumps(cards, indent=4))
    messagebox.showinfo('Bye now!', 'wrote backup to' + str(backup.name) + ' and saved your work... bye!')
    sys.exit(0)

def getQuestion(questions):
    return random.choice(questions)

def getCard(cardData):
    for i in range(0,len(cardData)):
        if cardData[i]['wait'] == 0:
            return cardData[i]
    print('hmm, did not find any cards with wait 0 - ask brian to fix')

def loadjson(jsonfile):
    data = None
    with open(jsonfile, 'r') as infile:
        data = infile.read()
    return json.loads(data)

def chooseFile(entry):
    filename = tk.filedialog.askopenfilename(title = 'Select file to make cards from')
    entry.delete(0, 'end')
    entry.insert(0, filename)

def packer(thinglist, padx=0, pady=0, toppady=0):
    firstThing = True
    for thing in thinglist:
        fill = None
        if firstThing:
            thing.pack(padx=padx, pady=toppady)
            firstThing = False
        if isinstance(thing, ttk.Separator):
            fill = 'x'
        thing.pack(padx=padx, pady=pady, fill=fill)

def hider(thinglist):
    for thing in thinglist:
        thing.pack_forget()

def init(win):
    win.minsize(500,300)
    iFrame = tk.Frame(win)
    iFrame.pady = 150
    iLabel = tk.Label(iFrame,
        text='Choose a card and question file to begin.')
    ccFrame = tk.Frame(iFrame)
    ccEntry = tk.Entry(ccFrame)
    ccButton = tk.Button(ccFrame, text='Select cards',
        command=lambda:chooseFile(ccEntry))
    cqFrame = tk.Frame(iFrame)
    cqEntry = tk.Entry(cqFrame)
    cqButton = tk.Button(cqFrame, text='Select questions',
        command=lambda:chooseFile(cqEntry))
    sep = ttk.Separator(iFrame)
    startButton = tk.Button(iFrame, text='Start study',
        command=lambda:study(win, ccEntry.get(), cqEntry.get(), initThings))
    initThings = [iLabel, ccEntry, ccButton, ccFrame, cqEntry, cqButton, cqFrame,
        iFrame, sep, startButton]
    packer(initThings, pady=7)


def makeline(parentframe, field, card):
    lineframe = tk.Frame(parentframe)
    font = 'arial 15 bold'
    #thelabel = tk.Label(lineframe, text=field, font=font)
    dataText=field + ': ' + str(card[field])
    maxlen = 40
    if len(dataText) > maxlen:
        dataText = '\n'.join([dataText[i:i+maxlen] \
            for i in range(0, len(dataText), maxlen)])
    thedata = tk.Label(lineframe, text=dataText, font=font)
    #thelabel.pack(side='left')
    thedata.pack(side='right')
    lineframe.pack(pady=3)

def ask(win, cards, questions):
    askFrame = tk.Frame(win)
    qFrame = tk.Frame(askFrame)
    card = getCard(cards)
    question = getQuestion(questions)
    for field in question['question']:
        makeline(qFrame, field, card)
    qFrame.pack()
    askFrame.pack()
    askEntry = tk.Entry(qFrame)
    askSep = ttk.Separator(qFrame)
    askSep.pack(fill='x')
    answerFrame = tk.Frame(askFrame)
    for field in question['answer']:
        makeline(answerFrame, field, card)
    correctBtn = tk.Button(answerFrame, text='1: correct', command=lambda: askAgain(True, card, askFrame, win, cards, questions))
    wrongBtn = tk.Button(answerFrame, text='2: incorrect', command=lambda: askAgain(False, card, askFrame, win, cards, questions))
    correctBtn.pack(pady=3)
    wrongBtn.pack(pady=3)
    win.bind('<Return>', lambda i: answerFrame.pack())
    win.bind('1', lambda i: correctBtn.invoke())
    win.bind('2', lambda i: correctBtn.invoke())

def askAgain(correct, card, askFrame, win, cards, questions):
    timePasses(cards)
    if correct:
        masterCard(card)
    else:
        failCard(card)
    askFrame.destroy()
    ask(win,cards,questions)

def study(win, cardfile, questionfile, initThings):
    cards = loadjson(cardfile)
    questions = loadjson(questionfile)
    hider(initThings)
    win.protocol('WM_DELETE_WINDOW', lambda: quitStudy(cardfile, cards))
    ask(win,cards,questions)

def main():
    win = tk.Tk()
    win.title('Study time')
    #win.geometry('1200x800')
    init(win)
    win.mainloop()
    '''
    qFrame = tk.Frame(win)
    aFrame = tk.Frame(win)
    toolsFrame = tk.Frame(win)
    quitButton = tk.Button(toolsFrame, text='Finish session',
        command=lambda:)
    '''

main()
