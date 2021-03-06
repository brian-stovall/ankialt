import json

def getCharFromUnicode(uc):
    return chr(int(uc, base=16))

def cellSelector(line, startChar, cells, multiple = False, tr = (1,None)):
    target = [cell[tr[0]:tr[1]] for cell in cells if cell.startswith(startChar)]
    if multiple == False:
        assert len(target) < 2, 'line ' + str(line) + \
            '\ncells ' + str(cells) + \
            '\ntrouble startChar: ' + startChar + '\ntarget: ' + str(target)
        if len(target) == 0:
            return ''
        return target[0]
    return ', '.join(target)

def getMeanings(line, startChar, endChar):
    meaningsStart = line.index(startChar) - 1
    meanings = line[meaningsStart:]
    if endChar is not None:
        meanings = meanings.replace(endChar, '')
    meanings = meanings.split(startChar)[1:]
    return '/'.join([meaning.strip() for meaning in meanings])

def getJMeanings(line):
    return getMeanings(line, '{', '}')

def getCMeanings(line):
    return getMeanings(line, '/', None)

def makeKanjiPin():
    sep = '\t'
    lineNo = 0
    kanjipin = {}
    inheader = True
    with open('/home/artiste/quizlet/dicts/kanjidic', 'r') as infile:
        for line in infile:
            lineNo = lineNo + 1
            if inheader:
                inheader = False
                continue
            cells = line.split(' ')
            kanji = getCharFromUnicode(cellSelector(lineNo, 'U', cells))
            #print(line, kanji)
            pinyin = cellSelector(lineNo, 'Y', cells, multiple = True)
            assert kanji not in kanjipin.keys(), 'duplicate kanji: ' + kanji
            kanjipin[kanji] = pinyin
    print(lineNo, ' kanji processed')
    with open('kanjipin', 'w') as outfile:
        outfile.write(json.dumps(kanjipin, indent=4, ensure_ascii=False))

def makeJoyou():
    sep = '\t'
    maxFreq = 2495
    with open('joyou', 'r') as infile:
        with open('mydict', 'w') as outfile:
            header = ['jFreq', 'hanzi', 'rtk', 'pinyin',
                    'strokeNum', 'jMeanings']
            outfile.write(sep.join(header) + '\n')
            for line in infile:
                jMeanings = getJMeanings(line)
                cells = line.split(' ')
                hanzi = getCharFromUnicode(cellSelector('U', cells))
                rtk = cellSelector('L', cells)
                pinyin = cellSelector('Y', cells, multiple = True)
                strokeNum = cellSelector('S', cells, multiple = True)
                jFreq = cellSelector('F', cells)
                if jFreq == '':
                    maxFreq = maxFreq + 1
                    jFreq = str(maxFreq)
                outfile.write(sep.join([jFreq, hanzi, rtk, pinyin,
                    strokeNum, jMeanings]) + '\n')

def enrichJoyou():
    sep = '\t'
    charDict = {}
    simpleDict = {}
    with open('character-cedict', 'r') as chardict:
        for line in chardict:
            meanings = [meaning for meaning in \
                    getCMeanings(line).split('/') if meaning is not '']
            data = line.split(' ')
            traditionalChar = data[0]
            simpChar = data[1]
            pinyin = ''.join(data[2][1:-1])
            if simpChar not in simpleDict.keys():
                simpleDict[simpChar] = traditionalChar
            if traditionalChar in charDict.keys():
                charDict[traditionalChar]['simple'].add(simpChar)
                charDict[traditionalChar]['pinyin'].add(pinyin)
                charDict[traditionalChar]['meanings'].union(set(meanings))
            else:
                charDict[traditionalChar] = {
                        'simple': set([simpChar]),
                        'pinyin': set([pinyin]),
                        'meanings': set(meanings)
                }
    header = ['jFreq', 'traditional', 'simple',
        'cdict-pinyin', 'strokeNum', 'jMeanings', 'cmeanings']
    entries = {}
    entries[0] = sep.join(header) + '\n'
    with open('mydict', 'r') as mydict:
        header = True
        for line in mydict:
            if header:
                header = False
                continue
            line = line.replace('\n','').split(sep)
            jFreq = line[0]
            traditional = line[1]
            edict_pinyin = line[3]
            strokes = line[4]
            jMeanings = line[5]
            if traditional in charDict.keys():
                dictRow = charDict[traditional]
            elif traditional in simpleDict.keys():
                dictRow = charDict[simpleDict[traditional]]
            else:
                dictRow = {'simple':['n/a'],
                    'pinyin':['n/a'], 'meanings':['n/a']}
            simple = dictRow['simple']
            '''
            assert(len(simple) == 1), 'more than one simp for trad ' + \
                traditional + '\n' + '/'.join(simple)
            '''
            if (len(simple) > 1):
                pass
                '''
                print('more than one simp for trad ',
                    traditional + '\n' + '/'.join(simple))
                '''
            simple = '/'.join(simple)
            cdict_pinyin = '/'.join(dictRow['pinyin'])
            cmeanings = '/'.join(dictRow['meanings'])
            '''
            #about the same
            if edict_pinyin != cdict_pinyin and \
                edict_pinyin.split('/')[0] not in cdict_pinyin.lower() and \
                edict_pinyin.lower() not in cdict_pinyin.lower() and \
                cdict_pinyin.lower() not in edict_pinyin.lower():
                print(edict_pinyin, '!=', cdict_pinyin)
            '''
            entries[int(jFreq)] = sep.join([jFreq, traditional, simple,
                cdict_pinyin, strokes, jMeanings, cmeanings]) + '\n'
            #print(entries[int(jFreq)])
    with open('enriched-joyou', 'w') as outfile:
        entryMax = max(entries.keys())
        #print(entryMax)
        for i in range(0, entryMax + 1):
            if i not in entries.keys():
                #print(i, ' not a key!')
                continue
            #print(entries[i])
            outfile.write(str(entries[i]))

