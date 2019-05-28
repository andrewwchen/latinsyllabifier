# latinsyllabifier
## Features
Syllabifies a Latin passage line-by-line through:
1. Dividing the passage into lines (liner function)
2. Dividing each line into words, removing extra whitespace, numerals, punctuation, and tesserae file metadata (worder function)
3. Dividing each word into component consonant and vowel sounds taking into account pairs of letters e.g. 'qu', 'ae', elision, and prodelision (sounder function)
4. Groups the consonant sounds with vowel sounds based on syllabification rules (line_syllabifier function)
5. Syllabifies whole passages (syllabifier function) as a list lists of syllables of each line
6. Syllabifies passages with line numbers (syllabifier_line_numbers function) as a list of tuples (#, [syllables])