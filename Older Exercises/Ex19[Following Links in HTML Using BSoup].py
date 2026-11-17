import urllib.request
from bs4 import BeautifulSoup

# Ask for the starting URL, number of links to follow, and position
url = input("Enter URL: ")
count = int(input("Enter count: "))
position = int(input("Enter position: "))

print("Retrieving:", url)

# Follow one link each time through the loop
for step in range(count):
    # Download and parse the current page
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    # Get all anchor tags (links) in their page order
    tags = soup("a")

    # Subtract 1 because Python indexes start at 0
    tag = tags[position - 1]

    # Save the selected name and its link for the next round
    name = tag.get_text()
    url = tag.get("href")

    print("Retrieving:", url)

# Display the name selected on the final round
print("Last name:", name)