missed_calls = {"Monday": 0, "Tuesday": 3, "Wednesday": 7}

missed_calls["Thursday"] = 2
missed_calls["Friday"] = 5

total = 0

for count in missed_calls.values():
    total = total + count

print(total)