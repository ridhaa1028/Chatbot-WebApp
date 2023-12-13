import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

from .models import InfrastructureBase
from .models import Infrastructure

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import re
from fuzzywuzzy import process  # Fuzzy string matching

engine = create_engine('sqlite:///actions/infrastructure.db')
InfrastructureBase.metadata.bind = engine 
InfrastructureBase.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class TellMeAboutInfraAction(Action):
    def name(self):
        return "action_what_tell_me_about_infrastructure"
    def run(self, dispatcher, tracker, domain):
        s1 = "<br>Rowan University has many different buildings and landmarks in the Glassboro campus.<br>"
        s2 = "This includes the following categories:<br>"
        Categories = ['Academic Buildings', 'Parking', 'Residence Halls & Apartments', 'Administrative & Support', 
                      'Athletics', 'Shuttle Stop Locations', 'Academic Departments', 'Outdoor Spaces', 'All Gender Restrooms']
        s3 = ""
        for c in Categories:
            s3 += c
            s3 += '<br>'
        s4 = "Feel free to ask more about a specific category!"
        message = ""
        for s in [s1, s2, s3, s4]:
            message += s + '<br>'
        dispatcher.utter_message(message)

class AskForLocationAction(Action):
    def name(self):
        return "action_ask_for_location"
    def run(self, dispatcher, tracker, domain):
        # Must be in the form: "Where is [location_name] located"
        user_message = tracker.latest_message.get('text').lower()
        match = re.search("where is (.+) located", user_message)
        if match:
            queried_name = match.group(1)

            # Open database session
            with Session() as session:
                # Query for all location names
                names = session.query(Infrastructure.name).all()  
                names = [n[0] for n in names]  # flatten tuples

                # Find the closest match
                closest_match = process.extractOne(queried_name, names)[0]

                # Query for the matched location's details
                location = session.query(Infrastructure).filter_by(name=closest_match).first()

                if location:
                    # Send the location details to the user
                    lat = location.latitude
                    long = location.longitude
                    maps_link = f"https://www.google.com/maps/?q={lat},{long}"
                    dispatcher.utter_message(f"Here is the location information for {location.name}: <a href='{maps_link}' target='_blank'>{maps_link}</a>")
                else:
                    # Handle no match found
                    dispatcher.utter_message("Sorry, I couldn't find that location.")

        else:
            # Handle invalid query format
            dispatcher.utter_message("Please ask in the format: 'Where is [name] located?'")
        

class TellMeMoreLocationAction(Action):
    def name(self):
        return "action_tell_me_more_about_location"
    def run(self, dispatcher, tracker, domain):
        # Must be in the form: ".... about [location_name]"
        user_message = tracker.latest_message.get('text').lower()
        match = re.search(".* about the place (.+)", user_message)
        if match:
            matched_text = match.group(1)  # Extracts the matched group
            with Session() as session:
                names = session.query(Infrastructure.name).all()  
                names = [n[0] for n in names]  # flatten tuples

                # Find the closest match
                closest_match = process.extractOne(matched_text, names)[0]

                # Query for the matched location's details
                location = session.query(Infrastructure).filter_by(name=closest_match).first()

                if location:
                    # Send the location details to the user
                    description = location.description
                    dispatcher.utter_message(f"Here is a description of {location.name}:<br><br>{description}")
                else:
                    # Handle no match found
                    dispatcher.utter_message("Sorry, I couldn't find that location.")
        else:
            dispatcher.utter_message("Please ask in the format: Tell me more about the place [name]")
        
    
class AskLandmarkAction(Action):
    def name(self):
        return "action_ask_for_landmarks"
    def run(self, dispatcher, tracker, domain):
        with Session() as session:
            HollyBush = session.query(Infrastructure.name).filter(Infrastructure.name == 'Hollybush Mansion').all()
            HollyBush = [h[0] for h in HollyBush]
            Outdoors = session.query(Infrastructure.name).filter(Infrastructure.categories == 'Outdoor Spaces').all()
            Outdoors = [O[0] for O in Outdoors]
            Landmarks = HollyBush + Outdoors

        s1 = "<br>Rowan University has a few landmarks Glassboro campus.<br>"
        s2 = "Here are some of the Landmarks:<br>"
        s3 = ""
        for l in Landmarks:
           s3 += l 
           s3 += '<br>'
        s4 = "Feel free to ask more about a specific landmark such as where it's located for directions!"
        message = ""
        for s in [s1, s2, s3, s4]:
            message += s + '<br>'
        dispatcher.utter_message(message)
        

