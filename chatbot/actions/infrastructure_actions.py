import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

""" class TestInfrastructureAction(Action):
    def name(self):
        return "action_test_infrastructure"

    def run(self, dispatcher, tracker, domain):
        # Make a GET request to your API to filter by ....
        api_url = "http://localhost:5000/infrastructure_data_by_column"  # Update with your API URL
        params = {'column_name': ['id'], 'column_value': [5]}

        # Send an empty JSON object in the request body
        data = {}

        # Set the headers to specify that you're sending JSON
        headers = {"Content-Type": "application/json"}

        response = requests.get(api_url, params=params, json=data, headers=headers)

        if response.status_code == 200:
            data = response.json()

            if data:
                # Format the response to ...
                selected_fields = ['name', 'categories', 'description'] # can use this list for both enforcing order and limiting columns

                # Can use this to rename the fields better
                field_mapping = {
                    'name': 'NAME',
                    'categories': 'CATEGORIES',
                    'description': 'DESCRIPTION'
                }


                formatted_location = []
                for item in data:
                    #event_info = "<br>".join([f"{key}: {value}" for key, value in item.items()])
                    event_info = "<br>".join([f"{field_mapping[key]}: {item[key]}" for key in selected_fields if key in item])
                    formatted_location.append(event_info)

                message = f"Here is one of the locations:<br><br>"
                message += "<br>".join(formatted_location)
                dispatcher.utter_message(message)
            else:
                dispatcher.utter_message(f"Sorry nothing found.")
        else:
            dispatcher.utter_message("Sorry, I couldn't retrieve a location at the moment.")  """


class TestInfrastructureAction(Action):
    def name(self):
        return "action_test_infrastructure"

    def run(self, dispatcher, tracker, domain):
        # Make a GET request to your API to filter by ....
        api_url = "http://localhost:5000/infrastructure_data_by_column"  # Update with your API URL
        params = {'column_name': ['id'], 'column_value': [5]}

        # Send an empty JSON object in the request body
        data = {}

        # Set the headers to specify that you're sending JSON
        headers = {"Content-Type": "application/json"}

        response = requests.get(api_url, params=params, json=data, headers=headers)

        if response.status_code == 200:
            data = response.json()

            if data:
                # Format the response to ...
                selected_fields = ['name', 'categories', 'description'] # can use this list for both enforcing order and limiting columns

                # Can use this to rename the fields better
                field_mapping = {
                    'name': 'NAME',
                    'categories': 'CATEGORIES',
                    'description': 'DESCRIPTION'
                }
                data_dict = dict()
                for item in data:
                    for key in item:
                        data_dict[key] = item[key]
                print(data)
                message = f"Here is one of the locations:<br><br>"
                message += (f"The name of this location is {data_dict['name']}")
                dispatcher.utter_message(message)
            else:
                dispatcher.utter_message(f"Sorry nothing found.")
        else:
            dispatcher.utter_message("Sorry, I couldn't retrieve a location at the moment.") 