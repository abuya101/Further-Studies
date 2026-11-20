import json

class CallTracker:
    def __init__(self, calls_by_day):
        #copy the dictionary so this tracker has its own data
        self.calls_by_day = calls_by_day.copy()

    def total_calls(self):
        #add all the daily call counts
        return sum(self.calls_by_day.values())

    def priority_days(self, threshold):
        #collect days whose missed calls meet of exceed the threshold
        days = []

        for day, count in self.calls_by_day.items():
            if count >= threshold:
                days.append(day)

        return days

    def save_calls(self, filename):
        #open the file for writing, then save our dictionary as JSON
        with open(filename, "w") as file:
            json.dump(self.calls_by_day, file, indent=4)


#New dictionary to act as our starting dataset

this_week = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 8,
}

#create an object that uses the CllTracker class
tracker = CallTracker(this_week)

print("Total missed calls:", tracker.total_calls())
print("Priority days:", tracker.priority_days(3))

#save this tracker data to a file
tracker.save_calls("missed_calls.json")