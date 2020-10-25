# Syllabifier for Latin Poetry by Andrew W. Chen
This repository contains a set of functions used for dividing Latin poetry into component syllables for quantitative analysis. Testing of each function and error analysis can be found in the jupyter notebook **latinsyllabifier.ipynb**. The Latin source text can be found at https://tesserae.caset.buffalo.edu/sources.php from the Tesserae Project.


>*Part of a paper on quantifying the phonetic difference between Virgil's Aeneid and it's translations for QSS 30.12.*

>A digital version of this paper can be found here:
https://docs.google.com/document/d/1KECKDe_43vN8M1XoZKLlk_22Qq_ChuoQZIVAKWEiWt0/edit?usp=sharing

## Features
Syllabifies a Latin passage line-by-line through:
1. Dividing the passage into lines (liner function)
2. Dividing each line into words, removing extra whitespace, numerals, punctuation, and tesserae file metadata (worder function)
3. Dividing each word into component consonant and vowel sounds taking into account pairs of letters e.g. 'qu', 'ae', elision, and prodelision (sounder function)
4. Groups the consonant sounds with vowel sounds based on syllabification rules (line_syllabifier function)
5. Syllabifies whole passages (syllabifier function) as a list lists of syllables of each line
6. Syllabifies passages with line numbers (syllabifier_line_numbers function) as a list of tuples (#, [syllables])
