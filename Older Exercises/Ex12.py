# Ask the user for a file name, such as romeo.txt
fname = input("Enter file name:")

# Open the file for reading
fh = open(fname)

# Create an empty list to store unique words
lst = list()

# Read the file one line at a time
for line in fh:
    # Split each line into a list of words
    words = line.split()

    # Check each word in that line
    for word in words:
        # Only add the word if it is not already in our list
        if word not in lst:
            lst.append(word)

# Close the file after reading
fh.close()

# Sort the words; uppercase letters come before lowercase letters
lst.sort()

# Print the sorted list of unique words
print(lst)