# KidSpell

Implementation of KidSpell, a child-oriented, rule-based, phonetic spellchecker for correcting English spelling errors.

## Usage

KidSpell.py contains the implementation of KidSpell, an example can be seen in example.py

metaphone_suggestions(word, count) returns a list of suggestions, up to the amount specified by count
```
    metaphone_suggestions('tuchdone', 5) #returns [touchdown, touchdowns, techno, tendon, trodden]
```

pkey(word) creates a phonetic key for a word
```
    mphone('tuchdone') #returns 'T1DN'
```

## Data

The data folder contains several files:

* word_freq.csv, word_freq_clean.csv
    * Dictionary to be used for KidSpell spelling suggestions, necessary for the spellchecker to run. Clean version contains no hate-based or sexually-explicit words

* Essay_Writing_Errors.csv
    * Examples of spelling errors made by children in a hand-written essay-writing context

* Closed_Search_Errors.csv
    * Examples of spelling errors made by children in a closed web-search context

* Open_Search_Errors.csv
    * Examples of spelling errors made by children in an open web-search context
