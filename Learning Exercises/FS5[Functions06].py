from week_data import this_week

def total_priority_calls(calls_by_day):
    total = 0

    for count in calls_by_day.values():
        if count >= 7:
            total = total + count #Add the calls, not just 1

    return total #Return after checking every day
    
result = total_priority_calls(this_week)
print("Missed calls on priority days:", result)