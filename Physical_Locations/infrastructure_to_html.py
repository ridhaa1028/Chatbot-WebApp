# Create html file to visualize all the catalog data
# Requires courses database with "catalog" table
import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('infrastructure.db')

# Fetch all table names from the database
table_names = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
table_names = [name[0] for name in table_names]

# Use Pandas to read each table and convert to HTML
html_parts = []
table_name = "locations" 
df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
html_parts.append(f"<h2>{table_name}</h2>")
html_parts.append(df.to_html(border=1, classes="table").replace("\\n"," "))

# Combine and save to an HTML file
with open("visualize_locs_db.html", "w") as f:  
    f.write("""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .table {
                border-collapse: collapse;
                width: 100%;
            }
            .table th, .table td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }
        </style>
    </head>
    <body>
    """)
    
    for html_part in html_parts:
        f.write(html_part)
    
    f.write("""
    </body>
    </html>
    """)

# Close the database connection
conn.close()