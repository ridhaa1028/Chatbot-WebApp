# Clean Section Tally Data
def fix_spacing(courses):
    courses = courses[~courses.apply(lambda row: row.str.isspace().all(), axis=1)]
    courses.reset_index(drop=True, inplace=True)
    return courses

def clean_columns(val):
    if isinstance(val, str):
        val = "".join(char for char in val if char.isalnum() or char in (" ", "_"))
        # convert to snake case
        val = val.strip().lower().replace(" ", "_")
        return val
    else:
        return val
    
def convert_floats(df):
    df['crn'] = df['crn'].astype(int) 
    df['hrs'] = df['hrs'].astype(int) 
    df['avail'] = df['avail'].astype(int) 

