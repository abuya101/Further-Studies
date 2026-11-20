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