
# Author - Naresh Ganatra
# http://youtube.com/c/NareshGanatra


from __future__ import print_function
# from future.standard_library import install_aliases
# install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    # commented out by Naresh
    res = processRequest(req)

    res = json.dumps(res, indent=4)

    r = make_response(res)


    r.headers['Content-Type'] = 'application/json'

    return r


def processRequest(req):

    if req.get("queryResult").get("action") != "rate":
        print("Please check your action name in DialogFlow...")
        return {}

    result = req.get("queryResult")
    parameters = result.get("parameters")



    print (parameters['currency-name1'])
    currency1 = parameters['currency-name']
    currency2 = parameters['currency-name1']
    baseurl = 'https://api.exchangeratesapi.io/latest?base=' + currency1 + '&symbols=' + currency2;




    if baseurl is None:
        return {}

    result = urlopen(baseurl).read()
    data = json.loads(result)
    # for some the line above gives an error and hence decoding to utf-8 might help
    # data = json.loads(result.decode('utf-8'))
    res = makeWebhookResult(data,currency2)
    return res



def makeWebhookResult(data,currency2):
    query = data.get('rates')

    if query is None:
        return {}
    result = query.get(currency2)
    if result is None:
        return {}

    speech = "The exchange rate is  " + str(result)


    # Naresh
    return {

        "fulfillmentText": speech,
        "source": "Exchange rateapi"
    }


@app.route('/test', methods=['GET'])
def test():
    return "Hello there my friend !!"


@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Processing your request. Your bot has been deployed successfully! Here is your Id 0e5e7180-9d57-4b50-b383-014ffdcaf77a"
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

