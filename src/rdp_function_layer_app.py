# |-----------------------------------------------------------------------------
# |            This source code is provided under the Apache 2.0 license      --
# |  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
# |                See the project's LICENSE.md for details.                  --
# |           Copyright Refinitiv 2020. All rights reserved.                  --
# |-----------------------------------------------------------------------------

# |-----------------------------------------------------------------------------
# |   Refinitiv Data Platform APIs direct call vs RDP ease-of-use libraries   --
# |-----------------------------------------------------------------------------

'''
Both RDP APIs and RDP Libraries require the same RDP access credentials which are the username, password and App Key (client id).
'''

import json
from datetime import datetime, timedelta
from dateutil import tz

APP_KEY = ''
RDP_LOGIN = ''
RDP_PASSWORD = ''

# --------------------------- RDP Library -------------------------------------------

import refinitiv.dataplatform as rdp

# -- Init and Authenticate Session
session = rdp.open_platform_session(
    APP_KEY, 
    rdp.GrantPassword(
        username = RDP_LOGIN, 
        password = RDP_PASSWORD
    )
)

# ------------ Historical Pricing Data Request

# Request retrieve time series pricing events of yesterday for 15 rows of data.

response = rdp.get_historical_price_events(
    universe = 'EUR=', 
    start = timedelta(-1),  #example value 2020-07-13T08:54:53.619177000Z
    count = 15,
    adjustments = [
        rdp.Adjustments.EXCHANGE_CORRECTION,
        rdp.Adjustments.MANUAL_CORRECTION
    ]
)



print('This is a Pricing result from RDP library')
print(response)
print('By default, the RDP library Function Layer always returns data in DataFrame format')
print(type(response))


# --------------------------- RDP API Direct Call -------------------------------------

import requests

scope = 'trapi'
client_secret = ''

RDP_version = "/v1"
base_URL = "https://api.refinitiv.com"
category_URL = "/auth/oauth2"
service_endpoint_URL = "/token"

auth_endpoint = base_URL + category_URL + RDP_version + service_endpoint_URL 

auth_obj = None
response = None

# -- Init and Authenticate Session
auth_request_msg = {
    'username': RDP_LOGIN,
	'password': RDP_PASSWORD,
	'grant_type': "password",
	'scope': scope,
	'takeExclusiveSignOnControl': "true"
}

try:
    response = requests.post(auth_endpoint, headers = {'Accept':'application/json'}, data = auth_request_msg, auth = (APP_KEY,client_secret))
except Exception as exp:
	print('Caught exception: %s' % str(exp))

if response.status_code == 200:  # HTTP Status 'OK'
    print('Authentication success')
    auth_obj = response.json()
else:
    print('RDP authentication result failure: %s %s' % (response.status_code, response.reason))
    print('Text: %s' % (response.text))


# ------------ Historical Pricing


category_URL = '/data/historical-pricing'
service_endpoint_URL = '/views/events'

historical_pricing_url = base_URL + category_URL + RDP_version + service_endpoint_URL + '/EUR=' #https://api.refinitiv.com/data/historical-pricing/v1/views/events/EUR=

# Set start date and timestamp to be yesterday in UTC timezoe and in ISO8601 format
start = (datetime.now() + timedelta(-1)).astimezone(tz.gettz('UTC')).replace(tzinfo=None)
start_iso = start.isoformat(timespec='microseconds') + '000Z' #example value 2020-07-13T08:54:53.619177000Z

payload = {'adjustments': 'exchangeCorrection,manualCorrection', 'start': start_iso , 'count':15}

try:
    response = requests.get(historical_pricing_url, headers={'Authorization': 'Bearer {}'.format(auth_obj['access_token'])}, params = payload)
except Exception as exp:
	print('Caught exception: %s' % str(exp))

if response.status_code == 200:  # HTTP Status 'OK'
    print('This is a Historical Pricing data result from RDP API Call')
    print(response.json())
    #print(json.dumps(response.json(),sort_keys=True, indent=2, separators=(',', ':')))
else:
    print('RDP APIs: Pricing data request failure: %s %s' % (response.status_code, response.reason))
    print('Text: %s' % (response.text))



'''
The result shows that RDP library Function layer aims for data scientist/coder who want data in a "ready to use" format. The Dataframe data type lets them analyze data and plotting graph for data visualize. 

In the same time, the direct RDP APIs call return data as a JSON format which is more suitable for data processing or pass it to other system like GUI.
'''