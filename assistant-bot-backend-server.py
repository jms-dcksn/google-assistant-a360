
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



@app.route('/run_bot', methods=['POST'])
def msg_bot():
    req = request.get_json(silent=True, force=True)
    
    if(req.get("queryResult").get("action") == "AbsenceRequest"):
        name = req.get("queryResult").get("parameters").get("name")
        startDateEntities = req.get("queryResult").get("parameters").get("dates").get("startDate")[:10].split('-')
        startDate = startDateEntities[1] + startDateEntities[2] + startDateEntities[0]
        endDateEntities = req.get("queryResult").get("parameters").get("dates").get("endDate")[:10].split('-')
        endDate = endDateEntities[1] + endDateEntities[2] + endDateEntities[0]
        type = req.get("queryResult").get("parameters").get("type")
        deploymentId = Deploy(startDate, endDate, type)
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

def Deploy(startDate, endDate, type):
    token = CRauth()
    crUrl = "https://aa-saleseng-use-2.my.automationanywhere.digital/v3/automations/deploy"
    data = { "fileId": 91099, "callbackInfo": {}, "runAsUserIds": [366], "poolIds": [42], "overrideDefaultDevice": False, "botInput": { "startDate": { "type": "STRING", "string": startDate }, "endDate": { "type": "STRING", "string": endDate }, "type": { "type": "STRING", "string": type } }}
    data_json = json.dumps(data)
    headers = {"Content-Type": "application/json", "X-Authorization":token}
    response = requests.post(crUrl, data=data_json, headers=headers)
    output = response.json()
    deploymentId = output['deploymentId']
    return deploymentId

def BotStatus():
    token = CRauth()
    crUrl = "https://aa-saleseng-use-2.my.automationanywhere.digital/v2/activity/list"
    data = {"sort":[{"field":"startDateTime","direction":"desc"}],"filter": {"operator": "eq", "field": "fileId", "value": 91099}}
    data_json = json.dumps(data)
    headers = {"Content-Type": "application/json", "X-Authorization":token}
    response = requests.post(crUrl, data=data_json, headers=headers)
    output = response.json()
    status = output['list'][0]['status']
    return status
    

def createResp(Id):
    speech = "Processing your request. Your time-off request is being submitted in Workday. Your request Id is: " + str(Id)[:3] + ". Please check back in a few moments for final confirmation. Say or type: check status of my absence request."

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
        speech = "Your bot is working hard to complete the request in Workday. Please check back in a few moments."
    else:
        speech = "The request has been successfully submitted in Workday for your upcoming absence. Is there anything else I can do for you?"
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

