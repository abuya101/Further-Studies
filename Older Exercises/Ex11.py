fname = input ("Enter file name: ")
fh = open(fname)

count = 0
total = 0.0

for line in fh:
    if line.startswith("X-DSPAM-Confidence:"):
        value = float(line.split(":")[1])
        total = total + value
        count = count + 1

fh.close()

print("Average spam confidence:", total/count)
    