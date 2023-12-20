# Takes Created CSV and makes sqlite database
# Final stage so high level overview of everything:
# Pdf -> Raw Text -> Cleaned Text -> Process into CSV -> SQLite DB 
import sqlite3
import csv
conn =  sqlite3.connect('courses.db')

c = conn.cursor()

c.execute("DROP TABLE IF EXISTS catalog;")
c.execute("""
CREATE TABLE IF NOT EXISTS catalog (
       subj TEXT NOT NULL,
       crse TEXT NOT NULL,
       title TEXT NOT NULL,
       prereq TEXT,
       description TEXT,
       level TEXT)""")

# Load data from the CSV file
with open('ALLCOMBINED.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # skip the header row
    for row in csv_reader:
        c.execute("""
        INSERT INTO catalog (subj, crse, title, prereq, description, level) 
        VALUES (?, ?, ?, ?, ?, ?);
        """, row)

conn.commit()
conn.close()