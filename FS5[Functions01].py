def total_missed_calls(calls_by_day):
    #Add the counts and give back the total
    return sum(calls_by_day.values())

this_week = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}
next_week ={"Sunday": 5, "Monday": 4, "Tuesday": 3}

weekly_total = total_missed_calls(next_week)
last_week_total = total_missed_calls(this_week)
print(weekly_total, last_week_total)