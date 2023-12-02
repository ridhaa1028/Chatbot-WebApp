import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

class TestEventsAction(Action):
    def name(self):
        return "action_test_events"

    def run(self, dispatcher, tracker, domain):
        # Make a GET request to your API to filter by ....
        api_url = "http://localhost:5000/events_data_by_column"  # Update with your API URL
        params = {'column_name': ['id'], 'column_value': [3]}

        # Send an empty JSON object in the request body
        data = {}

        # Set the headers to specify that you're sending JSON
        headers = {"Content-Type": "application/json"}

        response = requests.get(api_url, params=params, json=data, headers=headers)

        if response.status_code == 200:
            data = response.json()

            if data:
                # Format the response to .......
                formatted_event = []
                for item in data:
                    event_info = "<br>".join([f"{key}: {value}" for key, value in item.items()])
                    formatted_event.append(event_info)

                message = f"Here is one of the events:<br><br>"
                message += "<br>".join(formatted_event)
                dispatcher.utter_message(message)
            else:
                dispatcher.utter_message(f"Sorry nothing found.")
        else:
            dispatcher.utter_message("Sorry, I couldn't retrieve an event at the moment.")