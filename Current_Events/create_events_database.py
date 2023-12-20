from icalendar import Calendar
from datetime import datetime
from pytz import timezone
import sqlite3

def convert_time(original_time):
    # Convert to Philadelphia time
    rowan_time = original_time.astimezone(timezone('America/New_York'))
    return rowan_time.strftime('%Y-%m-%d %H:%M:%S')
    # Note for sql queries can use: datetime(time_string) for time operations

file_path = 'events.ics'

# Open the file and read its content
with open(file_path, 'rb') as f:
    cal_data = f.read()

# Parse the calendar
cal = Calendar.from_ical(cal_data)

conn =  sqlite3.connect('events.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS events;")
# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        host TEXT,
        location TEXT,
        start TEXT,
        end TEXT,
        last_modified TEXT,
        url TEXT
    )
''')

for component in cal.walk():
    if component.name == "VEVENT":
        name = component.get('summary')
        description = component.get('description').split("Additional Information can be found at:")[0]
        parts = description.split("Hosted by:")
        description = parts[0].strip()
        host = None
        if len(parts) > 1:
            host = parts[1].strip()
        location = component.get('location')
        start = convert_time(component.get('dtstart').dt)
        end = convert_time(component.get('dtend').dt)
        last_modified = convert_time(component.get('dtstamp').dt) #Note this MAY not be accurate if scraped data is old
        url = component.get('url')

        c.execute('''
            INSERT INTO events (name, description, host, location, start, end, last_modified, url) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, host, location, start, end, last_modified, url))
    
conn.commit()
conn.close()
