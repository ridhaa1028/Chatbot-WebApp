import requests
import re
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet


class AskAboutSchedulerAction(Action):
    def name(self):
        return "action_ask_how_to_use_scheduler"

    def run(self, dispatcher, tracker, domain):
        message = (
            "Absolutely!<br>"
            "📅 *Scheduler Usage Instructions* 📅<br><br>"
            "The scheduler is a very useful tool that will allow you to see all possible schedules you can take for the Spring 2024 semester.<br>" 
            "All you need to know beforehand is the courses you need to take and their respective Subject and Course Numbers.<br>" 
            "You will need to provide the courses followed by a comma and then a number indicating the max number of schedules you want to see.<br>"
            "If you want to see all possible schedules, provide \"All\" instead of a number.<br>"
            "Optionally, followed by another comma, you can also provide an additional constraint. We offer 3 constraints: Minimize Days, Minimize Gap, and Minimize both.<br><br>"
            "Do you want to reduce the number of days you have to be in school? Use Minimize Days!<br><br>"
            "Ever had a long, boring 3 hour break between classes with nothing to do? Well, worry no more! By providing “Minimize Gap” you will<br>" 
            "get the schedules that reduce the chances of that happening with the least amount of wait time between classes on the same day.<br><br>"
            "\"Minimize Both\" will get schedules with the minimum days and then show the ones with the smallest gap.<br><br>"
            "So a message will look like: Courses, Number of Schedules [, Optional Constraint]<br><br>"
            "Here are a few examples of messages to demonstrate this. Pay specical attention to the use of commas!<br>"
            "- ACC03500 CS04400 ARAB12102 MATH01330 PHIL09213, 3, Minimize Days<br>"
            "- ACC 03500 CS 04400 ARAB 12102 MATH 01330 PHIL 09213, 12<br>"
            "- ACC03500 CS04400 ARAB12102 MATH01330 PHIL09213, 1, Minimize Both<br>"
            "- CS 04321 CS 04380 DS	02395 HIST 05150, All, Minimize Gap<br><br>"
            "Feel free to check out the User Guide for more details!"
        )
        dispatcher.utter_message(message)



class CreateScheduleAction(Action):
    def name(self):
        return "action_ask_to_create_schedule"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get('text').upper()
        message_values = user_message.split(',')
        if len(message_values) == 3:
            course_string, user_limit, constraint = message_values
        # Did not provide a specific constraint
        elif len(message_values) == 2:
            course_string, user_limit = message_values
            constraint = None
        else:
            dispatcher.utter_message("Please refer to the user guide or ask the bot on how to correctly format message for scheduler")
            return
        
        # Handling inputted limit
        if 'ALL' in user_limit:
            user_limit = -1
        elif is_string_number(user_limit):
            user_limit = int(user_limit)
        else:
            dispatcher.utter_message("Please refer to the user guide or ask the bot on how to correctly format message for scheduler")
            return
        
        # 0 if no constraint, 1 min days, 2 min gap, 3 both min days and gap
        flag = 0
        if constraint:
            if 'DAYS' in constraint:
                flag = 1
            elif 'GAP' in constraint:
                flag = 2
            else:
                flag = 3

        # Is a list of subj + # tuples: eg [('ACC', '03211'), ('ACC', '03320'), ('ENGL', '02116'), ('ENGR', '01391'), ('XYZ', '22223')]
        course_list = extract_from_user(course_string)

        # Will send course_list, user_limit and flag as parameters to flask endpoint
        api_url = "http://localhost:5000/create_schedule"
        payload = {
            'course_list': course_list,
            'limit': user_limit,
            'constraint': flag
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            schedules_data = response.json().get('schedules', [])
            if schedules_data:
            # Format and send the schedules to the user
                message = "Found the following Schedules for Spring 2024:<br><br>"
                for schedule in schedules_data:
                    for course in schedule:
                        message += f"{course['title']} with {course['prof']} with Timing {course['timing']} [CRN={course['crn']}]<br>" + " "
                    message += "<br><br>"
                dispatcher.utter_message(message)
            else:
                dispatcher.utter_message("No schedules were found based on the given criteria.")

            
        elif response.status_code == 400:
            error_data = response.json()
            if "not_found" in error_data:
                not_found_courses = ", ".join(error_data["not_found"])
                m1 = f"Could not create schedule. The following courses were not found: {not_found_courses}"
                m2 = f"<br> It is either not being offered for Spring 2024 or there is no such course in the University"
                dispatcher.utter_message(m1 + m2)
                return
        
        else:
            # Handle other errors
            dispatcher.utter_message("Sorry, there was a problem generating the schedule.")

def is_string_number(s):
    try:
        int(s)  # Try converting to an integer
        return True
    except ValueError:
        return False
def extract_from_user(string):

    # Not strict in terms of capitalization
    # Now SQL Query can always expect good inputs
    string = string.upper()
    
    # Ensure no extra spaces - strip whitespace/extraspace
    string = re.sub(' +', ' ', string).strip()

    # match all, space between subject and number is optional
    # list of (subj, number) string tuples
    return re.findall(r'([a-z]{2,5})\s?(L[0-9]{4}|[0-9]{2,5})', string, re.I)