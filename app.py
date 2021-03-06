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
import google.protobuf  as pf
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
    return response
        

#to extract values from input json and call detect intent function
def processing(content):   
    url2 = content.get('keyurl')
    r2 = requests.get(url2).json()
    f = open("serverkey.json",'w')
    f.write(json.dumps(r2))
    f.close()
    #setting google credential.
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']='serverkey.json'
    project_id=content.get('project_ID')
    session_id=content.get('messenger user id') # for session and context management
    language_code=content.get('language_code')
    texts=[content.get('last user freeform input')]
    #print(project_id, session_id, texts, language_code)
    response = detect_intent_texts(project_id, session_id, texts, language_code)
    #service key removed
    os.remove('serverkey.json')
    return response


@app.route('/connectDialogflow/', methods=['POST','GET'])
def connectDialogflow():
    content = request.args
    response = processing(content)
	#try adding custom_payload if availalble.
    try: 
        custom_payload = json.loads(pf.json_format.MessageToJson(response.query_result.fulfillment_messages[1].payload, including_default_value_fields=False))
        return jsonify({"messages": [{"text": response.query_result.fulfillment_text},{"attachment":custom_payload["messages"][0]["attachment"]}]})
    except:
        return jsonify({"messages": [{"text": response.query_result.fulfillment_text}]})



if __name__ == '__main__':
	app.debug = True
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port = port)