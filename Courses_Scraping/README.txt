pdf_scraping folder has most of the code for pdf related stuff (Not all: doesn’t include the part of actually scraping and cleaning the pdf for example)
    -Just treat it like a black box.... 
    -Important point is it creates the catalog part of the database (which I then just copied the courses.db file to the section_tally scraping folder manually)

sectiontally_scraping folder contains the logic for the scraping of section_tally
    -Note it depends on the database created from the pdf_scraping folder because the catalog database has the nicer titles 
    -"make_st_database.py" is kind of like the "driver"
    -The general idea: after web scraping section_tally, we obtain "Spring2024.html", use pandas to store and clean the data and then create the database
    -In creating the database I depend on the previously created courses.db to get the nicer title from the catalog table wherever possible
    -End result is the final database (courses.db) with both the section_tally and catalog table stored in this sectiontally_scraping folder
    
both folders contain python code to create html representation of the database just so it's easier to visualize the database
    -See catalog_database.html and st_database.html to visualize