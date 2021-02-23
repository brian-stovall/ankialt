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

def getKanjiJson():
    kanjiJson = None
    with open('./dicts/kanji-json') as infile:
        kanjiJson=json.loads(infile.read())
    return kanjiJson

def begin():
    global start
    start = time.time()
    begin = None
    end = None
    jsondata = None
    kj = getKanjiJson()
    begin = int(input('Start with which entry?')) - 1
    end = int(input('End with which entry?'))
    jsondata = load()[begin : end]
    random.shuffle(jsondata)
    test(kj, jsondata, start)

def end():
    global globalErrors
    with open('lastErrors', 'w') as myerrors:
        myerrors.write(json.dumps(list(globalErrors), ensure_ascii=False))

def lookup(kj, symbol):
    data = kj[symbol]
    for key, value in data.items():
        print(key, value)

def test(kj, jsondata, start, frame = 1):
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
        lookup(kj, symbol)
        input()

    elapsed = time.time() - start
    minutes = elapsed / 60.0
    print('good job! ', minutes, ' min ')
    again = input('go again?')
    if again == 'y':
        begin()
    else:
        end()

begin()



