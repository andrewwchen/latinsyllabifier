"""
sounder function rules: http://logical.ai/arma/
1. identifies potential vowel sounds (1 letter)
2. designates all other letters as consonants (1 letter)
3. pairs together stop + liquid, dipthong, aspirates, and qu (2 letters)
4. ellides and removes letters: vowel + (m +) (h +) vowel
5: TODO prodelides forms of 'esse'

syllabifier rules: http://wheelockslatin.com/chapters/introduction/introduction_syllables.html
1. A single consonant between two vowels goes with the second vowel
2. When two or more consonants stand between two vowels, generally only the last consonant goes with the second vowel

"""
import string

def list_reverser(l):
    if len(l) == 0:
        return []
    else:
        return [l[-1]] + list_reverser(l[:-1])

def liner(passage):
    enter = -1
    lines = []
    passage += '\n'
    for i in range(len(passage)):
        if passage[i] == '\n':
            lines.append(passage[enter + 1:i])
            enter = i
    return(lines)

def worder(line):
    space = -1
    words = []
    if line[0] == '<':
        index = line.index('>')
        searching = True
        while searching:
            index += 1
            if line[index] != ' ':
                searching = False   
                line = line[index + 1:]
    line += ' '
    line = line.lower().translate(str.maketrans('', '', string.punctuation)).translate(str.maketrans('', '', string.digits)).strip() + ' '
    while '  ' in line:
        line = line.replace('  ', ' ')
    for i in range(len(line)):
        if line[i] == ' ':
            words.append(line[space + 1:i])
            space = i
    return(words)

def sounder(line):
    words = worder(line)
    lineChars = []
    for word in words:
        chars = []
        for i in range(len(word)):
            if word[i] in ['a', 'e', 'o', 'y']:
                chars.append(['v', word[i]])
            elif word[i] == 'u' and not word[i-1] == 'q':
                chars.append(['v', word[i]])
            elif word[i] == 'i':
                if i == 0:
                    if word[1] not in ['a', 'e', 'i', 'o', 'u', 'y']:
                        chars.append(['v', word[0]])
                    else:
                        chars.append(['c', word[i]])
                elif i != len(word) - 1:
                    if not (word[i - 1] in ['a', 'e', 'i', 'o', 'y'] or (word[i-1] == 'u' and not word[i-2] == 'q')) or not word[i + 1] in ['a', 'e', 'i', 'o', 'u', 'y']:
                        chars.append(['v', word[i]])
                    else:
                        chars.append(['c', word[i]])
                elif i == len(word) - 1:
                    if not (word[i - 1] in ['a', 'e', 'i', 'o', 'y'] or (word[i-1] == 'u' and not word[i-2] == 'q')):
                        chars.append(['v', word[i]])
                    else:
                        chars.append(['c', word[i]])
            else:
                chars.append(['c', word[i]])
        
        pairs = []
        for i in range(len(chars) - 1):
            if chars[i][0] == 'c' and chars[i + 1][0] == 'c':
                pair = chars[i][1] + chars[i + 1][1]
                if pair in ['qu', 'ch', 'ph', 'th', 'bl', 'cl', 'dl', 'fl', 'gl', 'pl', 'tl', 'br', 'cr', 'dr', 'fr', 'gr', 'pr', 'tr']:
                    pairs.append((i, pair))
            elif chars[i][0] == 'v' and chars[i + 1][0] == 'v':
                pair = chars[i][1] + chars[i + 1][1]
                if pair in ['ae', 'au', 'ei', 'eu', 'oe', 'ui']:
                    pairs.append((i, pair))
        for pair in reversed(pairs):
            chars[pair[0]][1] = pair[1]
            del chars[pair[0] + 1]
        lineChars.append(chars)

    deletedWords = []
    l = list_reverser(list(range(len(lineChars)-1)))
    
    for i in l:
        if lineChars[i][-1][0] == 'v':
            nextWord = ''
            for x in lineChars[i+1]:
                nextWord += x[1]
            if nextWord in ['esse', 'es', 'est', 'estis', 'eram', 'eras', 'erat', 'eramus', 'eratis', 'erant', 'essem', 'esses', 'esset', 'essemus', 'essetis', 'essent', 'ero', 'eris', 'erit', 'erimus', 'eritis', 'erint', 'este', 'ens']:
                lineChars[i] = lineChars[i] + lineChars[i + 1][1:]
                deletedWords.append(i+1)
            elif lineChars[i + 1][0][0] == 'v':
                lineChars[i] = lineChars[i][:-1] + lineChars[i + 1]
                deletedWords.append(i+1)
            elif lineChars[i + 1][1][0] == 'v' and lineChars[i + 1][0][1] == 'h':
                lineChars[i] = lineChars[i][:-1] + lineChars[i + 1][1:]
                deletedWords.append(i+1)
        elif lineChars[i][-2][0] == 'v' and lineChars[i][-1][1] == 'm':
            nextWord = ''
            for x in lineChars[i+1]:
                nextWord += x[1]
            if nextWord in ['esse', 'es', 'est', 'estis', 'eram', 'eras', 'erat', 'eramus', 'eratis', 'erant', 'essem', 'esses', 'esset', 'essemus', 'essetis', 'essent', 'ero', 'eris', 'erit', 'erimus', 'eritis', 'erint', 'este', 'ens']:
                lineChars[i] = lineChars[i] + lineChars[i + 1][1:]
                deletedWords.append(i+1)
            elif lineChars[i + 1][0][0] == 'v':
                lineChars[i] = lineChars[i][:-2] + lineChars[i + 1]
                deletedWords.append(i+1)
            elif lineChars[i + 1][1][0] == 'v' and lineChars[i + 1][0][1] == 'h':
                lineChars[i] = lineChars[i][:-2] + lineChars[i + 1][1:]
                deletedWords.append(i+1)
    for w in deletedWords:
        del lineChars[w]
        
    return(lineChars)

