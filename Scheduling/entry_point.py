# Main "Entry" point of algorithm
# Right now the user query is just hard coded into the code as "user_string"

from schedule_models import *
from extract_times import *
from solve_basic import * # Change this to change which algo is ran 
import re

# Flexible in terms of strings it accepts (Regex!)
# Examples:
"""
"ACC 03211 ACC 03320 ENGL 02116 ENGR 01391 and, XYZ 22223"
[('ACC', '03211'), ('ACC', '03320'), ('ENGL', '02116'), ('ENGR', '01391'), ('XYZ', '22223')]

"ACC03211 ACC03320 ENGL 02116 ENGR01391   XYZ 22223"
[('ACC', '03211'), ('ACC', '03320'), ('ENGL', '02116'), ('ENGR', '01391'), ('XYZ', '22223')]
""" 
def extract_from_user(string):

    # Not strict in terms of capitalization
    # Now SQL Query can always expect good inputs
    string = string.upper()
    
    # Ensure no extra spaces - strip whitespace/extraspace
    string = re.sub(' +', ' ', string).strip()

    # match all, space between subject and number is optional
    # list of (subj, number) string tuples
    return re.findall(r'([a-z]{2,5})\s?(L[0-9]{4}|[0-9]{5})', string, re.I)

user_string = "CS 04400 CS 06395 PHIL 09151 ARAB 12102"
#user_string = "HLT 00103 INTR 01107 CS 06205"

course_list = extract_from_user(user_string)

# Run query to get all possible sections of each course
results = fetch_course(course_list)

def check_none_possible():
    # Get unique titles from the results
    unique_titles_from_results = {course.title for course in results}
    # If the number of unique titles doesn't match the length of user's input list
    if len(unique_titles_from_results) != len(course_list):
        print("One or more courses not found in the database.")
        unique_combo = {course.subj + " " + course.crse for course in results}
        all_combo = {p[0]+" "+ p[1] for p in course_list}
        not_found = [i for i in unique_titles_from_results]
        for not_found in [i for i in all_combo if i not in unique_combo]:
            print("Not Found ->", not_found)
        raise Exception("Can't make Schedule")

check_none_possible()

# CSP Solver will take in a list of lists representing each possible section
# Eg: [crn, subj+crse, list of Day Start End Time block Strings]
# Example list: a list of many sections like [22143, 'ARAB12102', ['M 1100 1215', 'W 1100 1215']]
input_to_algo = []
for c in results:
    input_to_algo.append([c.crn, c.subj + c.crse, extract_times(c.day_beg_end_bldgroom_type)])

# limit is max number of schedules possible to produce

limit = float('inf') # if you want all just do infinite 
# limit = 1

# Returns a list of list of crns as the representation of all schedules
schedules = do_solve(input_to_algo, limit)

# Now that we have crns, can see exact schedule by querying
for schedule in schedules:
    for c in detail_schedule(schedule):
        print(f"{c.crn}, {c.subj}-{c.crse}, {c.title}, WITH {c.prof}, {c.day_beg_end_bldgroom_type}, AVAIL {c.avail}")
    print("") 