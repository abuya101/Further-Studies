nh = input ("How many hours: ")
nr = input ("Whats your hourly rate: ")
try:
    fh = float (nh)
    fr = float (nr)
except:
    print("Enter a valid numeric input")
    quit()
if fh > 40 :
    regp = fh * fh
    otp = (fh - 40.0) * (fr * 0.5)
    xp = regp + otp
else:
    xp = fh * fr
print ("Your pay is", xp,"dollars!")


