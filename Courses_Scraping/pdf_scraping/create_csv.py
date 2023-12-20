import csv
import re
# Combine all three cleaned pdfs into one: undergrad + undergrad music catalog, grad catalog
final_list = [['subj', 'crse', 'title', 'prereq', 'description', 'level']]
####################################################################################################################################################
# Undergrad catalog
import csv
import re
def split_text_u(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Split based on 'END'
    sections_u = [section.strip() for section in content.split('END') if section.strip() != '']

    # Convert each section to a list of lines
    result_u = [section.split('\n\n') for section in sections_u]
    
    return result_u

filename_u = 'cleaned_pdf_texts/cleaned_pdf.txt'
list_of_lists_under = split_text_u(filename_u)

# Had to do sorting because PDF text is messy and out of order (inconsistent)
def custom_sort_u(inner_list):
    def sorting_key_u(line):
        # Define your conditions here
        if re.search(r'^[A-Z]{2,5} [0-9]{5}:', line):
            priority = 1
        elif re.search(r'erequisite|orequisite', line) or re.search(r'.+[A-Z]{2,5} [0-9]{5}:', line):
            priority = 3
        elif (not re.search(r'[A-Z] [0-9]{5}', line) and not re.search(r'^Prerequisit', line)) and not re.search(r'^Corequisit', line) and not len(line) > 100 and not re.search(r'This.*course', line, re.I):
            priority = 2
        elif re.search(r'This.*course', line, re.I) or len(line) > 100:
            priority = 4
        else:
            priority = 5  # Default priority, in case none of the conditions match
        return priority
    return sorted(inner_list, key=sorting_key_u)
# sort
list_of_lists_under = [custom_sort_u(inner_list) for inner_list in list_of_lists_under] 

# ensure 4 columns in same order
for course in list_of_lists_under:
    # len is def at least 2
    if len(course) == 2:
        course.append('None')
        course.append('None')
    # if 4 we're good, only problem is 3
    if len(course) == 3:
        # either missing pre-req or description
        thereis_prereq = re.search(r'erequisites:|orequisites:', course[2]) or re.search(r'.+[A-Z]{2,5} [0-9]{5}:', course[2])
        if thereis_prereq: 
            course.append('None')
        else:
            # pre-req is missing
            course.insert(2, 'None')

#Remove Colon from first column:
for course in list_of_lists_under:
    course[0] = course[0].replace(':', '')

# Split Subj-Number into 2
for lst in list_of_lists_under:
    spliited = lst[0].split(' ', 1)
    lst[0:1] = spliited


# Since this will be combined with the grad database: add a level field (grad or undergrad)
for item in list_of_lists_under:
    item.append('undergrad')
####################################################################################################################################################
# Music list (was apart of undergrad catalog but came out bad so had to manually clean)
def split_text(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Split based on 'END'
    sections_m = [section.strip() for section in content.split('END') if section.strip() != '']

    # Convert each section to a list of lines
    result_m = [section.split('\n\n') for section in sections_m]
    
    return result_m

filename_m = 'cleaned_pdf_texts/clean_music.txt'
list_of_lists_music = split_text(filename_m)

# Had to do sorting because PDF text is messy and out of order (inconsistent)
def custom_sort_m(inner_list):
    def sorting_key_m(line):
        # Define your conditions here
        words = line.split()
        num_words = len(words)
        if re.search(r'^[A-Z]{2,5} [0-9]{5}:', line):
            priority = 1
        elif re.search(r'erequisite|orequisite', line) or re.search(r'.+[A-Z]{2,5} [0-9]{5}:', line):
            priority = 3
        elif not re.search(r'The.*', line, re.I) and num_words < 6:
            priority = 2
        elif re.search(r'The.*', line, re.I) or num_words > 6:
            priority = 4
        else:
            priority = 5  # Default priority, in case none of the conditions match
        return priority
    return sorted(inner_list, key=sorting_key_m)
# sort
list_of_lists_music = [custom_sort_m(inner_list) for inner_list in list_of_lists_music] 

# ensure 4 columns in same order
for course in list_of_lists_music:
    # len is def at least 2
    if len(course) == 2:
        course.append('None')
        course.append('None')
    # if 4 we're good, only problem is 3
    if len(course) == 3:
        # either missing pre-req or description
        thereis_prereq = re.search(r'erequisites:|orequisites:', course[2]) or re.search(r'.+[A-Z]{2,5} [0-9]{5}:', course[2])
        if thereis_prereq: 
            course.append('None')
        else:
            # pre-req is missing
            course.insert(2, 'None')

#Remove Colon from first column:
for course in list_of_lists_music:
    course[0] = course[0].replace(':', '')

# Split Subj-Number into 2
for lst in list_of_lists_music:
    spliited = lst[0].split(' ', 1)
    lst[0:1] = spliited


for item in list_of_lists_music:
    item.append('undergrad')
####################################################################################################################################################
def split_text(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Split based on 'END'
    sections = [section.strip() for section in content.split('END') if section.strip() != '']

    # Convert each section to a list of lines
    result = [section.split('\n\n') for section in sections]
    
    return result

filename_g = 'cleaned_pdf_texts/grad_text_cleaned.txt'
list_of_lists_grad = split_text(filename_g)

# ensure 4 columns in same order
for course in list_of_lists_grad:
    # len is def at least 2
    if len(course) == 2:
        course.append('None')
        course.append('None')
    # if 4 we're good, only problem is 3
    if len(course) == 3:
        # either missing pre-req or description
        thereis_prereq = re.search(r'erequisites:|orequisites:', course[2]) or re.search(r'.+[A-Z]{2,5} [0-9]{5}:', course[2])
        if thereis_prereq: 
            course.append('None')
        else:
            # pre-req is missing
            course.insert(2, 'None')

#Remove Colon from first column:
for course in list_of_lists_grad:
    course[0] = course[0].replace(':', '')

# Split Subj-Number into 2
for lst in list_of_lists_grad:
    spliited = lst[0].split(' ', 1)
    lst[0:1] = spliited

# Since this will be combined with the other database: add a level field (grad or undergrad)
for item in list_of_lists_grad:
    item.append('grad')
####################################################################################################################################################
# Combine lists into 1 big list
final_list = list_of_lists_under + list_of_lists_music + list_of_lists_grad

# Create final big csv
# Wrie to CSV
# Open a CSV file for writing
with open("ALLCOMBINED.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write each list in the list of lists to the CSV
    for row in final_list:
        writer.writerow(row) 