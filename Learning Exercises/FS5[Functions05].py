def find_priority_days(calls_by_day):
    priority_days = [] #start with an empty list

    for day, count in calls_by_day.items():
        if count >= 7:
            priority_days.append(day)

    return priority_days

from week_data import this_week

days = find_priority_days(this_week)

print ("Number of priority days is:", len(days))
print ("They are:", ",".join(days))
