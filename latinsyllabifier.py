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


def list_reverser(list_to_reverse):
    if len(list_to_reverse) == 0:
        return []
    else:
        return [list_to_reverse[-1]] + list_reverser(list_to_reverse[:-1])


def liner(passage):
    enter = -1
    lines = []
    passage += '\n'
    for i in range(len(passage)):
        if passage[i] == '\n':
            lines.append(passage[enter + 1:i])
            enter = i
    return lines


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
    line = line.lower().translate(str.maketrans('', '', string.punctuation)).translate(str.maketrans('', '', string.digits)).replace('x', 'cs').replace('z', 'ds').strip() + ' '
    while '  ' in line:
        line = line.replace('  ', ' ')
    for i in range(len(line)):
        if line[i] == ' ':
            words.append(line[space + 1:i])
            space = i
    return words


def sounder(line):
    words = worder(line)
    line_chars = []
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
                else:
                    chars.append(['v', word[i]])
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
# ['ae', 'au', 'ei', 'eu', 'oe', 'ui']
                if pair in ['ae', 'au', 'ei', 'eu', 'oe', 'ui']:
                    pairs.append((i, pair))
        for pair in reversed(pairs):
            chars[pair[0]][1] = pair[1]
            del chars[pair[0] + 1]
        line_chars.append(chars)

    deleted_words = []
    l = list_reverser(list(range(len(line_chars)-1)))
    
    for i in l:
        if line_chars[i][-1][0] == 'v':
            next_word = ''
            for x in line_chars[i+1]:
                next_word += x[1]
            if next_word in ['esse', 'es', 'est', 'estis', 'eram', 'eras', 'erat', 'eramus', 'eratis', 'erant', 'essem', 'esses', 'esset', 'essemus', 'essetis', 'essent', 'ero', 'eris', 'erit', 'erimus', 'eritis', 'erint', 'este', 'ens']:
                line_chars[i] = line_chars[i] + line_chars[i + 1][1:]
                deleted_words.append(i+1)
            elif line_chars[i + 1][0][0] == 'v':
                line_chars[i] = line_chars[i][:-1] + line_chars[i + 1]
                deleted_words.append(i+1)
            elif line_chars[i + 1][1][0] == 'v' and line_chars[i + 1][0][1] == 'h':
                line_chars[i] = line_chars[i][:-1] + line_chars[i + 1][1:]
                deleted_words.append(i+1)
        elif line_chars[i][-2][0] == 'v' and line_chars[i][-1][1] == 'm':
            next_word = ''
            for x in line_chars[i+1]:
                next_word += x[1]
            if next_word in ['esse', 'es', 'est', 'estis', 'eram', 'eras', 'erat', 'eramus', 'eratis', 'erant', 'essem', 'esses', 'esset', 'essemus', 'essetis', 'essent', 'ero', 'eris', 'erit', 'erimus', 'eritis', 'erint', 'este', 'ens']:
                line_chars[i] = line_chars[i] + line_chars[i + 1][1:]
                deleted_words.append(i+1)
            elif line_chars[i + 1][0][0] == 'v':
                line_chars[i] = line_chars[i][:-2] + line_chars[i + 1]
                deleted_words.append(i+1)
            elif line_chars[i + 1][1][0] == 'v' and line_chars[i + 1][0][1] == 'h':
                line_chars[i] = line_chars[i][:-2] + line_chars[i + 1][1:]
                deleted_words.append(i+1)
    for w in deleted_words:
        del line_chars[w]
        
    return line_chars


def print_sounder(sounder_output):
    print('')
    line = ''
    for word in sounder_output:
        letters = ''
        for letter in word:
            letters += letter[1]
        line += letters + ' '
    print(line[:-1])
    for word in sounder_output:
        print(word)


def line_syllabifier(line):
    line_syllables = []
    for word in sounder(line):
        syllables = []
        vowel_count = 0
        for sound in word:
            if sound[0] == 'v':
                vowel_count += 1
        
        if vowel_count == 1:
            syllables.append(word)

        else:
            first = True
            remaining_vowels = vowel_count
            for i in range(len(word)):
                if word[i][0] == 'v':
                    remaining_vowels -= 1
                    if first:
                        first = False
                        consonant_count = 0
                        next_vowel = False
                        while not next_vowel:
                            if word[i + consonant_count + 1][0] == 'v':
                                next_vowel = True
                            else:
                                consonant_count += 1
                        if consonant_count == 0:
                            syllables.append(word[:i + 1])
                        elif consonant_count == 1:
                            syllables.append(word[:i + 1])
                        else:
                            syllables.append(word[:i + consonant_count])
                    elif remaining_vowels == 0:
                        consonant_count = 0
                        last_vowel = False
                        while not last_vowel:
                            if word[i - consonant_count - 1][0] == 'v':
                                last_vowel = True
                            else:
                                consonant_count += 1
                        if consonant_count == 0:
                            syllables.append(word[i:])
                        else:
                            syllables.append(word[i-1:])
                    else:
                        consonant_count_before = 0
                        consonant_count_after = 0
                        last_vowel = False
                        next_vowel = False
                        while not last_vowel:
                            if word[i - consonant_count_before - 1][0] == 'v':
                                last_vowel = True
                            else:
                                consonant_count_before += 1
                        while not next_vowel:
                            if word[i + consonant_count_after + 1][0] == 'v':
                                next_vowel = True
                            else:
                                consonant_count_after += 1
                        if consonant_count_before == 0:
                            if consonant_count_after == 0:
                                syllables.append(word[i:i + 1])
                            elif consonant_count_after == 1:
                                syllables.append(word[i:i + 1])
                            else:
                                syllables.append(word[i:i + consonant_count_after])
                        else:
                            if consonant_count_after == 0:
                                syllables.append(word[i - 1:i + 1])
                            elif consonant_count_after == 1:
                                syllables.append(word[i - 1:i + 1])
                            else:
                                syllables.append(word[i - 1:i + consonant_count_after])
        for s in syllables:
            line_syllables.append(s)
    return line_syllables


def print_line_syllabifier(syllabifier_output):
    line = []
    for syllable in syllabifier_output:
        sounds = ''
        for sound in syllable:
            sounds += sound[1]
        line.append(sounds)
    return line


def syllabifier(passage):
    syllables = []
    for line in liner(passage):
        syllables.append(print_line_syllabifier(line_syllabifier(line)))
    return syllables


def syllabifier_line_numbers(passage):
    lines = syllabifier(passage)
    output = []
    line_number = 1
    for line in lines:
        output.append((line_number, line))
        line_number += 1
    return output


def list_lister(list_o_lists):
    for list_to_print in list_o_lists:
        print(list_to_print)
