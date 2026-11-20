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