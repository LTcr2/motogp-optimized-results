"""Example of using an API."""

import requests
from pprint import pprint

import http.client

conn = http.client.HTTPSConnection("api.sportradar.us")

your_api_key = 't2pxakdxpkskhr3ajc3rgb72'

conn.request("GET", "/motogp/trial/v2/en/competitors/sr:competitor:49401/profile.xml?api_key={your_api_key}")

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


# the above code returns "<hi>Developer Inactive</h1>" when use.py run in interactive mode in console


# def print_emp(label, api, competitor_id):
# 	"""Print detail about a competitor."""

# 	print()
# 	print(label)
# 	print()

# 	comp = requests.get()