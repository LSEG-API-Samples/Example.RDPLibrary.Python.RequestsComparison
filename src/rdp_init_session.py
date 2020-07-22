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

import warnings
warnings.filterwarnings('ignore')

APP_KEY = ''
RDP_LOGIN = ''
RDP_PASSWORD = ''


# --------------------------- RDP Library -------------------------------------------
import refinitiv.dataplatform as rdp

try:
    # -- Init and Authenticate Session
    session = rdp.open_platform_session(
        APP_KEY, 
        rdp.GrantPassword(
            username = RDP_LOGIN, 
            password = RDP_PASSWORD
        )
    )
    # -- Check Session Status
    print(session.get_open_state())

    # -- Close Session, just calls close_session() function
    rdp.close_session()
    print('Session Status: ', session.get_open_state())
except Exception as exp:
	print('Caught exception: %s' % str(exp))


# --------------------------- RDP API Direct Call -------------------------------------

import requests

scope = 'trapi'
client_secret = ''

RDP_version = "/v1"
base_URL = "https://api.refinitiv.com"
category_URL = "/auth/oauth2"
service_endpoint_URL = "/token"

auth_endpoint = base_URL + category_URL + RDP_version + service_endpoint_URL #https://api.refinitiv.com/auth/oauth2/v1/token

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
    print('RDP APIs: Authentication success')
    auth_obj = response.json()
    print('RDP access_token = %s' % auth_obj['access_token'])
    print('RDP refresh_token = %s' % auth_obj['refresh_token'])
    print('RDP expires_in = %d' % int(auth_obj['expires_in']))
else:
    print('RDP APIs: Authentication result failure: %s %s' % (response.status_code, response.reason))
    print('Text: %s' % (response.text))

# -- Close Session, sending revoke access token request 
close_request_msg = {
    'token': auth_obj['access_token']
}

service_endpoint_URL = "/revoke"

revoke_endpoint = base_URL + category_URL + RDP_version + service_endpoint_URL #https://api.refinitiv.com/auth/oauth2/v1/revoke

try:
    response = requests.post(revoke_endpoint, headers = {'Accept':'application/json'}, data = close_request_msg, auth = (APP_KEY,client_secret))
except Exception as exp:
	print('Caught exception: %s' % str(exp))

if response.status_code == 200:  # HTTP Status 'OK'
    print('RDP APIs: Revoke access token success')
    print(response)
else:
    print('RDP APIs: Revoke access token failure: %s %s' % (response.status_code, response.reason))
    print('Text: %s' % (response.text))

