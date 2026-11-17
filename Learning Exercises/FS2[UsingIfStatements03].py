missed_calls = 5

if missed_calls == 0:
    print("No need to follow up")
elif missed_calls >= 4:
    print("Prioritize callbacks")
else:
    print("Add callbacks to todo list")
