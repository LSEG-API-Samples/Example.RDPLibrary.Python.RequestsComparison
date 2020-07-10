'''
Both RDP APIs and RDP Library require the same RDP access credential, the username, password and App Key (client id).
'''


import json

APP_KEY = ''
RDP_LOGIN = ''
RDP_PASSWORD = ''
universe = ['GBP=','JPY=']
fields   = ['BID','ASK']


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

# ------------ Pricing Data Request

response = rdp.get_snapshot( universe = universe, fields   = fields)

print('This is a Pricing result from RDP library')
print(response)
print('By default, the RDP library Function Layer always returns data in DataFrame format')
print(type(response))
print('Application can use Dataframe.to_json function to convert Dataframe to JSON')
print(response.to_json())


# --------------------------- RDP API Direct Call -------------------------------------

import requests

scope = 'trapi'
client_secret = ''

RDP_version = "/v1"
base_URL = "https://api.refinitiv.com"
category_URL = "/auth/oauth2"
endpoint_URL = "/token"

auth_endpoint = base_URL + category_URL + RDP_version + endpoint_URL

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

# ------------ Pricing Data Request

category_URL = '/data/pricing'
endpoint_URL = '/snapshots'
RDP_version = '/beta3'
pricing_url = base_URL + category_URL + RDP_version + endpoint_URL 

payload = {'universe': ','.join(universe), 'fields': ','.join(fields)}

try:
    response = requests.get(pricing_url, headers={'Authorization': 'Bearer {}'.format(auth_obj['access_token'])}, params = payload)
except Exception as exp:
	print('Caught exception: %s' % str(exp))

if response.status_code == 200:  # HTTP Status 'OK'
    print('This is a Pricing data result from RDP API Call')
    print(response.json())
else:
    print('RDP APIs: Pricing data request failure: %s %s' % (response.status_code, response.reason))
    print('Text: %s' % (response.text))


'''
The result shows that RDP library Function layer aims for data scientist/coder who want data in a "ready to use" format. The Dataframe data type lets them analyze data and plotting graph for data visualize. 

In the same time, the direct RDP APIs call return data as a JSON format which is more suitable for data processing or pass it to other system like GUI.
'''