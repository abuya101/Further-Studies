smallest = None
print ("Before")
for value in [17,23,4,56,7,89,10]:
    if smallest is None :
        smallest = value
    elif value < smallest :
        smallest = value
    print (smallest, value)
print ("After", smallest)
    