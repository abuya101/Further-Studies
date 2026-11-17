def count_priority_days(calls_by_day):
    priority_days = 0

    for count in calls_by_day.values():
        if count>= 7:
            priority_days = priority_days + 1

    return priority_days
from week_data import this_week



result = count_priority_days(this_week)
print("Days needing priority follow-up:", result)
