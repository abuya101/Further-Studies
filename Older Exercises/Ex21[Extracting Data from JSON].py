import urllib.request
import json

# Ask for the URL containing the JSON data.
url = input("Enter location: ")

# Download the data and convert it from bytes to text.
print("Retrieving", url)
with urllib.request.urlopen(url) as response:
    data = response.read().decode()

print("Retrieved", len(data), "characters")

# Convert the JSON text into a Python dictionary.
info = json.loads(data)

# Get the list of comments from the dictionary.
comments = info["comments"]

# Add the count from each comment to the total.
total = 0
for comment in comments:
    total += comment["count"]

# Display the number of comments and the total.
print("Count:", len(comments))
print("Sum:", total)