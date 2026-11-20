Let’s build a Missed Call Follow-Up Tracker: a small system that turns call records into a daily list of customers who need a callback.

It builds directly on the CallTracker exercises and introduces a core data engineering task: taking raw data, cleaning it, storing it and producing useful results.

We’ll use fictional customer details while learning.
What the finished project will do
Imagine a service business exports this call log:
Call ID	Date	Customer	Phone	Status	Duration
C001	2026-11-16	Alex	0700000001	missed	0
C002	2026-11-16	Sam	0700000002	answered	120
C003	2026-11-17	Alex	0700000001	missed	0


Your program will:
1. Read call records from a CSV file.
2. Check for missing values, invalid records and duplicate call IDs.
3. Store valid records in a SQLite database.
4. Calculate missed calls by day and customer.
5. Produce a callback list, highlighting customers with repeated missed calls.
6. Display the results on a simple PHP webpage.
7. Run automatically through Linux cron.
For Alex, the report would show two missed calls requiring follow-up. A later answered call would not automatically count as a completed callback; we’ll track follow-up separately.
How your existing lessons fit
What you have learned	How we’ll use it
Variables and data types	Store dates, call counts and customer details
Lists and dictionaries	Represent records and collect results
if statements	Validate records and assign callback priority
Loops	Process each row in a file
Functions and return	Break the work into small, reusable tasks
Imports	Share code between project files
Classes and self	Extend your existing CallTracker
File handling and JSON	Save summaries and read configuration
Virtual environments	Keep project dependencies separate
Git and GitHub	Record progress at each working milestone


We’ll add exception handling, SQL, logging, PHP and Linux automation gradually. Inheritance can wait until we have a clear reason to use it.
The roles of Python, PHP and Linux
Python processes the data. It reads files, validates records, updates the database and creates reports.

SQL stores and retrieves the data. SQLite gives us a manageable starting point for learning tables, unique IDs, queries and relationships.

PHP displays the results. We’ll begin with a page that reads Python’s JSON report. Python and SQL will carry most of the data engineering work.

Linux runs the system. You’ll practise terminal commands, file paths, permissions, logs and scheduled tasks.
We’ll build it in small milestones
Stage	Working result	New learning
1	Read a CSV and display missed-call totals	CSV files and record structure
2	Separate valid and rejected records	Validation and exception handling
3	Store calls without importing duplicates	SQLite, SQL and repeatable imports
4	Generate a callback report	Queries and business rules
5	Display the report in PHP	Basic PHP and reading JSON
6	Run automatically and record failures	Linux cron and logging
7	Document and publish the project	README, setup instructions and Git


An important goal: running the same input file twice should not double your call counts. That is a practical data engineering requirement we’ll learn to handle.

We’ll keep this project in its own folder inside your existing repository:
Further Studies/Missed-Call-Tracker/

We’ll create additional files only as each stage needs them, and I’ll explain the code with comments rather than give you the entire application at once.