import json
import os
import tempfile
from pathlib import Path
from datetime import datetime, timezone
import csv

def save_summary(summary, filename):
    #Convert the supplied filename into a Path Object
    report_file = Path(filename)
    #copy the dictionary so we dont change the original summary
    report = summary.copy()

    #Report the current time in UTC. isoformat() produces a std date time string
    report["generated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    #Take note the temporary file's location for cleanup
    temporary_file = None

    try:
        # Create a uniquely named temporary file beside the report.
        # Keeping both files in the same folder allows atomic replacement.
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=report_file.parent,
            prefix=".summary-",
            suffix=".tmp",
            delete=False,
        ) as file:
            temporary_file = Path(file.name)

            #write the complete report to the temp file
            json.dump(report, file, indent=4)
        #The temp file is now closed. Replace the old report with the completed new report
        os.replace(temporary_file, report_file)

    finally:
        # Remove the temporary file if it still exists after a failure.
        # After successful replacement, its old path no longer exists.  
        if temporary_file is not None:
            temporary_file.unlink(missing_ok=True) 

def export_callback_candidates(candidates, filename):
    #Open a CSV file for writing. newline="" lers the csv module manage line endings
    with open(filename, "w", newline="", encoding="utf-8") as file:
        #Define the column names and their order
        columns = ["phone", "missed_count", "priority"]

        #create a writer that accepts dictionaries
        writer = csv.DictWriter(file, fieldnames=columns)

        #Write the column headings
        writer.writeheader()

        #Write one row for each callback candidate
        writer.writerows(candidates)