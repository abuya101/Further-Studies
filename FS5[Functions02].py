this_week = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}
next_week ={"Sunday": 5, "Monday": 4, "Tuesday": 3}

def add_missed_calls(x, y):
    return x + y

this_week_total = sum(this_week.values())
next_week_total = sum(next_week.values())

total = add_missed_calls(this_week_total, next_week_total)

print(total)