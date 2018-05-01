# Dialogflow v2 connect JSON API
Currently handles fulfilment texts with context management and text-based intent detection and custom payloads. Future steps:
1. Enable voice based intent detection

|Varible|Description|
|--|--|
|{{keyurl}}|	URL for your google credential service key, hosted on dropbox or similar service). Note: this will be used and removed and will not be saved anywhere post request) If you are wondering how to generate it, I will be explaining that below|
|{{project_ID}}|go to your bot settings and select copy the project ID|
|{{language_code}}|	In case your bot and dialogflow handles many languages, you might want to take it from user programmatically using quick replies maybe, else enter the one that your bot handles in my case “en-US”|
|{{last user freeform input}}|	Inbuilt in chatfuel, this is variable contains the last text that user entered which bot was unable to understand|
|{{messenger user id}}|	Inbuilt (we will be using this value for session and context management)|

For more detailed steps: click [here](https://github.com/JainVikas/dialogflow-json-api/blob/master/Dialogflow%20v2%20json%20API.docx)

If you plan to use, or reuse this code in any format
please cite the link of repository. https://github.com/JainVikas/dialogflow-json-api
