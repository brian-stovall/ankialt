import json, random, sys, os
import datamunger

def cardBuilder(csvFile, cardfile='my-cards.json', sep='\t'):
    try:
        with open(csvFile, 'r') as infile:
            isHeader = True
            header = None
            rank = 0
            mastery = 0
            wait = 0
            dataDict = []
            for line in infile:
                line = line.replace('\n', '')
                if isHeader:
                    header = line.split(sep)
                    isHeader = False
                    continue
                entry = {}
                data = line.split(sep)
                for i in range(0, len(header)):
                    entry[header[i]] = data[i]
                rank = rank + 1
                entry['rank'] = rank
                entry['mastery'] = mastery
                entry['wait'] = 0
                dataDict.append(entry)
            with open(cardfile, 'w') as outfile:
                jsonString = json.dumps(dataDict, indent=4)
                outfile.write(jsonString)
            return 'Success! Made ' + str(len(dataDict)) + ' cards.'
    except Exception as e:
        return e


def study(cardFile, questionsFile):
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

'''
char_cards = 'cards-and-questions/char-cards.json'
char_questions = 'cards-and-questions/char-questions.json'
study(char_cards, char_questions)
'''
#cardBuilder('enriched-joyou')
#makeJoyou()
#enrichJoyou()


