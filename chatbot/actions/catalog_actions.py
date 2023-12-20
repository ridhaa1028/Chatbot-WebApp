import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

class GetCourseDescriptionAction(Action):
    def name(self):
        return "action_get_course_description"

    def run(self, dispatcher, tracker, domain):
        # Extract the course name from the user's message
        course_name = tracker.get_slot("title")
        
        lowercase_course_name = course_name.lower()
        if lowercase_course_name == "iot" or lowercase_course_name == "cloud computing":
            course_name = "CLOUD COMPUT & INTERNET THINGS"
        elif lowercase_course_name == "dsa":
            course_name = "DATA STRUCT/ALGORITHM"
        elif lowercase_course_name == "oopda" or lowercase_course_name == "data abstraction":
            course_name = "OBJ-ORIENT PRGRM/DATA ABSTR"
        elif lowercase_course_name == "lab techniques" or lowercase_course_name == "lab tech" or lowercase_course_name == "lcomputer lab techniques":
            course_name = "COMPUTER LAB TECHNQ"
        elif lowercase_course_name == "os":
            course_name = "OPERATING SYSTEMS"

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

        return [SlotSet("title", None)]

class GetJustCourseDescriptionAction(Action):
    def name(self):
        return "action_get_just_course_description"

    def run(self, dispatcher, tracker, domain):
        # Extract the course name from the user's message
        course_name = tracker.get_slot("title")

        lowercase_course_name = course_name.lower()
        if lowercase_course_name == "iot" or lowercase_course_name == "cloud computing":
            course_name = "CLOUD COMPUT & INTERNET THINGS"
        elif lowercase_course_name == "dsa":
            course_name = "DATA STRUCT/ALGORITHM"
        elif lowercase_course_name == "oopda" or lowercase_course_name == "data abstraction":
            course_name = "OBJ-ORIENT PRGRM/DATA ABSTR"
        elif lowercase_course_name == "lab techniques" or lowercase_course_name == "lab tech" or lowercase_course_name == "lcomputer lab techniques":
            course_name = "COMPUTER LAB TECHNQ"
        elif lowercase_course_name == "os":
            course_name = "OPERATING SYSTEMS"

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
                # Extract only the "description" column from the API response
                descriptions = [item.get("description") for item in data]

                if descriptions:
                    # Format the response to display the descriptions
                    message = f"Here is the description for '{course_name}':<br><br>"
                    message += "<br>".join(descriptions)
                    dispatcher.utter_message(message)
                else:
                    dispatcher.utter_message(f"Sorry, no description found for '{course_name}'.")
            else:
                dispatcher.utter_message(f"Sorry, no classes found for '{course_name}'.")
        else:
            dispatcher.utter_message("Sorry, I couldn't retrieve the course description at the moment.")

        return [SlotSet("title", None)]

class GetCoursePrerequisitesAction(Action):
    def name(self):
        return "action_get_course_prerequisites"

    def run(self, dispatcher, tracker, domain):
        # Extract the course name from the user's message
        course_name = tracker.get_slot("title")

        lowercase_course_name = course_name.lower()
        if lowercase_course_name == "iot" or lowercase_course_name == "cloud computing":
            course_name = "CLOUD COMPUT & INTERNET THINGS"
        elif lowercase_course_name == "dsa":
            course_name = "DATA STRUCT/ALGORITHM"
        elif lowercase_course_name == "oopda" or lowercase_course_name == "data abstraction":
            course_name = "OBJ-ORIENT PRGRM/DATA ABSTR"
        elif lowercase_course_name == "lab techniques" or lowercase_course_name == "lab tech" or lowercase_course_name == "lcomputer lab techniques":
            course_name = "COMPUTER LAB TECHNQ"
        elif lowercase_course_name == "os":
            course_name = "OPERATING SYSTEMS"

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
                # Extract only the "prereq" column from the API response
                prerequisites = [item.get("prereq") for item in data]

                if prerequisites:
                    # Format the response to display the prerequisites
                    message = f"Here are the prerequisites for '{course_name}':<br><br>"
                    message += "<br>".join(prerequisites)
                    dispatcher.utter_message(message)
                else:
                    dispatcher.utter_message(f"Sorry, no prerequisites found for '{course_name}'.")
            else:
                dispatcher.utter_message(f"Sorry, no classes found for '{course_name}'.")
        else:
            dispatcher.utter_message("Sorry, I couldn't retrieve the course prerequisites at the moment.")

        return [SlotSet("title", None)]

