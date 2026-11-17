from week_data import this_week, another_week

class CallTracker:
    def __init__(self, calls_by_day):
        #store the dictionary on this tracker
        self.calls_by_day = calls_by_day

    def total_calls(self):
        #Calculate the total using the trackers data
        return sum(self.calls_by_day.values())

tracker = CallTracker(this_week)
second_tracker = CallTracker(another_week)

print(second_tracker.total_calls())
print(tracker.total_calls())