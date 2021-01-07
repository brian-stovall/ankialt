import json, sys, os, time, random
start = None
errorcount = 0
globalErrors = set()

def load():
    data = None
    datafile = '/home/artiste/Desktop/aozora.json'
    with open(datafile, 'r') as kanjidata:
        data = kanjidata.read()
    return json.loads(data)

def getUnihan():
    unihan = None
    with open('/home/artiste/quizlet/dicts/unihan.json') as infile:
        unihan=json.loads(infile.read())
    return unihan

def getPreviousErrors():
    pe = None
    with open('./lastErrors') as infile:
        pe=json.loads(infile.read())
    return pe

def begin():
    begin = None
    end = None
    jsondata = None
    unihan = getUnihan()
    choice = input('Study previous errors?')
    if choice == 'y':
        jsondata = getPreviousErrors()
    else:
        begin = int(input('Start with which entry?')) - 1
        end = int(input('End with which entry?'))
        jsondata = load()[begin : end]
    random.shuffle(jsondata)
    test(unihan, jsondata)

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
        symbol = entry[0]
        os.system('clear')
        print(symbol)
        print()
        input()
        lookup(unihan, symbol)
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

begin()



