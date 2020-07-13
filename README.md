# Introduction

The [Refinitiv Data Platform (RDP) APIs](https://developers.refinitiv.com/refinitiv-data-platform/refinitiv-data-platform-apis) provide various Refinitiv data and content for developers via easy to use Web base API. The consumers which are data scientist, financial coder or trader can use any programming languages that support HTTP request-response and JSON message to retrieve content from RDP in a straightforward way. An example use case are data scientists use [Python language](https://www.python.org/) with the [requests library](https://requests.readthedocs.io/en/master/) to get data from RDP and visualize that data in [Jupyter Notebook](https://jupyter.org/) application.

The [Refinitiv Data Platform Libraries](https://developers.refinitiv.com/refinitiv-data-platform/refinitiv-data-platform-libraries) are ease-of-use APIs defining a set of uniform interfaces providing the developer access to the Refinitiv Data Platform. It simplify the API interface that even easier than using RDP APIs with Python and requests library directly. 

This article will demonstrate how easy developers can get Refinitiv content via RDP Libraries by comparing the application code with RDP Libraries ```PlatformSession ``` versus code with Python/requests library to get the same data from the platform.

Note: This article is focusing on **How to get data** only because once the application receives data from either direct RDP APIs call or RDP Libraries, the data processing or visualize logic are the same.

### Disclaimer

As these articles are based on alpha version 1.0.0.a0 of the Python library, the method signatures, data formats etc are subject to change.

## What is RDP libraries

## Initialize and Authentication

Refinitiv Data Platform entitlement check is based on OAuth 2.0 specification. The first step of an application work flow is to get a token, which will allow access to the protected resource, i.e. data REST API's. The API requires the following access credential information:
- Username: The username. 
- Password: Password associated with the username. .
- Client ID: This is also known as “AppKey”, and it is generated using an Appkey Generator. This unique identifier is defined for the user or application and is deemed confidential (not shared between users). The client_id parameter can be passed in the request body or as an “Authorization” request header that is encoded as base64.

Both RDP APIs and RDP Libraries PlatformSession applications require the above access credentials to initiate and authentication with the platform.

### Direct call RDP APIs

The application needs to send a HTTP Post message with the access credentials to RDP Auth Service endpoint ```https://api.refinitiv.com:443/auth/oauth2/v1/token``` (as of July 2020, the current version of RDP Auth Service is **v1**). 

A successful authentication response message from RDP Auth Service contains the following parameters:
- **access_token**: The token used to invoke REST data API calls as described above. Application must keeps this credential for further RDP/ERT in Cloud request.
- **refresh_token**: Refresh token to be used for obtaining an updated access token before expiration. Application must keeps this credential for access token renewal.
- **expires_in**: Access token validity time in seconds.
- **scope**: A list of all the scopes this token can be used with.

For the full detail and explanation of RDP Authentication process application workflow, please refer to the following RDP APIS tutorials:
* [Introduction to the Request-Response API](https://developers.refinitiv.com/requestresponse-apis/learning?content=38560&type=learning_material_item).
* [Authorization - All about tokens](https://developers.refinitiv.com/refinitiv-data-platform/refinitiv-data-platform-apis/learning?content=38562&type=learning_material_item).
* [Authorization in Python](https://developers.refinitiv.com/refinitiv-data-platform/refinitiv-data-platform-apis/learning?content=39322&type=learning_material_item).

Example Code:
```
import json
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
    print('RDP APIs: Authentication success')
    auth_obj = response.json()
    print('RDP access_token = %s' % auth_obj['access_token'])
    print('RDP refresh_token = %s' % auth_obj['refresh_token'])
    print('RDP expires_in = %d' % int(auth_obj['expires_in']))
else:
    print('RDP APIs: Authentication result failure: %s %s' % (response.status_code, response.reason))
    print('Text: %s' % (response.text))
```

The above code is very straightforward, the application creates a request message in JSON message format, send HTTP Post request message and get authentication result if HTTP status response is 200 (Ok).

However, the RDP Libraries gives developers the easiest way to authenticates with RDP Auth Service.

### RDP Libraries

With RDP Libraries, the first thing the application needs to do is create a **Session** with the following logical connection points based on how the application intend to access the platform. The list of supported connection points are following:
- DesktopSession (Eikon/Refinitiv Workspace)
- PlatformSession (RDP, ERT in Cloud)
- DeployedPlatformSession (deployed Elektron enterprise platform -TREP/ADS)

The session is an interface to a specific access channel and is responsible for defining authentication details, managing connection resources, and implementing the necessary protocol to manage the life cycle of the session.

Lets focus on the PlatformSession session which requires the same RDP access credentials as a direct call to RDP APIs.

Example Code:
```
import refinitiv.dataplatform as rdp

# -- Init and Authenticate Session
session = rdp.open_platform_session(
    APP_KEY, 
    rdp.GrantPassword(
        username = RDP_LOGIN, 
        password = RDP_PASSWORD
    )
)

print(session.get_open_state())
```

Thats it, the application just pass the same RDP access credentials to the Libraries ```open_platform_session()``` function to initialize and authenticate with RDP Auth Service. Once the session is established , application can check the session status with the ```get_default_session().get_open_state()``` function.

The RDP Libraries makes application source code simple and easy to read.

## Requesting RDP Data

Once the application success authenticates with RDP platform, the application can request data/content from the platform. 

### Direct call RDP APIs

When the application receives the Access Token (an authorization token) from RDP Auth Service, all subsequent REST API calls will use this token to get the data. The application needs to input Access Token via *Authorization* HTTP request message header as shown below. 
- Header: 
    * Authorization = ```Bearer <RDP Access Token>```

Please notice *the space* between the ```Bearer``` and ```RDP Access Token``` values.

The application then creates a request message in a JSON message format or URL query parameter based on interested service and send it to the Service Endpoint. Developers can get RDP APIs information regarding the Service Endpoint, HTTP operations and parameters from Refinitiv Data Platform's [API Playground page](https://api.refinitiv.com/) - which an interactive documentation site developers can access once they have a valid Refinitiv Data Platform account.

Example Code for **/data/pricing** service:
```
# Authentication success with RDP Auth Service Access Token in auth_obj['access_token']

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
    print(response.json())
else:
    print('RDP APIs: Pricing data request failure: %s %s' % (response.status_code, response.reason))
    print('Text: %s' % (response.text))
```

Example Code for **/data/company-fundamentals** service:
```
# Authentication success with RDP Auth Service Access Token in auth_obj['access_token']

# -- Company Fundamentals Data

RDP_version = "/beta1"
category_URL = '/data/company-fundamentals'
endpoint_URL = '/views/operating-metrics-brief/standardized'
company_fundamentals_url = base_URL + category_URL + RDP_version + endpoint_URL #https://api.refinitiv.com/data/company-fundamentals/beta1/views/operating-metrics-brief/standardized

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
```

The above code from two services show that the main application logic is the same even the application change interested service. The application just needs to change the Service Endpoint URL and request message.

### RDP Libraries - Function Layer

With RDP Libraries, the application does not need to handle the Access Token information. The application just calls the Libraries Function or Content or Delivery Layer interfaces to get data, the Libraries will handle the Session and authentication information for the application.

The RDP Libraries *Function Layer* provides the easiest to the most commonly used data content such as News Headlines and Stories, retrieving historical intraday/interday data etc. The Function layer interfaces are single function call aims for scripting languages like Python which allows researchers, data scientists or the casual developer to rapidly prototype solutions within interactive environments such as [Jupyter Notebooks](https://jupyter.org/).


Example Code for **Pricing** service:
```
# rdp.open_platform_session initialize call success

response = rdp.get_snapshot( universe = universe, fields   = fields)
print(response) # DataFrame

print(response.to_json()) # JSON
```

The Function Layer returns data as Pandas's [DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) object by default which is the main data type on Jupyter Notebook. The application can convert that DataFrame to JSON object via DataFrame's ```to_json()``` function.

If developers want the same content as above with a full detail response or with Asynchronous/Event-Driven operating mode, the RDP Libraries also provides the *Content Layer* for developers. Please see more detail regarding the Content Layer in [Discover our Refinitiv Data Platform Library (part 1) tutorial](https://developers.refinitiv.com/article/discover-our-upcoming-refinitiv-data-platform-library-part-1).

### RDP Libraries - Delivery Layer

Refinitiv is developing the library and hope to offer Function and Content Layers support for other data content such as Environmental, Social and Governance (ESG) data, Fundamentals and so on. In the meantime, the Libraries also let developers access to a wide range of content that not available in Function and Content Layers yet with a *Delivery Layer*.

Please note that developers are still need to get the Service Endpoint and Request parameters information from the [API Playground page](https://api.refinitiv.com/). 

Example Code for **/data/company-fundamentals** service
```
# rdp.open_platform_session initialize call success

endpoint_url = 'https://api.refinitiv.com/data/company-fundamentals/beta1/views/operating-metrics-brief/standardized'
endpoint = rdp.Endpoint(session, endpoint_url)
response = endpoint.send_request( query_parameters ={'universe': universe , 'start': 0 ,'end': -4} )
print('This is a Company Fundamentals data result from RDP library')
print(response.data.raw)
```

The above code show that the Delivery Layer simplify how the application can sends the request message to the interested RDP Service.

## Un-initialize and Revoke Authentication

### Direct call RDP APIs

The application need to send the revoke request message to RDP Auth Service to revoke authorization of the Access Token.

Example Code:
```
# -- Close Session, sending revoke access token request 
close_request_msg = {
    'token': auth_obj['access_token']
}

endpoint_URL = "/revoke"

revoke_endpoint = base_URL + category_URL + RDP_version + endpoint_URL

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
```

### RDP Libraries

The application just calls RDP Libraries ```close_session()``` function to revoke/close the current Session.

Example Code:
```
# -- Close Session, just calls close_session() function
rdp.close_session()
print(session.get_open_state())
```

# When should developers use the direct call for RDP APIs?

Basically, if developers use the RDP libraries' unsupported language, they can still get all content from Refinitiv Data Platform with a basic HTTP request-response operations. 

The other case is the application requires a manual control over the HTTP status handlers, connection detail and credentials information such as a server application, web application or GUI. The direct call with any programming languages that supports JSON and HTTP request-response is also suitable.

# Other benefits of using RDP Libraries

With RDP libraries, developers are not limited only Refinitiv Data Platform , but developers also can access to Refinitiv Desktop (Eikon or Refinitiv Workspace) and Deployed/Managed TREP infrastructure platforms with a the same set of API. Using the library you can access content from all 3 of the access points - all from within the same application if required. One example would be sourcing realtime streaming Pricing data from your TREP server as well as say historical pricing events from the cloud-based Refinitiv Data platform.

## <a id="references"></a>References
For further details, please check out the following resources:
* [Refinitiv Data Platform Libraries page](https://developers.refinitiv.com/refinitiv-data-platform/refinitiv-data-platform-libraries) on the [Refinitiv Developer Community](https://developers.refinitiv.com/) web site.
* [Refinitiv Data Platform APIs page](https://developers.refinitiv.com/refinitiv-data-platform).
* [Refinitiv Data Platform APIs Gateway page](https://api.refinitiv.com).
* [Developer Article: Discover our Refinitiv Data Platform Library part 1](https://developers.refinitiv.com/article/discover-our-upcoming-refinitiv-data-platform-library-part-1).
* [Developer Article: Discover our Refinitiv Data Platform Library part 2](https://developers.refinitiv.com/article/discover-our-upcoming-refinitiv-data-platform-library-part-2-0).
* [Refinitiv Data Platform Libraries: An Introduction page](https://developers.refinitiv.com/refinitiv-data-platform/refinitiv-data-platform-libraries/docs?content=62446&type=documentation_item).
* [Refinitiv Data Platform Libraries: Delivery Layer Tutorial page](https://developers.refinitiv.com/refinitiv-data-platform/refinitiv-data-platform-libraries/learning?content=52250&type=learning_material_item).

For any question related to Refinitiv Data Platform or Refinitiv Data Platform Libraries, please use the Developers Community [Q&A Forum](https://community.developers.refinitiv.com/spaces/231/index.html).