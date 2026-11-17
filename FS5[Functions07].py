from week_data import this_week

def total_priority_calls(calls_by_day, threshold=7):
    total = 0

    for count in calls_by_day.values():
        if count >= threshold:
            total = total + count
    return total

#No threshold provided, so python uses 7
print(total_priority_calls(this_week))

#supply a threshold example
print(total_priority_calls(this_week, 9))