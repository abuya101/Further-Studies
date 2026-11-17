# Ask for the file name
name = input("Enter file:")

# Use mbox-short.txt if nothing is entered
if len(name) < 1:
    name = "mbox-short.txt"

handle = open(name)

# Create a dictionary to store each sender and their message count
counts = dict()

for line in handle:
    # Only process lines starting with "From " (not "From:")
    if line.startswith("From "):
        # Split the line into words
        words = line.split()

        # The second word is the sender's email address
        sender = words[1]

        # Get their current count (or 0), then add 1
        counts[sender] = counts.get(sender, 0) + 1

handle.close()

# Start with no highest count or winning sender
bigcount = None
bigword = None

# Check each sender and their message count
for sender, count in counts.items():
    # Save this sender if this is the first entry
    # or their count is higher than the current highest
    if bigcount is None or count > bigcount:
        bigword = sender
        bigcount = count

# Print the sender with the most messages and their count
print(bigword, bigcount)