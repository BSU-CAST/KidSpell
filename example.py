import KidSpell

print(KidSpell.suggestions('skul', 10))
#['school', 'scale', 'cycle', 'skill', 'skull', 'sickle', 'scull', 'scowl', 'suckle', 'skulk']

print(KidSpell.isInVocab('skul'))
#False

print(KidSpell.getErrors('the skul bus goes relly fast'))
#['skul',relly']

print(KidSpell.getSuggestionsForSentence('the skul bus goes relly fast'))
#{'skul': ['school', 'scale', 'cycle', 'skill', 'skull'], 'relly': ['really', 'relay', 'rely', 'rally', 'riley']}