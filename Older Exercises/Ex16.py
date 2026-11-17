# Import Python's regular expression tools
import re

# Ask for the downloaded file's name
fname = input("Enter file name: ")
fh = open(fname)

# Start the total and number counter at zero
total = 0
count = 0

# Read the file one line at a time
for line in fh:
    # Find every group of one or more digits
    # The results are strings, such as "123"
    numbers = re.findall("[0-9]+", line)

    for number in numbers:
        # Convert each string to an integer and add it
        total = total + int(number)
        count = count + 1

fh.close()

# Display how many numbers were found and their total
print("Count:", count)
print("Sum:", total)