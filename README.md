# Introduction

The [RDP APIs](https://developers.refinitiv.com/refinitiv-data-platform/refinitiv-data-platform-apis) provide various Refinitiv data and content for consumer via easy to use Web base API. The consumer which are data scientist, financial coder or trader can use any programming languages that support HTTP request-response and JSON message to get content from RDP APIs in a straightforward way. An example use case are data scientists use [Python language](https://www.python.org/) with the [requests library](https://requests.readthedocs.io/en/master/) to get data from RDP and visualize it in [Jupyter Notebook](https://jupyter.org/).

The [RDP libraries](https://developers.refinitiv.com/refinitiv-data-platform/refinitiv-data-platform-libraries) are ease-of-use APIs defining a set of uniform interfaces providing the developer access to the Refinitiv Data Platform. It simplify the API interface that even easier than using RDP APIs with Python and requests library directly. 

This article will demonstrate how easy developers can get Refinitiv content via RDP libraries by comparing the application code with RDP libraries ```PlatformSession ``` versus code with Python/requests library to get the same data from Refinitiv Data Platform.

Note: This article is focusing on **How to get data** only. The reason is once the application receives data from either direct call to RDP APIs or RDP libraries, the data processing or visualize logic are the same.

### Disclaimer

As these articles are based on alpha version 1.0.0.a0 of the Python library, the method signatures, data formats etc are subject to change.

## What is RDP libraries



# When should we use the direct call for RDP APIs?

Basically, if developers use the RDP libraries' unsupported language, they can still get data from RDP with a basic HTTP request-response way. 

The other case is developers need to manual control the HTTP status, connection detail and credentials information based on the application requirement such as a server application, web application or GUI. 

# Other benefits of using RDP libraries

With RDP libraries, developers are not limited only Refinitiv Data Platform , but developers also can access to Refinitiv Desktop (Eikon or Refinitiv Workspace) and Deployed/Managed TREP infrastructure platforms with a the same set of API. Using the library you can access content from all 3 of the access points - all from within the same application if required. One example would be sourcing realtime streaming Pricing data from your TREP server as well as say historical pricing events from the cloud-based Refinitiv Data platform.