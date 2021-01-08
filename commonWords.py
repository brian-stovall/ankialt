import json, sys, os, time, random, subprocess
start = None
errorcount = 0
thisWindowID = None
kitenWindowID = None
globalErrors = set()

def load():
    data = None
    datafile = '/home/artiste/quizlet/dicts/freq-data'
    with open(datafile, 'r') as worddata:
        data = worddata.read()
    return json.loads(data)

def getUnihan():
    unihan = None
    with open('/home/artiste/quizlet/dicts/unihan.json') as infile:
        unihan=json.loads(infile.read())
    return unihan

def getPreviousErrors():
    pe = None
    with open('./lastErrors-words') as infile:
        pe=json.loads(infile.read())
    return pe

def kitenLookup(target):
    #sleeptime = 0.3
    delaytime = '50'
    #subprocess.call(['xdotool', 'windowactivate', '--sync', kitenWindowID])
    subprocess.call(['xdotool', 'key', '--window', kitenWindowID, '--clearmodifiers', 'Ctrl+l'])
    #time.sleep(sleeptime)
    subprocess.call(['xdotool', 'type', '--window', kitenWindowID, target])
    #time.sleep(sleeptime)
    subprocess.call(['xdotool', 'key', '--window', kitenWindowID, 'Return'])
    #subprocess.call(['xdotool', 'windowactivate', '--sync', thisWindowID])

def begin():
    global thisWindowID
    global kitenWindowID
    thisWindowID = input('terminal window id?')
    kitenWindowID = input('kiten window id?')
    begin = None
    end = None
    jsondata = None
    studyData = []
    unihan = getUnihan()
    choice = input('Study previous errors?')
    if choice == 'y':
        jsondata = getPreviousErrors()
    else:
        begin = int(input('Start with which entry?'))
        end = int(input('End with which entry?'))
        jsondata = load()
        for num in range(begin, end +1):
            studyData.append(jsondata[str(num)])
    random.shuffle(studyData)
    test(unihan, studyData)

def end():
    global globalErrors
    with open('lastErrors', 'w') as myerrors:
        myerrors.write(json.dumps(list(globalErrors), ensure_ascii=False))

def lookup(unihan, symbol):
    unidata = unihan[symbol]
    print(symbol, ''.join(unidata['pinyin']), ''.join(unidata['definition']))

def test(unihan, jsondata, frame = 1):
    global errorcount
    global start
    errors = []
    if start == None:
        start = time.time()
    for entry in jsondata:
        word = entry['word']
        rank = entry['rank']
        os.system('clear')
        print(word, rank)
        print()
        input()
        for symbol in word:
            if symbol in unihan.keys():
                lookup(unihan, symbol)
        kitenLookup(word)
        print()
        choice = input('n if not correct - q to quit')
        if 'q' in choice:
            sys.exit(0)
        elif 'n' in choice:
            errorcount += 1
            errors.append(symbol)
            globalErrors.add(symbol)
    print('frame', frame, ' errors:', len(errors), ' total:', len(jsondata))
    if len(errors) > 0:
        input('enter to continue to next frame')
        test(unihan, errors, frame +1)
    else:
        elapsed = time.time() - start
        minutes = elapsed / 60.0
        print('good job! ', minutes, ' min ', errorcount, ' errors')
        input()
        end()

#begin()



