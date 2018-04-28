# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 16:11:41 2017

@author: vikas
"""
from flask import Flask, request, jsonify
import os
import dialogflow
import requests
import json
import uuid

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

# intent detect function for text.
def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))
    return response
        

#to extract values from input json and call detect intent function
def processing(content):
    print(content)
    #content['url'] 
    url2 = 'https://dl.dropbox.com/s/yio1uc4srkn7jwq/servicekey.json'
    r2 = requests.get(url2).json()
    f = open("serverkey.json",'w')
    f.write(json.dumps(r2))
    f.close()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']='serverkey.json'
    project_id="testapi-tybiwr"
    session_id=str(uuid.uuid4())
    language_code="en-US"
    texts=['testing']
    response = detect_intent_texts(project_id, session_id, texts, language_code)
    os.remove('serverkey.json')
    return response



@app.route('/connectDialogflow/', methods=['POST'])
def connectDialogflow():
    print(request)
    content = request.args
    response = processing(content)
    print(response)
    return jsonify({"response":"Success"})




if __name__ == '__main__':
	app.debug = True
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port = port)