def fixCore6k():
    sep = '\t'
    kanjipin = None
    output = [['word', 'pinyin', 'definition', 'pos', 'sentence', 'translation']]
    lineNo = 0
    with open('kanjipin', 'r') as kanji_in:
        kanjipin = json.loads(kanji_in.read())
    with open('common6k.tsv', 'r') as infile:
        isHeader = True
        headerIndex = None
        for line in infile:
            line = line.split(sep)
            lineNo = lineNo + 1
            if isHeader:
                headerIndex = line
                isHeader = False
                continue
            word = line[headerIndex.index('Vocab-expression')]
            definition = line[headerIndex.index('Vocab-meaning')]
            pos = line[headerIndex.index('Vocab-pos')]
            sentence = line[headerIndex.index('Sentence-expression')]
            sentence = sentence.replace('<', '').replace('>', '') \
                .replace('b', '').replace('/', '')
            translation = line[headerIndex.index('Sentence-meaning')]
            pinyin = []
            for character in word:
                if character in kanjipin.keys():
                    pinyin.append(kanjipin[character])
            pinyin = ', '.join(pinyin)
            output.append([word, pinyin, definition, pos, sentence, translation])
    print(len(output), ' entries churned')
    with open('enriched6k.tsv', 'w') as outfile:
        for line in output:
            outfile.write(sep.join(line) + '\n')

def makeUnihan():
    sep = '\t'
    unidir = '/home/artiste/unihan/'
    unidict = {}
    with open(unidir+'Unihan_Readings.txt', 'r') as readings:
        entryTypes = {
            'kDefinition': 'definition',
            'kJapaneseOn': 'onyomi',
            'kMandarin':'pinyin'
        }
        for line in readings:
            if line.startswith('#') or len(line)==1:
                continue
            line=line.replace('\n','')
            char, entrytype, data = line.split('\t')
            char = getCharFromUnicode(char.replace('U+', ''))
            if char not in unidict.keys():
                unidict[char] = {}
            entry = unidict[char]
            if entrytype in entryTypes.keys():
                if entrytype == 'kMandarin':
                    if ' ' in data:
                        print('two entries!', data, 'choosing ', data.split(' ')[0])
                        data = data.split(' ')[0]
                    data = convertpinyin(data)
                key = entryTypes[entrytype]
                if key not in entry.keys():
                    entry[key] = [data]
                else:
                    entry[key].append(data)
    with open(unidir+'Unihan_Variants.txt', 'r') as variants:
        entryTypes = {
            'kSimplifiedVariant': 'variant-simplified',
            'kTraditionalVariant': 'variant-traditional'
        }
        for line in variants:
            if line.startswith('#') or len(line)==1:
                continue
            line=line.replace('\n','')
            char, entrytype, rawdata = line.split('\t')
            char = getCharFromUnicode(char.replace('U+', ''))
            dataPoints = rawdata.split(' ')
            for data in dataPoints:
                if '<' in data:
                    data = data[0:data.index('<')]
                if 'U+' in data:
                    data = getCharFromUnicode(data.replace('U+', ''))
                if char not in unidict.keys():
                    unidict[char] = {}
                entry = unidict[char]
                if entrytype in entryTypes.keys():
                    key = entryTypes[entrytype]
                    if key not in entry.keys():
                        entry[key] = [data]
                    else:
                        entry[key].append(data)
    unihancleanup(unidict)
    with open('./dicts/unihan.json', 'w') as outfile:
        outfile.write(json.dumps(unidict, indent=4, ensure_ascii=False))

def unihancleanup(unidict):
    pass

def convertpinyin(data):
    lookup = {
        'āēīōūǖ':'1',
        'áéíóúǘ':'2',
        'ǎěǐǒǔǚ':'3',
        'àèìòùǜ':'4'
    }
    char_convert = {
        0:'a',
        1:'e',
        2:'i',
        3:'o',
        4:'u',
        5:'v'
    }
    number = ''
    replacechar = None
    replaceindex = None
    for char in data:
        for key in lookup.keys():
            if char in key:
                number = lookup[key]
                replacechar = char
                replaceindex = key.index(char)
                break
    data = data + number
    if replacechar is not None:
        data = data.replace(replacechar, char_convert[replaceindex])
    return data

