import urllib.request
import xml.etree.ElementTree as ET

# Ask for the URL containing the XML data.
url = input("Enter location: ")

# Download the XML from the URL.
print("Retrieving", url)
with urllib.request.urlopen(url) as response:
    data = response.read()

print("Retrieved", len(data), "characters")

# Parse the XML into a tree Python can search.
tree = ET.fromstring(data)

# Find every <count> element anywhere in the XML tree.
counts = tree.findall(".//count")

# Convert each count's text to an integer and add it to the total.
total = 0
for count in counts:
    total += int(count.text)

# Display how many counts were found and their sum.
print("Count:", len(counts))
print("Sum:", total)