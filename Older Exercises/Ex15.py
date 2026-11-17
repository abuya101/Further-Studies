# Ask for a file name
name = input("Enter file:")

# Use mbox-short.txt if nothing is entered
if len(name) < 1:
    name = "mbox-short.txt"

handle = open(name)

# Store each hour and its message count in a dictionary
counts = dict()

# Read the file one line at a time
for line in handle:
    # Only process "From " lines, excluding "From:"
    if line.startswith("From "):
        words = line.split()

        # The sixth word is the time, such as "09:14:16"
        time = words[5]

        # Split the time at each colon and take the hour
        hour = time.split(":")[0]

        # Add 1 to this hour's count; start at 0 if it is new
        counts[hour] = counts.get(hour, 0) + 1

handle.close()

# Sort the (hour, count) pairs by hour and print each pair
for hour, count in sorted(counts.items()):
    print(hour, count)