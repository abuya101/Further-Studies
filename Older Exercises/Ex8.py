str = "X_DSPAM_Confidence: 0.8475"
colon = str.find(":")

print(colon)
section = str[colon+1:]

print(section)

value = float(section)
print(value)