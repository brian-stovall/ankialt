import json

kanarange = range(int(0x3040), int(0x30FF) + 1)
unihan = None
commonWords = None
edictJson = None

def makeEdict():
    data = {}
    with open('./dicts/edict', 'r', encoding='euc-jp') as infile:
        for line in infile:
            meaningStart = line.find('/') + 1
            meaning = line[meaningStart : line.find('/', meaningStart)]
            readingStart = line.find('[') + 1
            reading = line[readingStart : line.find(']', readingStart)]
            reading = reading.split(';')[0]
            word = line.split()[0].split(';')[0]
            data[word] = {
                'meaning': meaning,
                'reading' : reading,
                }
    with open('./dicts/edict-json', 'w') as outfile:
        outfile.write(json.dumps(data, indent=4, ensure_ascii=False))



def getCommonWord(kanji):
    global commonWords
    if commonWords == None:
        with open('./commonWords.json') as infile:
            commonWords=json.loads(infile.read())
    global edictJson
    if edictJson == None:
        with open('./dicts/edict-json') as infile:
            edictJson=json.loads(infile.read())
    for entry in commonWords:
        if kanji in entry['word']:
            word = entry['word']
            if word in edictJson:
                return (word, edictJson[word]['reading'],
                    edictJson[word]['meaning'])
    return (None, None, None)

def isReading(word):
    for char in word:
        if ord(char) not in kanarange and char != '.' and char != '-':
            return False
    return True

def lookupPinyin(symbol):
    global unihan
    if unihan == None:
        with open('./dicts/unihan.json') as infile:
            unihan=json.loads(infile.read())
    unidata = unihan[symbol]
    if 'pinyin' not in unidata.keys():
        return None
    pinyin = unidata['pinyin']
    assert len(pinyin) == 1, 'too long pinyin!! ' + symbol
    return pinyin[0]

def getCharFromUnicode(uc):
    return chr(int(uc, base=16))

def getMeanings(line):
    meanings = []
    for idx, character in enumerate(line):
        if character == '{':
            meanings.append(line[idx + 1 : line.find('}', idx)])
    #print(meanings)
    return meanings

def getReadings(line):
    readings = []
    line = line[0:line.find('{')]
    line = line.split()
    if 'T1' in line:
        line = line[0:line.index('T1')]
    line.reverse()
    for element in line:
        if isReading(element):
            readings.append(element)
    readings.reverse()
    return readings


def makeKanjiDict():
    sep = '\t'
    data = {}
    inheader = True
    lineNo = -1
    with open('./dicts/kanjidic', 'r', encoding='euc-jp') as infile:
        for line in infile:
            lineNo = lineNo + 1
            if lineNo == 0:
                continue #get rid of header
            #if lineNo > 10: #debug
            #    return
            cells = line.split()
            character = getCharFromUnicode(cells[2][1:])
            meanings = getMeanings(line)
            readings = getReadings(line)
            pinyin = lookupPinyin(character)
            commonWord, commonReading, commonMeaning = getCommonWord(character)
            data[character] = {
                'meanings' : meanings,
                'readings' : readings,
                'pinyin' : pinyin,
                'commonWord' : commonWord,
                'commonMeaning' : commonMeaning,
                'commonReading' : commonReading
            }
    print(len(data))
    with open('./dicts/kanji-json', 'w') as outfile:
        outfile.write(json.dumps(data, indent=4, ensure_ascii=False))

#makeEdict()
makeKanjiDict()
