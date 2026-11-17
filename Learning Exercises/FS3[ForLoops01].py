daily_missed_calls = [0, 3, 4, 7, 2, 8]

for missed_calls in daily_missed_calls:
    if missed_calls == 0:
        print(missed_calls, "- You good")
    elif missed_calls <= 5:
          print(missed_calls, "- You might wanna check these")
    else:
         print(missed_calls, "- These could be an issue")