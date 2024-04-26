import requests


# In this project, Session manage the HTTP request and persist parameters like headers or cookies
# across multiple requests. This can be particularly useful if you're making many requests to 
# the same server, as it allows you to reuse the underlying TCP connection, which can result in a 
# significant performance increase.


# Create a Session
session = requests.Session()

# Set some default headers for all requests in this Session
session.headers.update({'User-Agent': 'MyApp/1.0'})

# Make a request
response = session.get('https://httpbin.org/get')

# The User-Agent header is automatically included
print(response.request.headers['User-Agent'])
