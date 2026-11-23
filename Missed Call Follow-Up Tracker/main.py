# Import Python's built-in tools for reading CSV files
import csv
# Import Path to help locate files on your computer
from pathlib import Path
# Define a function that receives the location of a CSV file
from validation import (is_valid_status, 
                        is_valid_duration, 
                        is_valid_date, 
                        is_valid_call_id,
                        validate_columns,
                        has_complete_row,
                        )
from reporting import save_summary, export_callback_candidates
from database import (initialize_database,
                      save_calls, 
                      count_stored_calls, 
                      get_missed_calls_by_day,
                      get_callback_candidates,
                      )

from config import CALLBACK_THRESHOLD
import logging #Pythons inbuilt tool for recording events

import sqlite3 #Access SQLites db exception types

def summarize_calls(filename):
    #Start our counters at zero
    total_calls = 0
    missed_calls = 0
    invalid_calls = 0
    duplicate_calls = 0
    # Store call IDs already encountered during this run
    seen_call_ids = set()
    #Collect records that pass every check
    valid_calls = []
    #Store each date and its missed call count
    # Create an empty dictionary to hold missed-call counts by date
    # Example: {"2026-11-16": 1, "2026-11-17": 2}
    missed_by_day = {}

    # Open the CSV file:
    # "r" means read mode
    # newline="" lets the csv module handle line endings
    # encoding="utf-8" specifies how to read the text
    # "with" automatically closes the file when this block finishes
    with open(filename, "r", newline="", encoding="utf-8") as file:
        #read each row as a dictionary using the column names. Each remaining row becomes a dictionary.
        reader = csv.DictReader(file)

        #Check the header before processing any records
        validate_columns(reader.fieldnames)

        for call in reader:
            total_calls += 1
            date = call["date"]
            #Reject rows with missing or extra fields
            if not has_complete_row(call):
                invalid_calls += 1

                logging.warning(
                    "CSV line %s: missing or extra fields",
                    reader.line_num,
                )
                continue
            #Remove accidental spaces around the call ID
            call_id = call["call_id"].strip()

            #Reject a call with no ID 
            if not is_valid_call_id(call_id):
                invalid_calls += 1

                logging.warning(
                    "CSV line %s: missing call ID",
                    reader.line_num,
                )
                continue

            #Skip this record if its ID has already appeared
            if call_id in seen_call_ids:
                duplicate_calls += 1

                #Record the detail in tracker.log instead of printing it in terminal
                logging.warning("Duplicate call skipped: %s", call_id)
                continue

            #Remember this ID before processing the rest of the record
            seen_call_ids.add(call_id)

            # Remove spaces from both ends and convert the status to lowercase
            status = call["status"].strip().lower()

            #reject statuses outside our two accepted values
            if not is_valid_status(status):
                invalid_calls += 1

                #show which record needs correcting
                # %r displays quotes, making blank values and spaces visible
                logging.warning(
                    "Invalid status in call %s: %r",
                    call_id,
                    call["status"],
                )
                #skip the rest of the iteration and read the next record
                continue
            # Converting the call duration from text into a whole number
            if not is_valid_duration(call["duration_seconds"]):
                invalid_calls += 1

                logging.warning(
                    "CSV line %s: invalid duration in call %s: %r",
                    reader.line_num,
                    call_id,
                    call["duration_seconds"],
                )
                continue
            # Remove spaces surrounding the date
            call_date = call["date"].strip()

            # Reject records with an invalid date
            if not is_valid_date(call_date):
                invalid_calls += 1

                logging.warning(
                    "CSV line %s: invalid date in call %s: %r",
                    reader.line_num,
                    call_id,
                    call["date"],
                )
                continue
            #Build a cleaned record using consistent values and types
            cleaned_call = {
                "call_id": call_id,
                "date": date,
                "customer": call["customer"].strip(),
                "phone": call["phone"].strip(),
                "status": status,

                #validation confirmed that this can be an integer
                "duration_seconds": int(call["duration_seconds"]),
            }
            #Add this dictionary as one item on our list
            valid_calls.append(cleaned_call)
            # Compare the cleaned value
            if status == "missed":

                # Add 1 to the overall missed-call count
                missed_calls += 1

                #start a counter when we encounter a date for the first time
                if call_date not in missed_by_day:
                    missed_by_day[call_date] = 0

                missed_by_day[call_date] += 1

    #Return the results together in a dictionary
    return {
        "total_calls": total_calls,
        "missed_calls": missed_calls,
        "invalid_calls": invalid_calls,
        "missed_by_day": missed_by_day,
        "duplicate_calls": duplicate_calls,
        "valid_call_count": len(valid_calls),
        "valid_calls": valid_calls,
    }