class AskDepartmentAction(Action):
    def name(self):
        return "action_ask_for_departments"
    def run(self, dispatcher, tracker, domain):
        with Session() as session:
            Departments = session.query(Infrastructure.name, Infrastructure.description).filter(Infrastructure.categories == 'Academic Departments').all()

        s1 = "<br>Rowan University has many different departments in the Glassboro campus.<br>"
        s2 = "Here are all of the Departments:<br>"
        s3 = ""
        for dept, desc in Departments:
            match = re.search(r"located in (.+)", desc)
            location = desc.split("located")[1]
            s3 += dept + " - Located " + location
            s3 += '<br><br>'
        s4 = "Feel free to ask more about a specific department such as where it's exactly located for exact directions!"
        message = ""
        for s in [s1, s2, s3, s4]:
            message += s + '<br>'
        dispatcher.utter_message(message)
        

class AskBathroomsAction(Action):
    def name(self):
        return "action_ask_for_bathrooms"
    def run(self, dispatcher, tracker, domain):
        with Session() as session:
            Bathrooms = session.query(Infrastructure.name).filter(Infrastructure.categories == 'All Gender Restrooms').all()
            Bathrooms = [d[0] for d in Bathrooms]

        s1 = "<br>Rowan University has many All Gender Restrooms on the Glassboro campus.<br>"
        s2 = "Here are all of the Bathrooms:<br>"
        s3 = ""
        for d in Bathrooms:
            s3 += d
            s3 += '<br>'
        s4 = "Feel free to ask more about a specific bathroom such as where it's located for directions!"
        message = ""
        for s in [s1, s2, s3, s4]:
            message += s + '<br>'
        dispatcher.utter_message(message)
    

class AskParkingAction(Action):
    def name(self):
        return "action_ask_for_parking"
    def run(self, dispatcher, tracker, domain):
        with Session() as session:
            parking_categories = ['Commuter Parking', 'Employee Parking', 'Resident Parking', 'Visitor Parking']
            Parkings = session.query(Infrastructure.name, Infrastructure.categories).filter(Infrastructure.categories.in_(parking_categories)).all()

        s1 = "<br>Rowan University has many parking spaces on the Glassboro campus.They fall into 4 categories:<br>"
        s1 += "Commuter Parking, Employee Parking, Resident Parking and Visitor Parking<br>"
        s2 = "Here are all of the Parking spaces along with it's category:<br>"
        s3 = ""
        for name, category in Parkings:
            s3 += name + " - " + category
            s3 += '<br>'
        s4 = "Feel free to ask more about a specific spot such as where it's located for directions!"
        message = ""
        for s in [s1, s2, s3, s4]:
            message += s + '<br>'
        dispatcher.utter_message(message)
        

class AskResidenceAction(Action):
    def name(self):
        return "action_ask_for_residence"
    def run(self, dispatcher, tracker, domain):
        with Session() as session:
            Houses = session.query(Infrastructure.name).filter(Infrastructure.categories == 'Residence Halls & Apartments').all()
            Houses = [d[0] for d in Houses]

        s1 = "<br>Rowan University has many places for housing around the Glassboro campus.<br>"
        s2 = "Here are all of the Housing Areas:<br>"
        s3 = ""
        for h in Houses:
            s3 += h
            s3 += '<br>'
        s4 = "Feel free to ask more about a specific Housing Area such as where it's located for directions!"
        message = ""
        for s in [s1, s2, s3, s4]:
            message += s + '<br>'
        dispatcher.utter_message(message)
        

class AskAcademicsAction(Action):
    def name(self):
        return "action_ask_for_academics"
    def run(self, dispatcher, tracker, domain):
        with Session() as session:
            AcademicBuildings = session.query(Infrastructure.name).filter(Infrastructure.categories == 'Academic Buildings').all()
            AcademicBuildings = [d[0] for d in AcademicBuildings]

        s1 = "<br>Rowan University has many Academic Buildings in the Glassboro campus.<br>"
        s2 = "Here are all of the Academic Buildings:<br>"
        s3 = ""
        for b in AcademicBuildings:
            s3 += b
            s3 += '<br>'
        s4 = "Feel free to ask more about a specific building such as where it's located for directions!"
        message = ""
        for s in [s1, s2, s3, s4]:
            message += s + '<br>'
        dispatcher.utter_message(message)
        

class AskAdminAction(Action):
    def name(self):
        return "action_ask_for_admin"
    def run(self, dispatcher, tracker, domain):
        with Session() as session:
            AdminBuildings = session.query(Infrastructure.name).filter(Infrastructure.categories == 'Administrative & Support').all()
            AdminBuildings = [d[0] for d in AdminBuildings]

        s1 = "<br>Rowan University has many places for administration or support are the Glassboro campus.<br>"
        s2 = "Here are all of the Administrative or Support Buildings:<br>"
        s3 = ""
        for b in AdminBuildings:
            s3 += b 
            s3 += '<br>'
        s4 = "Feel free to ask more about a specific building such as where it's located for directions!"
        message = ""
        for s in [s1, s2, s3, s4]:
            message += s + '<br>'
        dispatcher.utter_message(message)
        # f'<a href="{event.url}">{event.name}</a><br>'


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