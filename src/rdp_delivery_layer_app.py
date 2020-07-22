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

universe = 'IBM.N'

RDP_version = '/v1'
base_URL = 'https://api.refinitiv.com'

ipa_request_message ={
  "fields": [ "InstrumentTag", "StartDate", "EndDate", "FxSpot", "FxSwapsCcy1Ccy2", "FxOutrightCcy1Ccy2" ],
  "outputs": [ "Data", "Headers" ],
  "universe": [
    {
      "instrumentType": "FxCross",
      "instrumentDefinition": {
        "instrumentTag": "FX_deal_001",
        "fxCrossType": "FxForward",
        "fxCrossCode": "EURGBP",
        "legs": [ { "tenor": "3M10D" } ]
      },
      "pricingParameters": {
        "valuationDate": "2019-02-02T00:00:00Z",
        "priceSide": "Mid"
      }
    }
  ]
}

# --------------------------- RDP Library -------------------------------------------

import refinitiv.dataplatform as rdp

# -- Init and Authenticate Session

try:
    session = rdp.open_platform_session(
        APP_KEY, 
        rdp.GrantPassword(
            username = RDP_LOGIN, 
            password = RDP_PASSWORD
        )
    )
    
except Exception as exp:
	print('RDP Libraries: Initialize Session exception: %s' % str(exp))

print('RDP Library Platfrom Session Status = %s' % session.get_open_state())


# -- Requesting ESG Data

category_URL = '/data/environmental-social-governance'
service_endpoint_URL = '/views/scores-full'

endpoint_url = base_URL + category_URL + RDP_version + service_endpoint_URL #https://api.refinitiv.com/data/environmental-social-governance/v1/views/scores-full
try:
    endpoint = rdp.Endpoint(session, endpoint_url)
    response = endpoint.send_request( query_parameters = {'universe': universe} )
    print('This is a ESG data result from RDP library')
    print(response.data.raw)
except Exception as exp:
	print('RDP Libraries: Delivery Layer exception: %s' % str(exp))

print('\n')

# --- Requesting  Business summary: Returns data for business summary of the specific ric or permId

category_URL = '/user-framework/mobile/overview-service'
service_endpoint_URL = '/corp/business-summary'

endpoint_url = base_URL + category_URL + RDP_version + service_endpoint_URL + '/' + universe #https://api.refinitiv.com/user-framework/mobile/overview-service/v1/corp/business-summary/IBM.N
try:
    endpoint = rdp.Endpoint(session, endpoint_url)
    response = endpoint.send_request()
    print('This is a Business summary data result from RDP library')
    print(response.data.raw)
    print('\n')
except Exception as exp:
	print('RDP Libraries: Delivery Layer exception: %s' % str(exp))

print('\n')

# --- Requesting IPA Data: Financial contracts - FX Forward

category_URL = '/data/quantitative-analytics'
service_endpoint_URL = '/financial-contracts'

endpoint_url = base_URL + category_URL + RDP_version + service_endpoint_URL  #https://api.refinitiv.com/data/quantitative-analytics/v1/financial-contracts

try:
    endpoint = rdp.Endpoint(session, endpoint_url)
    response = endpoint.send_request( method = rdp.Endpoint.RequestMethod.POST, body_parameters  = ipa_request_message)
    print('This is a IPA data result from RDP library')
    print(response.data.raw)
    print('\n')
except Exception as exp:
	print('RDP Libraries: Delivery Layer exception: %s' % str(exp))

# --------------------------- RDP APIs Direct Call -------------------------------------


import requests

# -- Init and Authenticate Session

scope = 'trapi'
client_secret = ''

RDP_version = '/v1'
base_URL = 'https://api.refinitiv.com'
category_URL = '/auth/oauth2'
service_endpoint_URL = '/token'

auth_endpoint = base_URL + category_URL + RDP_version + service_endpoint_URL #https://api.refinitiv.com/auth/oauth2/v1/token

auth_obj = None
response = None

auth_request_msg = {
    'username': RDP_LOGIN,
	'password': RDP_PASSWORD,
	'grant_type': 'password',
	'scope': scope,
	'takeExclusiveSignOnControl': 'true'
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

# -- Requesting ESG Data

print('\n')

category_URL = '/data/environmental-social-governance'
service_endpoint_URL = '/views/scores-full'
esg_url = base_URL + category_URL + RDP_version + service_endpoint_URL  #https://api.refinitiv.com/data/environmental-social-governance/v1/views/scores-full


payload = {'universe': universe}

try:
    response = requests.get(esg_url, headers={'Authorization': 'Bearer {}'.format(auth_obj['access_token'])}, params = payload)
except Exception as exp:
	print('Caught exception: %s' % str(exp))

if response.status_code == 200:  # HTTP Status 'OK'
    print('This is a ESG data result from RDP API Call')
    print(response.json())
else:
    print('RDP APIs: ESG data request failure: %s %s' % (response.status_code, response.reason))
    print('Text: %s' % (response.text))

print('\n')

# --- Requesting  Business summary: Returns data for business summary of the specific ric or permId

RDP_version = '/v1'
category_URL = '/user-framework/mobile/overview-service'
service_endpoint_URL = '/corp/business-summary'
business_summary_url = base_URL + category_URL + RDP_version + service_endpoint_URL + '/' + universe #https://api.refinitiv.com/user-framework/mobile/overview-service/v1/corp/business-summary/IBM.N

try:
    response = requests.get(business_summary_url, headers={'Authorization': 'Bearer {}'.format(auth_obj['access_token'])})
except Exception as exp:
	print('Caught exception: %s' % str(exp))

if response.status_code == 200:  # HTTP Status 'OK'
    print('This is a Business summary data result from RDP API Call')
    print(response.json())
else:
    print('RDP APIs: Business summary data request failure: %s %s' % (response.status_code, response.reason))
    print('Text: %s' % (response.text))

print('\n')

# -- Requesting  IPA: Financial contracts - FX Forward

RDP_version = '/v1'
category_URL = '/data/quantitative-analytics'
service_endpoint_URL = '/financial-contracts'
ipa_url = base_URL + category_URL + RDP_version + service_endpoint_URL  #https://api.refinitiv.com/data/quantitative-analytics/v1/financial-contracts

try:
    response = requests.post(ipa_url, headers = {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(auth_obj['access_token'])}, data = json.dumps(ipa_request_message))
except Exception as exp:
	print('Caught exception: %s' % str(exp))

if response.status_code == 200:  # HTTP Status 'OK'
    print('This is a IPA data result from RDP API Call')
    print(response.json())
else:
    print('RDP APIs: IPA data request failure: %s %s' % (response.status_code, response.reason))
    print('Text: %s' % (response.text))


'''
The RDP Libraries Delivery Layer give developers easy way to make the HTTP request-response operation (and also the other delivery methods such as Stream/WebSockets), Queue  and Files).
'''