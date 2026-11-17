import urllib.request
from bs4 import BeautifulSoup

# Ask for the data URL
url = input("Enter - ")

# Download and parse the HTML
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")

# Find all span tags instead of anchor (a) tags
tags = soup("span")

count = 0
total = 0

for tag in tags:
    # Extract the text inside each span and convert it to an integer
    number = int(tag.contents[0])

    # Add the number to the total and count this tag
    total = total + number
    count = count + 1

# Match the assignment's output format
print("Count", count)
print("Sum", total)