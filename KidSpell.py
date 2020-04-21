import pandas as pd
import stringdist #pip install StringDist
import numpy as np
import re

#Word Frequency Data
word_freq = pd.read_csv('data/word_freq_clean.csv')
word_freq = word_freq.sort_values(['score'], ascending=[False])
word_freq.set_index('word', inplace=True, drop=False)
ks_vocab = pd.Series(word_freq.score.values,index=word_freq.word).to_dict()

#Phonetic rules
rules = [
    (r'[^a-z]', r''),  #remove non-letters

    #EXCEPTIONS
    (r'(?<=^[rct])ough', r'F'), #rough, cough, tough, make an F sound
    (r'(?<=^en)ough', r'F'), #enough makes the F sound
    (r'^laugh', r'LF'), #laugh makes an F sound
    (r'(?<=[wc(sh)]ou)ld', r'D'), #could not, should not, and would not have an L

    #PRIMARY RULES
    (r'([bdfhjklmnpqrstvwxyz])\1+', r'\1'), #remove some consecutives
    (r'cc', r'K'), #cc -> K
    (r'ck', r'K'), #ck -> K
    (r'^ocea', r'A2'), #^ocea -> OSH
    (r'^[aeiou]+', r'A'), #^vowels -> A
    (r'^[gkp]n', r'N'), #^GN,KN,PN -> N
    (r'^wr', r'R'), #^WR -> R
    (r'^x', r'S'), #^x -> S
    (r'^wh', r'W'), #^wh -> W
    (r'^w', r'W'), #^W -> W
    (r'^gh', r'G'), #^GH -> G
    (r'^rh', r'R'), #^RH-> R
    (r'mb(?=ed|ing|ings|s|\b)', r'M'), #mb at end of word -> M
    (r'^sch', r'SK'), #^sch -> SK
    (r'th', r'0'), #th sound represented as '0'
    (r'^y', r'Y'), #^y -> Y, other Y's will be silent
    (r't?ch',r'1'), #ch or tch to CH - CH sound represented as 1
    (r'sh', r'2'), #sh sound reprented as '2'
    (r'c(?=ion|iou)', r'2'), #cion or ciou -> SH
    (r't(?=ure)', r'1'), # t in ture -> CH 
    (r't(?=ual)', r'1'), # t in tual -> CH
    (r'[st](?=i[ao])', r'2'), #sio, sia, tia, tio -> SH
    (r's?c(?=[iey])', r'S'), #ci, ce, cy, sci, sce, scy -> S
    (r'[c]', r'K'), #other c's -> K
    (r'[d]g(?=[e])', r'J'), #dge -> J
    (r'g(?=h[^aeiou])', r''), #gh then non vowel -> silent like eight or fright
    (r'gh(?=ed|ing|ee|ings|ees|s|\b)', r''), #gh at end of word -> silent
    (r'gh', r'G'), #other gh -> G
    (r'gn(?=ed|ing|ee|ings|ees|s|\b)', r'N'), #gn at end of word -> N
    (r'[y]$', r'Y'), #Y at end of word -> Y
    (r'g+', r'G'), #remove extra g
    (r'ph', r'F'), #PH -> F
    (r'([aeiou])h(?=\b|[^aeiou])', r''), #vowel-h-nonvowel -> silent
    (r'[wy](?=[^aeiou])', r''), #w or y then non vowel -> silent
    (r'[aeiou]w', r''), #vowel then w -> silent
    (r'z', r'S'), # z -> S
    (r'y', r''), # y -> silent
    (r'(?!^)[aeiou]+', r''), #remove vowels
]

#Returns phonetic key for a word
def pkey(word):
    code = word.lower()
    for rule in rules:
        code = re.sub(rule[0], rule[1], code)
    return code.upper()

#Create our dictionary that maps from a key to a list of words
phonetic_dict = {}
for word in word_freq['word']:
    word = str(word).lower()
    try:
        word_phone = pkey(word)
    except:
        continue
    if word_phone in phonetic_dict:
        phonetic_dict[word_phone].append(word)
    else:
        phonetic_dict[word_phone] = [word]

#Generates words of edit distance 1
def edit_distance_1(word):
    word = word.lower()
    letters = list('abc1dfghjklmnpqrs2t0vwxyz')
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(transposes + deletes + replaces + inserts)

#Returns spelling suggestions for the given word
#The amount of spelling suggestions is up to the given count
def suggestions(word, count=5):
    spelling_phone = pkey(word)
    suggestions = []
    #Primary Keys
    if spelling_phone in phonetic_dict:
        suggestions.extend(phonetic_dict[spelling_phone]) 

    #Supplementary Keys
    if len(suggestions) < count:
        additional_suggestions = []
        for eword in edit_distance_1(spelling_phone):
            if eword.upper() in phonetic_dict:
                additional_suggestions.extend(phonetic_dict[eword.upper()])
        additional_suggestions.sort(key=lambda x: stringdist.levenshtein_norm(x, word))
        suggestions.extend(additional_suggestions)

    suggestions = [sug[0].upper() + sug[1:] if word[0].upper() == word[0] else sug for sug in list(dict.fromkeys(suggestions)) if len(sug) > 1]
    return suggestions[:count]

def isInVocab(word):
    return word.upper() in ks_vocab

def getErrors(sentence):
    return [word for word in sentence.split() if word.upper() not in ks_vocab]

def getSuggestionsForSetence(sentence, max=5):
    return {word:suggestions(word) for word in sentence.split() if word.upper() not in ks_vocab}