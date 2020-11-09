
def getCharFromUnicode(uc):
    return chr(int(uc, base=16))

def cellSelector(startChar, cells, multiple = False, tr = (1,None)):
    target = [cell[tr[0]:tr[1]] for cell in cells if cell.startswith(startChar)]
    if multiple == False:
        assert len(target) < 2, 'trouble startChar: ' + startChar
        if len(target) == 0:
            return ''
        return target[0]
    return '/'.join(target)

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
