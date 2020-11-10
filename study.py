import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import json, random

'''
def study2(cardFile, questionsFile):
    cards = None
    questions = None
    with open(cardFile,'r') as infile:
        cards = json.loads(infile.read())
    with open(questionsFile,'r') as infile:
        questions = json.loads(infile.read())
    goAgain = True
    while goAgain:
        goAgain = ask(getCard(cards), getQuestion(questions), cardFile, cards)
    quitStudy(cardFile, cards)

def ask(card, question, cardFile, cards):
    front = []
    back = []
    os.system('clear')
    for field in question['question']:
        front.append(field + ':\t' + card[field])
    for field in question['answer']:
        back.append(field + ':\t' + card[field])
    print('\n'.join(front))
    isQuit = input('\n<enter to see answer, q to quit>\n')
    if isQuit.lower() == 'q':
        return False
    else:
        print('\n'.join(back))
    if getCorrect():
        masterCard(card)
    else:
        failCard(card)
    timePasses(cards)
    print('mastery: ', card['mastery'])
    print('new wait: ', card['wait'])
    input('<enter to continue>')
    return True
'''

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
            print('wrote backup to', backup)
    with open(cardFile,'w') as outfile:
        outfile.write(json.dumps(cards, indent=4))
    print('wrote state, bye!')
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
    win.geometry('300x300')
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
    thelabel = tk.Label(lineframe, text=field, font=font)
    thedata = tk.Label(lineframe, text=str(card[field]))
    thelabel.pack(side='left')
    thedata.pack(side='right')
    lineframe.pack()
    #packer([thelabel, thedata, lineframe])

def ask(win, cards, questions):
    card = getCard(cards)
    question = getQuestion(questions)
    for field in question['question']:
        makeline(win, field, card)
    #TODO hit enter to see answer


def study(win, cardfile, questionfile, initThings):
    cards = loadjson(cardfile)
    questions = loadjson(questionfile)
    hider(initThings)
    askB = tk.Button(win,text='ask',
        command=lambda:ask(win,cards,questions))
    askB.pack()


def main():
    win = tk.Tk()
    win.title('Study time')
    win.geometry('600x600')
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
