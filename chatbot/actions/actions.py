# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

class GetAllClassesAction(Action):
   def name(self):
       return "action_get_all_classes"

   def run(self, dispatcher, tracker, domain):
       # Make a GET request to your API
       api_url = "http://localhost:5000/backend/all_data"  # Update with your API URL
       response = requests.get(api_url)

       if response.status_code == 200:
           data = response.json()

           if data:
               # Format the response to display all columns for each class
               class_info = "\n".join([
                   f"CRN: {item['crn']}, Subject: {item['subject']}, Course: {item['crse']}, " 
                   f"Sect: {item['sect']}, Title: {item['title']}, Prof: {item['prof']}, " 
                   f"Details: {item['day_beg_end_bldgroom_type']}, Hrs: {item['hrs']}, " 
                   f"Availability: {item['avail']}"
                   for item in data
               ])

               # Send the formatted response to the user
               dispatcher.utter_message(f"Here are all the classes:\n{class_info}")
           else:
               dispatcher.utter_message("There are no classes available.")
       else:
           dispatcher.utter_message("Sorry, I couldn't retrieve the class information at the moment.")

       return []


import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

class GetCourseSectionsAction(Action):
    def name(self):
        return "action_get_course_sections"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        # Extract the course name from the slot or entity
        course_name = tracker.get_slot("title")

        if course_name:
            # Make a GET request to your API to filter by 'title'
            api_url = "http://localhost:5000/data_by_column"  # Update with your API URL
            params = {'column_name': ['title'], 'column_value': [course_name]}

            # Send an empty JSON object in the request body
            data = {}

            # Set the headers to specify that you're sending JSON
            headers = {"Content-Type": "application/json"}

            response = requests.get(api_url, params=params, json=data, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if data:
                    # Format the response to display course sections
                    formatted_sections = []

                    for item in data:
                        section_info = "<br>".join([f"{key}: {value}" for key, value in item.items()])
                        formatted_sections.append(section_info)

                    # Create a message with HTML line breaks
                    message = f"Here are all the sections for '{course_name}':<br><br>"
                    message += "<br>".join(formatted_sections)

                    # Send the message with custom formatting
                    dispatcher.utter_message(message)
                else:
                    dispatcher.utter_message(f"Sorry, no sections found for '{course_name}'.")
            else:
                dispatcher.utter_message("Sorry, I couldn't retrieve the course sections at the moment.")
        else:
            dispatcher.utter_message("I couldn't find a course name in your message.")

        return [SlotSet("title", None)]







class GetCourseSubjectAction(Action):
    def name(self):
        return "action_get_course_subjects"

    def run(self, dispatcher, tracker, domain):
        # Extract the course name from the user's message
        course_name = tracker.latest_message['text']

        # Make a GET request to your API to filter by 'crse'
        api_url = "http://localhost:5000/data_by_column"  # Update with your API URL
        params = {'column_name': 'subj', 'column_value': course_name}

        # Send an empty JSON object in the request body
        data = {}

        # Set the headers to specify that you're sending JSON
        headers = {"Content-Type": "application/json"}

        response = requests.get(api_url, params=params, json=data, headers=headers)

        if response.status_code == 200:
            data = response.json()

            if data:
                # Format the response to display all columns for each matching course section
                formatted_sections = []
                for item in data:
                    section_info = "\n".join([f"{key}: {value}" for key, value in item.items()])
                    formatted_sections.append(section_info)

                message = f"Here are all the sections for '{course_name}':\n\n"
                message += "\n\n".join(formatted_sections)
                dispatcher.utter_message(message)
            else:
                dispatcher.utter_message(f"Sorry, no classes found for '{course_name}'.")
        else:
            dispatcher.utter_message("Sorry, I couldn't retrieve the course sections at the moment.")

        return [SlotSet("course_name", course_name)]

class ActionGetProfessorSection(Action):
    def name(self):
        return "action_get_professor_classes"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        # Extract the course name from the slot or entity
        professor = tracker.get_slot("professor")

        if professor:
            # Make a GET request to your API to filter by 'title'
            api_url = "http://localhost:5000/data_by_column"  # Update with your API URL
            params = {'column_name': ['prof'], 'column_value': [professor]}

             # Send an empty JSON object in the request body
            data = {}

            # Set the headers to specify that you're sending JSON
            headers = {"Content-Type": "application/json"}

            response = requests.get(api_url, params=params, json=data, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if data:
                    # Format the response to display course sections
                    formatted_sections = []

                    for item in data:
                        section_info = "\n".join([f"{key}: {value}" for key, value in item.items()])
                        formatted_sections.append(section_info)

                    message = f"Here are all the sections for '{professor}':\n\n"
                    message += "\n".join(formatted_sections)
                    dispatcher.utter_message(message)
                else:
                    dispatcher.utter_message(f"Sorry, no sections found for '{professor}'.")
            else:
                dispatcher.utter_message("Sorry, I couldn't retrieve the course sections at the moment.")
        else:
            dispatcher.utter_message("I couldn't find the professor in your message.")

        return [SlotSet("professor", None)]


class GetCourseDescriptionAction(Action):
    def name(self):
        return "action_get_course_description"

    def run(self, dispatcher, tracker, domain):
        # Extract the course name from the user's message
        course_name = tracker.get_slot("course")

        # Make a GET request to your API to filter by 'crse'
        api_url = "http://localhost:5000/catalog_data_by_column"  # Update with your API URL
        params = {'column_name': 'title', 'column_value': course_name}

        # Send an empty JSON object in the request body
        data = {}

        # Set the headers to specify that you're sending JSON
        headers = {"Content-Type": "application/json"}

        response = requests.get(api_url, params=params, json=data, headers=headers)

        if response.status_code == 200:
            data = response.json()

            if data:
                # Format the response to display all columns for each matching course section
                formatted_sections = []
                for item in data:
                    section_info = "<br>".join([f"{key}: {value}" for key, value in item.items()])
                    formatted_sections.append(section_info)

                message = f"Here is the description for '{course_name}':<br><br>"
                message += "<br>".join(formatted_sections)
                dispatcher.utter_message(message)
            else:
                dispatcher.utter_message(f"Sorry, no classes found for '{course_name}'.")
        else:
            dispatcher.utter_message("Sorry, I couldn't retrieve the course description at the moment.")

        return [SlotSet("course", None)]



