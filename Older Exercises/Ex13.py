# Ask the user for a file name
fname = input("Enter file name: ")

# Use mbox-short.txt if nothing is entered
if len(fname) < 1:
    fname = "mbox-short.txt"

# Open the file for reading
fh = open(fname)

# Start the message counter at zero
count = 0

# Read the file one line at a time
for line in fh:
    # Match "From " lines, excluding lines starting with "From:"
    if line.startswith("From "):
        # Split the line into a list of words
        words = line.split()

        # Print the second word: the sender's email address
        # Python counts positions from 0, so [1] means second
        print(words[1])

        # Add one to the message counter
        count = count + 1

# Close the file after reading
fh.close()

# Print the total number of matching lines
print("There were", count, "lines in the file with From as the first word")