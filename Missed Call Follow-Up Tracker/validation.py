#Import Python's date type for checking calendar dates
from datetime import date
def is_valid_status(status):
    #check if the cleaned status is what we require
    return status in ("answered", "missed")

def is_valid_duration(value):
    #try converting the duration value into a whole number
    try:
        duration = int(value)
    except ValueError:
        #Conversion failed, duration is invalid
        return False

    #Return true for zero or positive durations, otherwise false
    return duration >= 0

def is_valid_date(value):
    #Check the structure: YYYY, MM, DD
    parts = value.split("-")

    if len(parts) != 3:
        return False

    year, month, day = parts

    if len(year) != 4 or len(month) !=2 or len(day) != 2:
        return False

    #check that the value represents a real calendar date
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True

def is_valid_call_id(value):
    #Remove surrounding spaces. An empty string becomes False
    return bool(value.strip())

def validate_columns(fieldnames):
    #List the column names our DB requires
    required_columns = {
        "call_id",
        "date",
        "phone",
        "status",
        "duration_seconds"
    }

    #Use an empty set for a file with no header or is empty
    actual_columns = set(fieldnames or [])

    #Set subtraction finds required columns that are absent
    missing_columns = required_columns - actual_columns

    if missing_columns:
        #sort the names and join them into a readable message
        missing_names = ",".join(sorted(missing_columns))
        #Signal that the inout file has an invalid structure
        raise ValueError(f"Missing required columns: {missing_names}")

def has_complete_row(call):
    # DictReader uses the key None for extra fields.
    # Reject rows with more fields than the header.
    if None in call:
        return False

    #Missing fields receive the value None. Che that every column has a supplied field
    return all(value is not None for value in call.values())