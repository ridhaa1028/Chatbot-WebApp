from scrape_st import *
from clean_st_data import *
import sqlite3
import pandas as pd

# First get the html file into pandas dataframe

# scrape_site returns section_tally html  
path = scrape_site()

# read in the tables in the html
tables = pd.read_html(path)
# the 2nd table is what we need
section_tally = tables[1]

# Cleaning Step
# Remove rows where all values are spaces
section_tally = section_tally[~section_tally.apply(lambda row: row.str.isspace().all(), axis=1)]

# Fix names of some columns
section_tally = section_tally.rename(columns=clean_columns)

# Only keep columns we actually need (remove unnecessary columns)
section_tally = section_tally[['crn','subj','crse','sect','title','prof','day_beg_end_bldgroom_type', 'hrs', 'avail']]

# convert float types to ints
convert_floats(section_tally)

# Create Database
conn =  sqlite3.connect('courses.db')
c = conn.cursor()

# Drop the section_tally table if it exists
c.execute("DROP TABLE IF EXISTS section_tally;")
c.execute("""
CREATE TABLE IF NOT EXISTS section_tally (
       crn INTEGER PRIMARY KEY,
       subj TEXT NOT NULL,
       crse TEXT NOT NULL,
       sect TEXT NOT NULL,
       title TEXT NOT NULL,
       prof TEXT,
       day_beg_end_bldgroom_type TEXT,
       hrs INTEGER NOT NULL,
       avail INTEGER
                
)""")
section_tally.to_sql('section_tally', conn, if_exists='append', index=False)
c.execute("""
UPDATE section_tally AS st
SET title = COALESCE(
    (
        SELECT title FROM catalog AS c
        WHERE st.subj = c.subj AND st.crse = c.crse
    ),
    title
)
""")
conn.commit()
