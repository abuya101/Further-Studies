from week_data import this_week, another_week

class CallTracker:
    def __init__(self, calls_by_day):
        #store the dictionary on this tracker
        self.calls_by_day = calls_by_day

    def total_calls(self):
        #Calculate the total using the trackers data
        return sum(self.calls_by_day.values())

    def update_day(self, day, count):
        #set the missed call count for this day
        self.calls_by_day[day] = count

tracker = CallTracker(this_week)
second_tracker = CallTracker(another_week)

print("Before:", second_tracker.total_calls())

second_tracker.update_day("Monday", 6)

print("After:", second_tracker.total_calls())