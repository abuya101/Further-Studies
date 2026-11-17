#Next, let’s learn how a function can return two results: the names of priority days and their total missed calls.
from week_data import this_week

def priority_report(calls_by_day, cutoff):
    days = []
    total = 0

    for day, count in calls_by_day.items():
        if count >= cutoff:
            days.append(day) #collects the days name
            total = total + count #adds its missed calls
    return days, total

priority_days, priority_total = priority_report(this_week, 4)

print("Priority days:", priority_days)
print("Total missed calls:", priority_total)