def decodeJIS(text):
    return text.decode('iso2022_jp')

def makeEdict():
    edict = {}
    with open('/home/artiste/edict2', 'rb') as infile:
        lineNo = 0
        for line in infile:
            line = str(line.decode('euc_jp'))
            line = line.replace('\n','')
            lineNo = lineNo + 1
            if lineNo == 1:
                continue
            kanastart = line.index(' ')
            kanaend = kanastart
            if '[' in line:
                kanastart = line.index('[')
                kanaend = line.index(']')
            words = line[0:kanastart].strip().split(';')
            kana = line[kanastart+1: kanaend]
            gloss = line[kanaend + 1:]
            meanings = [meaning for meaning in gloss.strip().split('/') \
                if meaning.startswith('EntL') != True and meaning != '']
            for word in words:
                if word not in edict.keys():
                    edict[word] = set()
                entry = edict[word]
                entry = entry.union(set(meanings))
                edict[word] = entry
        for k in edict.keys():
            edict[k] = list(edict[k])
        with open('edict.json', 'w') as outfile:
            outfile.write(json.dumps(edict, indent=4, ensure_ascii=False))

def makeCedict():
    cedict = {}
    with open('./dicts/cedict', 'r') as infile:
        lineNo = 0
        for line in infile:
            if line.startswith('#'):
                continue
            lineNo = lineNo + 1
            tradform, simpform = line.split(' ')[0:2]
            cedict[simpform] = {}
            cedict[simpform]['reading'] = line[line.index('[') + 1 : line.index(']')]
            meanings = line.strip()[line.index('/') : ].split('/')
            cedict[simpform]['definition'] = [meaning for meaning in meanings if meaning != '']
            if simpform != tradform:
                cedict[simpform]['traditional'] = tradformmakeKanjiPin
            #print(lineNo, simpchar, tradchar, reading, meanings)
    with open('./dicts/cedict-json', 'w') as outfile:
        outfile.write(json.dumps(cedict, indent=4, ensure_ascii=False))

def getneededchars():
    '''
    with open('./shinjitai-untypeable', 'r') as infile:
        lineNo = 0
        for line in infile:
            if line.startswith('#') or len(line) < 10:
                continue
            lineNo = lineNo + 1
            line = line.strip()
            if lineNo == 1:
                neededchars.extend(line.split(' '))
                print(lineNo, len(neededchars))
            if lineNo == 2:
                neededchars.extend(thing[2] for thing in line.split(', '))
                print(lineNo, len(neededchars))
            if lineNo == 3 or lineNo == 4:
                [neededchars.extend([thing[0], thing[2]]) for thing in line.split(', ')]
                print(lineNo, len(neededchars))
            if lineNo == 5:
                [neededchars.extend([thing[2], thing[4]]) for thing in line.split(', ')]
                print(lineNo, len(neededchars))
    '''
    neededchars = set()
    cedict = None
    with open('./dicts/cedict-json') as infile:
        cedict = json.loads(infile.read())
    for entry in cedict.keys():
        neededchars.update(list(entry))
    #print(len(neededchars))
    kanjipin = None
    with open('./dicts/kanjipin') as infile:
        kanjipin = json.loads(infile.read())
    for entry in kanjipin.keys():
        neededchars.update(list(entry))
    #print(len(neededchars))
    blacklist = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    blacklist.extend([chr(i) for i in range(ord('A'), ord('Z') + 1)])
    blacklist.extend([str(i) for i in range(0, 10)])
    blacklist = set(blacklist)
    #print(len(blacklist))
    neededchars = neededchars.difference(blacklist)
    #print(len(neededchars))
    unihan = None
    rejects = []
    nopinyin = []
    with open('./dicts/unihan.json') as infile:
        unihan = json.loads(infile.read())
    for char in neededchars:
        if char not in unihan.keys():
            rejects.append(char)
        elif 'pinyin' not in unihan[char].keys():
            if 'onyomi' in unihan[char].keys():
                print('!onyomi', char)
            nopinyin.append(char)
    neededchars = neededchars.difference(rejects)
    neededchars = neededchars.difference(nopinyin)
    #print(len(neededchars))
    charpin = {}
    multi = 0
    for char in neededchars:
        charpin[char] = unihan[char]['pinyin']
        if len(charpin[char]) > 1:
            multi = multi + 1
    #print('multi', multi)
    return charpin

def makeibustable():
    longest = 0
    sep = '\t'
    table = []
    charpin = getneededchars()
    pinchar = {}
    for k, v in charpin.items():
        for pin in v:
            assert ' ' not in pin, print('bad pinyin: ', k, pin)
            table.append(sep.join([pin, k, '1']) + '\n')
            longest = max(longest, len(pin))
            '''
            if len(pin) == longest:
                print('longest so far', pin)
            '''
    print('longest', longest)
    with open('table','w') as outfile:
        for line in table:
            outfile.write(line)





makeibustable()
#getneededchars()
#makeCedict()
#makeEdict()
#makeUnihan()
#makeKanjiPin()
#fixCore6k()
