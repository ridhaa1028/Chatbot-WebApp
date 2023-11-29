Probably messy right now and will need to be refactored a lot to integrate properly with the final application

General rundowm:

entry_point.py is the entry point and calls rest of the code (to test the functionality just run entry_point.py)
Right now it is set up with the schedule you want to create being represented by the hardcoded user_string variable.
user_string is flexible - as long as it includes courses that follow the general pattern of [subj][#] in some way (see function extract_from_user())
Another thing hardocded is the "limit" variable that decides the max number of possible schedules to return

4 solve variations total:
basic: return any schedule as long as it is a schedule
minimizeDays: from all possible schedules return the schedule(s) with the minimum number of total days
minimizeGap: from all possible schedules return the schedule(s) with the minimum number of total gap/break between classes (the 15 minutes between time blocks doesn't count)
minimizeGapAndDays: combination of both - first reduces to minimum days and from those select the smallest total gap
