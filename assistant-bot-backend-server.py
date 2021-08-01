
# Author - James Dickson


from __future__ import print_function
# from future.standard_library import install_aliases
# install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import requests
import time
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)



@app.route('/message_bot', methods=['POST'])
def msg_bot():
    req = request.get_json(silent=True, force=True)
    
    if(req.get("queryResult").get("action") == "ShowMessage"):
        inputForBot = req.get("queryResult").get("parameters").get("message")
        deploymentId = Deploy(inputForBot)
        r = createResp(deploymentId)
        return r
    if(req.get("queryResult").get("action") == "GetStatus"):
        status = BotStatus()
        r = createStatusResp(status)
        return r

    


def CRauth():
    authurl = "https://aa-saleseng-use-2.my.automationanywhere.digital/v1/authentication"
    data = {"username": "james.dickson.creator","password": "8$BCAJimmyDenve"}
    data_json = json.dumps(data)
    headers = {'Content-Type':'application/json'}
    response = requests.post(authurl, data=data_json, headers=headers)
    output = response.json()
    #print(output)
    token = output['token']
    return token

def Deploy(botInput):
    token = CRauth()
    crUrl = "https://aa-saleseng-use-2.my.automationanywhere.digital/v3/automations/deploy"
    data = { "fileId": 91001, "callbackInfo": {}, "runAsUserIds": [366], "poolIds": [42], "overrideDefaultDevice": False, "botInput": { "sMsg": { "type": "STRING", "string": botInput } }}
    data_json = json.dumps(data)
    headers = {"Content-Type": "application/json", "X-Authorization":token}
    response = requests.post(crUrl, data=data_json, headers=headers)
    output = response.json()
    deploymentId = output['deploymentId']
    return deploymentId

def BotStatus():
    token = CRauth()
    crUrl = "https://aa-saleseng-use-2.my.automationanywhere.digital/v2/activity/list"
    data = {"sort":[{"field":"startDateTime","direction":"desc"}],"filter": {"operator": "eq", "field": "fileId", "value": 91001}}
    data_json = json.dumps(data)
    headers = {"Content-Type": "application/json", "X-Authorization":token}
    response = requests.post(crUrl, data=data_json, headers=headers)
    output = response.json()
    status = output['list'][0]['status']
    return status

def StartMessageBot():
    deploymentId = Deploy()
    

def createResp(Id):
    speech = "Processing your request. Your bot has been deployed successfully! Your deployment Id is: " + str(Id)

    my_result = {

        "fulfillmentText": speech,
        "source": speech
    }

    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def createStatusResp(status):
    if status == "UPDATE":
        speech = "Your bot is still running"
    else:
        speech = "Your bot has completed successfully and the message was delivered!"
    my_result = {

        "fulfillmentText": speech,
        "source": speech
    }

    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


@app.route('/static_reply', methods=['POST'])
def static_reply():
    req = request.get_json(silent=True, force=True)
    print(req)
    speech = "Processing your request. Your bot has been deployed successfully!"
    string = "You are awesome !!"
    Message = "this is the message"

    my_result = {

        "fulfillmentText": speech,
        "source": speech
    }

    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')

