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
    url2 = content.get('keyurl')
    r2 = requests.get(url2).json()
    f = open("serverkey.json",'w')
    f.write(json.dumps(r2))
    f.close()
    audio_file_path = "https://l.facebook.com/l.php?u=https%3A%2F%2Fcdn.fbsbx.com%2Fv%2Ft59.3654-21%2F30860130_1927196073957801_5646973402498465792_n.mp4%2Faudioclip-1525077887000-1920.mp4%3F_nc_cat%3D0%26oh%3D366fd1be12a27081f78997d1de408c16%26oe%3D5AE94C8B&h=ATMGIj2CUi7VdeLCxg6Pl6TrcKoUpL4tPqeSn0IJfJ8ptqpnsXR_AyJeM90bTJWTQWi3gHzkdfgnjary5EIqiAGuf5PJJvtJn9BpWD1dqNx11a968RWrxQ"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']='serverkey.json'
    project_id=content.get('project_ID')
    session_id=content.get('messenger user id') # for session and context management
    language_code=content.get('language_code')
    texts=[content.get('last user freeform input')]
    #print(project_id, session_id, texts, language_code)
    response = detect_intent_texts(project_id, session_id, texts, language_code)
    response2 = detect_intent_audio(project_id, session_id, audio_file_path,language_code)
    print("audio response", response2)
	
    #service key removed
    os.remove('serverkey.json')
    return response

class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
		
def detect_intent_audio(project_id, session_id, audio_file_path,
                        language_code):
    """Returns the result of detect intent with an audio file as input.

    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    session_client = dialogflow.SessionsClient()

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 16000

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    with open(audio_file_path, 'rb') as audio_file:
        input_audio = audio_file.read()

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)
    query_input = dialogflow.types.QueryInput(audio_config=audio_config)

    response = session_client.detect_intent(
        session=session, query_input=query_input,
        input_audio=input_audio)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))




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