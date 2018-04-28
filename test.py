import dialogflow
import requests
import json
        
import os
import uuid
#os.environ['GOOGLE_APPLICATION_CREDENTIALS']='servicekey.json'
'''
url = 'https://api.myjson.com/bins/1et04n'
r1 = requests.get(url).json()
print(r1)


url2 = 'https://dl.dropbox.com/s/yio1uc4srkn7jwq/servicekey.json'
r2 = requests.get(url2).json()
print(r2)

f = open("server.json",'w')
f.write(json.dumps(r2))
f.close()

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='server.json'
'''
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
        
# [END dialogflow_detect_intent_text]

'''project_id="testapi-tybiwr"
session_id=str(uuid.uuid4())
language_code="en-US"
texts=['testing']


@app.route('/connectDialogflow', methods=['POST'])
def connectDialogflow():
	content = request.json
	
	return
'''	
def processing():
	url2 = 'https://dl.dropbox.com/s/yio1uc4srkn7jwq/servicekey.json'
	r2 = requests.get(url2).json()
	f = open("serverkey.json",'w')
	f.write(json.dumps(r2))
	f.close()
	os.environ['GOOGLE_APPLICATION_CREDENTIALS']='server.json'
	project_id="testapi-tybiwr"
	session_id=str(uuid.uuid4())
	language_code="en-US"
	texts=['testing']
	detect_intent_texts(project_id, session_id, texts, language_code)
	os.remove('serverkey.json'
	return
processing()