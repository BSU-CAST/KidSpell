# KidSpell

Implementation of KidSpell, a child-oriented, rule-based, phonetic spellchecker for correcting English spelling errors.

## Usage

KidSpell.py contains the implementation of KidSpell, an example can be seen in example.py

suggestions(word, count) returns a list of suggestions, up to the amount specified by count
```
    suggestions('tuchdone', 5) #returns [touchdown, touchdowns, techno, tendon, trodden]
```

pkey(word) creates a phonetic key for a word
```
    pkey('tuchdone') #returns 'T1DN'
```

## Data

The data folder contains several files:

* word_freq.csv, word_freq_clean.csv
    * Dictionary to be used for KidSpell spelling suggestions, necessary for the spellchecker to run. Clean version contains no hate-based or sexually-explicit words

* Essay_Writing_Errors.csv
    * Examples of spelling errors made by children in a hand-written essay-writing context

* Web_Search_Lab_Errors.csv
    * Examples of spelling errors made by children writing queries for web searches in a lab environment

* Web_Search_Informal_Errors.csv
    * Examples of spelling errors made by children writing queries for web searches in a informal environment
