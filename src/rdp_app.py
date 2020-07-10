'''
Both RDP APIs and RDP Library require the same RDP access credential, the username, password and App Key (client id).
'''


import json

APP_KEY = 'b4842f3904fb4a1fa18234796368799086c63541'
RDP_LOGIN = 'wasin.waeosri2@refinitiv.com'
RDP_PASSWORD = 'rvdOZlR!0.IQX!3@I2p='

universe = 'IBM.N'

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

print('RDP Library Platfrom Session Status = %s' % session.get_open_state())

# -- ESG Data

endpoint_url = 'data/environmental-social-governance/v1/views/scores-full'
endpoint = rdp.Endpoint(session, endpoint_url)
response = endpoint.send_request( query_parameters = {'universe': universe} )
print('This is a ESG data result from RDP library')
print(response.data.raw)

print('\n')

# -- Company Fundamentals Data

endpoint_url = 'https://api.refinitiv.com/data/company-fundamentals/beta1/views/operating-metrics-brief/standardized'
endpoint = rdp.Endpoint(session, endpoint_url)
response = endpoint.send_request( query_parameters ={'universe': universe , 'start': 0 ,'end': -4} )
print('This is a Company Fundamentals data result from RDP library')
print(response.data.raw)
print('\n')

# --------------------------- RDP APIs Direct Call -------------------------------------

import requests

# -- Init and Authenticate Session

scope = 'trapi'
client_secret = ''

RDP_version = "/v1"
base_URL = "https://api.refinitiv.com"
category_URL = "/auth/oauth2"
endpoint_URL = "/token"

auth_endpoint = base_URL + category_URL + RDP_version + endpoint_URL

auth_obj = None
response = None

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

# -- ESG Data

print('\n')

category_URL = '/data/environmental-social-governance'
endpoint_URL = '/views/scores-full'
esg_url = base_URL + category_URL + RDP_version + endpoint_URL 

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

# -- Company Fundamentals Data

RDP_version = "/beta1"
category_URL = '/data/company-fundamentals'
endpoint_URL = '/views/operating-metrics-brief/standardized'
company_fundamentals_url = base_URL + category_URL + RDP_version + endpoint_URL 

payload = {'universe': universe , 'start': 0 ,'end': -4}

try:
    response = requests.get(company_fundamentals_url, headers={'Authorization': 'Bearer {}'.format(auth_obj['access_token'])}, params = payload)
except Exception as exp:
	print('Caught exception: %s' % str(exp))

if response.status_code == 200:  # HTTP Status 'OK'
    print('This is a Company Fundamentals data result from RDP API Call')
    print(response.json())
else:
    print('RDP APIs: Company Fundamentals data request failure: %s %s' % (response.status_code, response.reason))
    print('Text: %s' % (response.text))


'''
Returns Standardized Operating Metrics report for last 5 financial years by permId
'''