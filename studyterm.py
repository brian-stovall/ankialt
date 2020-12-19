import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import json, random, sys, os

num_studied = 0
font = 'arial 15'

def timePasses(cards, masteryThreshold=20):
    for card in cards:
        if card['mastery'] <= masteryThreshold:
            card['wait'] = max(0, card['wait'] - 1)

def masterCard(card):
    card['mastery'] = card['mastery'] + 1
    card['wait'] = card['mastery'] + 1 #for timePasses

def failCard(card):
    card['wait'] = random.choice(range(1,5))
    card['mastery'] = 0

def quitStudy(cardFile, cards):
    with open(cardFile + '-backup', 'w') as backup:
        with open(cardFile,'r') as source:
            backup.write(source.read())
    with open(cardFile,'w') as outfile:
        outfile.write(json.dumps(cards, indent=4, ensure_ascii=False))
    sys.exit(0)

def getQuestion(questions):
    return random.choice(questions)

def getCard(cardData):
    for i in range(0,len(cardData)):
        if cardData[i]['wait'] == 0:
            return cardData[i]
    messagebox.showinfo('hmm, did not find any cards with wait 0 - ask brian to fix')

def loadjson(jsonfile):
    data = None
    with open(jsonfile, 'r') as infile:
        data = infile.read()
    return json.loads(data)

def init(configfile='quiz-config'):
    lastcards=None
    lastquest=None
    if os.path.exists(configfile):
        with open(configfile, 'r') as conf_file:
            lastcards, lastquest = conf_file.read().split('|')
    prompt = 'Select a card file:'
    if lastcards != None:
        prompt += '(' + lastcards + ')'
    cards = input(prompt) or lastcards
    prompt = 'Select a questions file:'
    if lastquest != None:
        prompt += '(' + lastquest + ')'
    quest = input(prompt) or lastquest
    study(cards, quest, configfile)

def study(cardfile, questionfile, configfile):
    with open(configfile, 'w') as conf_file:
        conf_file.write(cardfile+'|'+ questionfile)
    cards = loadjson(cardfile)
    questions = loadjson(questionfile)
    ask(cards, cardfile, questions)

def ask(cards, cardfile, questions):
    global num_studied
    os.system('clear')
    print('#',num_studied)
    card = getCard(cards)
    question = getQuestion(questions)
    for field in question['question']:
        print(field, str(card[field]))
    print()
    input()
    for field in question['answer']:
        print(field, str(card[field]))
    choice = input('n if not correct - q to quit')
    if choice == 'q':
        quitStudy(cardfile, cards)
    elif choice == None:
        masterCard(card)
    else:
        failCard(card)
    num_studied = num_studied + 1
    ask(cards, cardfile, questions)

init()
