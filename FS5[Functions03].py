this_week = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 8}

def callback_priority(count):
    if count >= 7:
        return "Prioritize callbacks"
    return "Normal follow-up"

weekly_total = sum(this_week.values())
print("Total missed calls:", weekly_total)
print(callback_priority(weekly_total))

for day, count in this_week.items():
    print(day, callback_priority(count))