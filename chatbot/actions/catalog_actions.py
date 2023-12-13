import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

class GetCourseDescriptionAction(Action):
    def name(self):
        return "action_get_course_description"

    def run(self, dispatcher, tracker, domain):
        # Extract the course name from the user's message
        course_name = tracker.get_slot("title")

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