if __name__ == "__main__":
    # Locate the folder containing this script
    project_folder = Path(__file__).resolve().parent

    #Store the log in our working folder
    log_file = project_folder / "tracker.log"

    #Append events to the log, including their time and severity
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8"
    )

    logging.info("Import started")

    # Build paths for the input data and output report
    data_file = project_folder / "calls.csv"
    report_file = project_folder / "summary.json"
    try:
        # Attempt to read and process the input file
        summary = summarize_calls(data_file)


    except FileNotFoundError:
        #Record the missing input file in tracker.log
        logging.error("Import failed: input file not found: %s", data_file)

        #Also explain the problem to the person running the program
        print(f"Input file not found: {data_file}")
        print("Place calls.csv beside main.py and run again.")

        #Tell Linux that the run failed
        raise SystemExit(1)

    except ValueError as error:
        #Record the validation error and its explanation
        logging.error("Import failed: %s", error)

        print(f"Invalid input file: {error}")
        raise SystemExit(1)
    

    else:
        #locate the db inside main.py
        database_file = project_folder / "calls.db"
        try:
            #Create the database and tables if not existent
            initialize_database(database_file)

            #Save only the records that passed validation
            inserted_calls = save_calls(database_file, summary["valid_calls"])

            #Count valid records whose IDs are already in the database
            existing_calls = summary["valid_call_count"] - inserted_calls
            # Read the total directly from SQLite
            summary["stored_calls"] = count_stored_calls(database_file)

            #Include the import results in the JSON report
            summary["inserted_calls"] = inserted_calls
            summary["existing_calls"] = existing_calls

            #Calculate daily missed call totals from the stored db records
            summary["database_missed_by_day"] = get_missed_calls_by_day(database_file)
            # Get follow-up candidates from all stored missed calls
            summary["callback_candidates"] = get_callback_candidates(database_file,
                                                                     threshold=CALLBACK_THRESHOLD)
            summary["callback_threshold"] = CALLBACK_THRESHOLD
        except sqlite3.Error:
            #Save the error mesage and traceback in tracker.log
            logging.exception("Import failed during database operations")

            print("Database operation failed during database operations")
            raise SystemExit(1)
        try:
            # Run this section only if processing finished without an error
            save_summary(summary, report_file)
            #Build the callback csv path beside main.py
            callback_file = project_folder / "callback_candidates.csv"

            #Export the candidates already retrieved from SQLite
            export_callback_candidates(
                summary["callback_candidates"],
                callback_file,
            )
        except OSError:
            #Handle file writing problems, such as permission errors
            logging.exception("Import failed while saving the JSON report")

            print("Could not import file, check tracker.log for details.")
            raise SystemExit(1)

        #Record completion only after both stages succeed
        logging.info(
            "Import completed | total=%s valid=%s invalid=%s duplicate=%s",
            summary["total_calls"],
            summary["valid_call_count"],
            summary["invalid_calls"],
            summary["duplicate_calls"],
        )

        # Display each final counter once
        print("Total calls:", summary["total_calls"])
        print("Missed calls:", summary["missed_calls"])
        print("Invalid calls:", summary["invalid_calls"])
        print("Duplicate calls:", summary["duplicate_calls"])
        print("Valid calls:", summary["valid_call_count"])
        print("New calls saved:", summary["inserted_calls"])
        print("Calls already stored:", summary["existing_calls"])
        print("Total calls in database:", summary["stored_calls"])

        print("\nMissed calls by day:")

        for call_date, count in summary["missed_by_day"].items():
            print(f"{call_date}: {count}")

        print("\nMissed calls by day — database:")

        # Display the totals returned by our SQL query
        for call_date, count in summary["database_missed_by_day"].items():
            print(f"{call_date}: {count}")

        print("\nCallback candidates - db:")

        #Retrieve the list from our summary dictionary
        candidates = summary["callback_candidates"]

        if not candidates:
            print("No callback candidates found")
        else:
            #Display one line per phone number
            for candidate in candidates:
                phone = candidate["phone"]
                count = candidate["missed_count"]
                priority = candidate["priority"]

                print(f"{phone}: {count} missed calls | Priority: {priority}")