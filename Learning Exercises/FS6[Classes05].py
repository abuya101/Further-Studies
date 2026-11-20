import json
from FS6_Classes03 import CallTracker
from week_data import this_week

#Inherit the existing attributes and methods from CallTracker
class SavedCallTracker(CallTracker):
    #Add a new method to this extended class
    def save_calls(self, filename):
        with open(filename, "w") as file:
            json.dump(self.calls_by_day, file, indent=4)


tracker = SavedCallTracker(this_week)

#this method comes from the original class

print(tracker.total_calls())

#this method belongs to the extended class
tracker.save_calls("missed_calls3.json")