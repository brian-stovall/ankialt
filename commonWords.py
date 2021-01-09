import json, sys, os, time, random
start = None
errorcount = 0
globalErrors = set()

def load():
    data = None
    datafile = '/home/artiste/quizlet/commonWords.json'
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
    with open('./lastErrors-words') as infile:
        pe=json.loads(infile.read())
    return pe

def begin():
    begin = None
    end = None
    jsondata = None
    unihan = getUnihan()
    #choice = input('Study previous errors?')
    #if choice == 'y':
    #    jsondata = getPreviousErrors()
    if False:
        pass
    else:
        begin = int(input('Start with which entry?')) - 1
        end = int(input('End with which entry?'))
        jsondata = load()[begin : end]
    random.shuffle(jsondata)
    test(unihan, jsondata)

def end():
    global globalErrors
    with open('lastErrors-words', 'w') as myerrors:
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
        os.system('clear')
        print(word)
        if entry['sentence'] is not None:
            print(entry['sentence'])
        print()
        input()
        print(entry['definition'])
        if entry['sentence'] is not None:
            print(entry['translation'])
        if entry['sentence'] is not None:
            for char in entry['sentence']:
                if char in unihan.keys():
                    lookup(unihan, char)
        else:
            for symbol in word:
                if symbol in unihan.keys():
                    lookup(unihan, symbol)
        print()
        choice = input('n if not correct - q to quit')
        if 'q' in choice:
            sys.exit(0)
        elif 'n' in choice:
            errorcount += 1
            #errors.append(entry)
            #globalErrors.add(entry)
    print('frame', frame, ' errors:', errorcount, ' total:', len(jsondata))
    if len(errors) > 0:
        input('enter to continue to next frame')
        test(unihan, errorcount, frame +1)
    else:
        elapsed = time.time() - start
        minutes = elapsed / 60.0
        print('good job! ', minutes, ' minutes, ', errorcount, ' errors')
        input()
        end()

begin()



