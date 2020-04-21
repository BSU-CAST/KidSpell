import KidSpell

print(KidSpell.suggestions('skul', 10))
#['school', 'scale', 'cycle', 'skill', 'skull', 'sickle', 'scull', 'scowl', 'suckle', 'skulk']

print(KidSpell.isInVocab('skul'))
#False

print(KidSpell.getErrors('the skul bus goes relly fast'))
#['skul',relly']

print(KidSpell.getSuggestionsForSentence('the skul bus goes relly fast', 3))
#{'skul': ['school', 'scale', 'cycle'], 'relly': ['really', 'relay', 'rely']}