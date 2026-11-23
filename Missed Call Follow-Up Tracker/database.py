import sqlite3

def initialize_database(filename):
    #open the database, creating the file if it does not exist
    connection = sqlite3.connect(filename)

    try:
        #Create a table for our records, make this safe to run should it not exist
        connection.execute("""
            CREATE TABLE IF NOT EXISTS calls(
                call_id TEXT PRIMARY KEY NOT NULL,
                date TEXT NOT NULL,
                customer TEXT NOT NULL,
                phone TEXT NOT NULL,
                status TEXT NOT NULL
                    CHECK (status IN ('answered', 'missed')),
                duration_seconds INTERGER NOT NULL\
                    CHECK (duration_seconds >= 0)
            )
        """)
        #save the database changes
        connection.commit()

    finally:
        #close the connection even if an error occurs
        connection.close()

def save_calls(filename, calls):
    #open the existing database
    connection = sqlite3.connect(filename)
    #count records inserted during this run
    inserted_calls = 0

    try:
        for call in calls:
            #insert one cleaned record. no duplicates 
            cursor = connection.execute("""
                INSERT INTO calls (
                call_id,
                date,
                customer,
                phone,
                status,
                duration_seconds
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(call_id) DO NOTHING
                """, (
                    call["call_id"],
                    call["date"],
                    call["customer"],
                    call["phone"],
                    call["status"],
                    call["duration_seconds"],
                ))
                # rowcount is 1 for an inserted record, 0 for skipped ID
            inserted_calls += cursor.rowcount
            #Save all successful inserts together
            connection.commit()
    except sqlite3.Error:
         #Undo this batch if a database operation fails
         connection.rollback()

         #Pass the error back to the calling node
         raise
    finally:
        #Always close the db connection
        connection.close()

    return inserted_calls

def count_stored_calls(filename):
    #open our database
    connection = sqlite3.connect(filename)

    try:
        #Ask SQLite to count every row in the calls table
        cursor = connection.execute("SELECT COUNT(*) FROM calls")

        #Retrieve the result as a tuple, eg (7)
        result = cursor.fetchone()

        #Return the number inside the tuple
        return result[0]
    finally:
        #Close the connection as always
        connection.close()

def get_missed_calls_by_day(filename):
    #Open the database connection
    connection = sqlite3.connect(filename)

    try:
        # Filter for missed calls, group them by date,
        # and count the records in each group
        cursor = connection.execute("""
            SELECT date, COUNT(*) AS missed_count FROM calls WHERE status = 'missed' GROUP BY date ORDER BY date
        """)
        #Retrieve the results as a list of tuples. 
        rows = cursor.fetchall()

        #Convert the results into a dictionary
        missed_by_day = {}

        for call_date, missed_count in rows:
            missed_by_day[call_date] = missed_count

        return missed_by_day
    finally:
        #Always close the connection
        connection.close()

def get_callback_candidates(filename, threshold=2):
    #Open our existing database
    connection = sqlite3.connect(filename)

    try:
        #Group missed calls by phone number, showing callers with the most missed calls first
        cursor = connection.execute("""
            SELECT phone, COUNT(*) AS missed_count
            FROM calls
            WHERE status = 'missed'
                AND phone != ''
            GROUP BY phone
            ORDER BY missed_count DESC, phone ASC
        """)

        #Collect the query results
        rows = cursor.fetchall()

        #Build a list of dictionaries for reporting
        candidates = []

        for phone, missed_count in rows:
            #Two or more missed calls trigger priority follow-up
            if missed_count >= threshold:
                priority = "High"
            else:
                priority = "Normal"

            candidates.append({
                "phone": phone,
                "missed_count": missed_count,
                "priority": priority,
            })
        return candidates
    finally:
        connection.close()
