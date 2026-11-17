missed_calls = {"Monday": 0, "Tuesday": 3, "Wednesday": 7}

missed_calls["Thursday"] = 2
missed_calls["Friday"] = 5


for day, count in missed_calls.items():
    print(day, count)

total = sum(missed_calls.values())

print(total)
