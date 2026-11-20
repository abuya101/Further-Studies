import json
from datetime import datetime, timezone

def save_summary(summary, filename):
    #copy the dictionary so we dont change the original summary
    report = summary.copy()

    #Report the current time in UTC. isoformat() produces a std date time string
    report["generated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    #Open the output file for writing. "w" creates the file, can also rewrite it
    with open(filename, "w", encoding="utf-8") as file:
        #convert the summary dictionary into jso then save it
        json.dump(summary, file, indent=4)