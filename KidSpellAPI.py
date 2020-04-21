import KidSpell
import flask
from flask import request, jsonify
import logging
import random

application = flask.Flask(__name__)
application.config["DEBUG"] = True
random_order = False
#log = logging.getLogger('werkzeug')
#log.disabled = True

print(KidSpell.suggestions('skul', 10))
#['school', 'scale', 'cycle', 'skill', 'skull', 'sickle', 'scull', 'scowl', 'suckle', 'skulk']

@application.route('/', methods=['GET'])
def home():
    return "<h1>Spellchecking API</p>"

@application.route('/sgst', methods=['GET'])
def api_id():
    # check get variables
    if 'word' in request.args:
        word = request.args['word']
    else:
        return "Error: No word field provided. Please specify a word."
    
    if 'max' in request.args:
        max = int(request.args['max'])
    else:
        max = 5
	
    suggestions = KidSpell.suggestions(word,max)
    if random_order:
        random.shuffle(suggestions)
    # return object
    results = {
        "original": word,
        "suggestions": suggestions
    }

    response = flask.jsonify(results)
    response.headers.add('Access-Control-Allow-Origin', '*')
    # jsonify
    return response

@application.route('/errors', methods=['GET'])
def api_errors():
    if 'sentence' in request.args:
        sentence = request.args['sentence']
    else:
        return "Error: No sentence field provided. Please provide a sentence"

    if 'sugs' in request.args and request.args['sugs'].lower()=='true':
        sugs = True
    else:
        sugs = False

    if 'max' in request.args:
        max = int(request.args['max'])
    else:
        max = 5

    if sugs:
        results = KidSpell.getSuggestionsForSentence(sentence, max)
    else:
        results = {
            "errors": KidSpell.getErrors(sentence)
        }

    response = flask.jsonify(results)
    response.headers.add('Access-Control-Allow-Origin', '*')
    # jsonify
    return response

if __name__ == "__main__":
    application.run(host='0.0.0.0',port='4571')
#app.run(host='0.0.0.0')#,port='4571')
