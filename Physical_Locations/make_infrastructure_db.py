import sqlite3
import kml2geojson
import re

json_data_list = kml2geojson.convert('MainCampusGlassboro.kml')
data_dict = json_data_list[0]

# Notes
# kml2geojson.convert(kml_file) returns a list of one dict
# dict has two keys: type, features
# what we need is features whose values are a list

conn =  sqlite3.connect('infrastructure.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS locations;")
# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        keywords TEXT,
        categories TEXT, 
        latitude INTEGER,
        longitude INTEGER,
        departments TEXT
    )
''')
# Function to replace empty strings with 'None'
def get_value_or_none(key):
    value = properties.get(key, 'None')
    return 'None' if value == '' else value

def clean_description_location(description):
    # This function will remove the "<br>Location: latitude,longitude" from the description
    if "<br>Location:" in description:
        # Using regular expression to remove the unwanted pattern
        description = re.sub(r'<br>Location: [-+]?[0-9]*\.?[0-9]+,[-+]?[0-9]*\.?[0-9]+', '', description)
    return description.strip()

def clean_description_keyword(description):
    # This function will remove the "<br>Location: latitude,longitude" from the description
    if "<br><br>Keywords:" in description:
        # Using regular expression to remove the unwanted pattern
        description = re.sub(r'<br><br>Keywords.*', '', description)
    return description.strip()

def clean_description_keyword_other(description):
    # This function will remove the "<br>Location: latitude,longitude" from the description
    if "<br>Keywords:" in description:
        # Using regular expression to remove the unwanted pattern
        description = re.sub(r'<br>Keywords.*', '', description)
    return description.strip()

rows = []
for i in range(len(data_dict['features'])):
    properties = data_dict['features'][i]['properties']
    geometry = data_dict['features'][i]['geometry']

    name = get_value_or_none('name')
    description = get_value_or_none('description')
    keywords = get_value_or_none('Keywords')
    categories = get_value_or_none('Categories')
    latitude = geometry['coordinates'][1]
    longitude = geometry['coordinates'][0]

    rows.append([name, description, keywords, categories, latitude, longitude])

# Cleaning Data   
for i in range(len(rows)):
    rows[i][1] = clean_description_location(rows[i][1])
    rows[i][1] = clean_description_keyword(rows[i][1])
    rows[i][1] = clean_description_keyword_other(rows[i][1])

for i in range(len(rows)):
    if 'Restrooms' in rows[i][3]:
        rows[i][0] = rows[i][0] + ' Restrooms'

# Parking rows are uniquely dirty 
for i in range(len(rows)):
    if 'Parking' in rows[i][0]:
        rows[i][3] = rows[i][0]
        break_text = rows[i][1].split("<br>")
        rows[i][0] = break_text[0]
        rows[i][1] = break_text[1]
        rows[i][0] = rows[i][0].split(": ")[1]
        rows[i][1] = rows[i][1].split(": ")[1]

# Buildings home to departments have that info in the description
# Probably want to add to it's own column and use if needed (may not even need)
for i in range(len(rows)):
    rows[i].append("None")
    break_text = rows[i][1].split("Departments: ")
    if len(break_text) > 1:
        rows[i][1] = break_text[0]
        rows[i][6] = break_text[1]

for i in range(len(rows)):
    break_text = rows[i][1].split("Departments:")
    if len(break_text) > 1:
        rows[i][1] = break_text[0]
        rows[i][6] = break_text[1]

# Inserting Python data into sqlite
for i in range(len(rows)):
    c.execute('''
        INSERT INTO locations (name, description, keywords, categories, latitude, longitude, departments) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (rows[i][0], rows[i][1], rows[i][2], rows[i][3], rows[i][4], rows[i][5], rows[i][6]))

conn.commit()
conn.close()