def print_sounder(sounderOutput):
    line = ''
    for word in sounderOutput:
        letters = ''
        for letter in word:
            letters += letter[1]
        line += letters + ' '
    print(line[:-1])
    for word in sounderOutput:
        print(word)

def line_syllabifier(line):
    lineSyllables = []
    for word in sounder(line):
        syllables = []
        vowelCount = 0
        for sound in word:
            if sound[0] == 'v':
                vowelCount += 1
        
        if vowelCount == 1:
            syllables.append(word)

        else:
            first = True
            remainingVowels = vowelCount
            for i in range(len(word)):
                if word[i][0] == 'v':
                    remainingVowels -= 1
                    if first == True:
                        first = False
                        consonantCount = 0
                        nextVowel = False
                        while nextVowel == False:
                            if word[i + consonantCount + 1][0] == 'v':
                                nextVowel = True
                            else:
                                consonantCount += 1
                        if consonantCount == 0:
                            syllables.append(word[:i + 1])
                        elif consonantCount == 1:
                            syllables.append(word[:i + 1])
                        else:
                            syllables.append(word[:i + consonantCount])
                    elif remainingVowels == 0:
                        consonantCount = 0
                        lastVowel = False
                        while lastVowel == False:
                            if word[i - consonantCount - 1][0] == 'v':
                                lastVowel = True
                            else:
                                consonantCount += 1
                        if consonantCount == 0:
                            syllables.append(word[i:])
                        else:
                            syllables.append(word[i-1:])
                    else:
                        consonantCountBefore = 0
                        consonantCountAfter = 0
                        lastVowel = False
                        nextVowel = False
                        while lastVowel == False:
                            if word[i - consonantCountBefore - 1][0] == 'v':
                                lastVowel = True
                            else:
                                consonantCountBefore += 1
                        while nextVowel == False:
                            if word[i + consonantCountAfter + 1][0] == 'v':
                                nextVowel = True
                            else:
                                consonantCountAfter += 1
                        if consonantCountBefore == 0:
                            if consonantCountAfter == 0:
                                syllables.append(word[i:i + 1])
                            elif consonantCountAfter == 1:
                                syllables.append(word[i:i + 1])
                            else:
                                syllables.append(word[i:i + consonantCountAfter])
                        else:
                            if consonantCountAfter == 0:
                                syllables.append(word[i - 1:i + 1])
                            elif consonantCountAfter == 1:
                                syllables.append(word[i - 1:i + 1])
                            else:
                                syllables.append(word[i - 1:i + consonantCountAfter])
        for s in syllables:
            lineSyllables.append(s)
    return(lineSyllables)

def print_line_syllabifier(syllabifierOutput):
    line = []
    for syllable in syllabifierOutput:
        sounds = ''
        for sound in syllable:
            sounds += sound[1]
        line.append(sounds)
    return(line)

def syllabifier(passage):
    syllables = []
    for line in liner(passage):
        syllables.append(print_line_syllabifier(line_syllabifier(line)))
    return syllables

def syllabifier_line_numbers(passage):
    lines = syllabifier(passage)
    output = []
    lineNumber = 1
    for line in lines:
        output.append((lineNumber, line))
        lineNumber += 1
    return output
            
def list_lister(listOlists):
    for list in listOlists:
        print(list)

with open('latin.txt', 'r') as file:
    passage = file.read()
