import urllib.request
import urllib
import json

service_url = "http://py4e-data.dr-chuck.net/opengeo?"

address = input("Enter location: ")

parameters = {"q": address, "key": 42}
url = service_url + urllib.parse.urlencode(parameters)

print("Retrieving", url)
with urllib.request.urlopen(url) as response:
    data = response.read().decode()

print("Retrieved", len(data), "characters")

info = json.loads(data)

plus_code = info["features"][0]["properties"]["plus_code"]

print("Plus code", plus_code)