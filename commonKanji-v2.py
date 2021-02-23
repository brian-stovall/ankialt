import json, sys, os, time, random
start = None
errorcount = 0
globalErrors = set()

def load():
    data = None
    datafile = './better-common-kanji.json'
    with open(datafile, 'r') as kanjidata:
        data = kanjidata.read()
    return list(json.loads(data).keys())

def getUnihan():
    unihan = None
    with open('./dicts/unihan.json') as infile:
        unihan=json.loads(infile.read())
    return unihan

def getPreviousErrors():
    pe = None
    with open('./lastErrors') as infile:
        pe=json.loads(infile.read())
    return pe

def removeNum(string):
    lst = list(string)
    return ''.join([char for char in lst if str.isnumeric(char) == False])

def begin():
    global start
    start = time.time()
    begin = None
    end = None
    jsondata = None
    unihan = getUnihan()
    #choice = input('Study previous errors?')
    choice = 'n'
    if choice == 'y':
        jsondata = getPreviousErrors()
    else:
        begin = int(input('Start with which entry?')) - 1
        end = int(input('End with which entry?'))
        jsondata = load()[begin : end]
    random.shuffle(jsondata)
    test(unihan, jsondata, start)

def end():
    global globalErrors
    with open('lastErrors', 'w') as myerrors:
        myerrors.write(json.dumps(list(globalErrors), ensure_ascii=False))

def lookup(unihan, symbol):
    unidata = unihan[symbol]
    pinyin = unidata['pinyin']
    definition =
    print(symbol, ''.join(unidata['pinyin']), ''.join(unidata['definition']))
    return removeNum(unidata['pinyin'])

def test(unihan, jsondata, start, frame = 1):
    global errorcount
    errors = []
    task = 0
    for symbol in jsondata:
        task += 1
        answer = ''
        while symbol not in answer:
            os.system('clear')
            print(symbol)
            print()
            answer = input()
            if 'q' in answer:
                end()
                sys.exit()
        lookup(unihan, symbol)
        input()

    print('frame', frame, ' errors:', len(errors), ' total:', len(jsondata))
    if len(errors) > 0:
        input('enter to continue to next frame')
        test(unihan, errors, start, frame +1)
    else:
        elapsed = time.time() - start
        minutes = elapsed / 60.0
        print('good job! ', minutes, ' min ', errorcount, ' errors')
        again = input('go again?')
        if again == 'y':
            begin()
        else:
            end()

begin()



