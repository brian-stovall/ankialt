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
    with open('kanjidic', 'r') as infile:
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
        outfile.write(json.dumps(kanjipin, indent=4))


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

#makeKanjiPin()
#fixCore6k()
