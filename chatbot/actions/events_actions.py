import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

from .models import EventsBase
from .models import CurrentEvents

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import re
from fuzzywuzzy import process  # Fuzzy string matching
from datetime import datetime, timedelta

engine = create_engine('sqlite:///actions/events.db')
EventsBase.metadata.bind = engine 
EventsBase.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class AskEventNowAction(Action):
    def name(self):
        return "action_ask_events_right_now"

    def run(self, dispatcher, tracker, domain):
        # Get the current time
        current_time = datetime.now()

        with Session() as session:
            current_events = session.query(CurrentEvents).filter(
                CurrentEvents.start <= current_time,
                CurrentEvents.end >= current_time
            ).all()

        
        if current_events:
            message = "<br>Here are the events happening right now:<br>"
            for event in current_events:
                message += f'<a href="{event.url}">{event.name}</a><br>'
            message += "<br>Feel free to ask a follow up question about a specific event!"
        else:
            message = "<br>There are no events happening at this moment.<br>"

        
        dispatcher.utter_message(message)

        

class AskEventTomorrowAction(Action):
    def name(self):
        return "action_ask_events_tomorrow"

    def run(self, dispatcher, tracker, domain):
        # Calculate tomorrow's date
        tomorrow = datetime.now().date() + timedelta(days=1)
        start_of_tomorrow = datetime.combine(tomorrow, datetime.min.time())
        end_of_tomorrow = datetime.combine(tomorrow, datetime.max.time())

        with Session() as session:
            # Query for events happening any time tomorrow
            events_tomorrow = session.query(CurrentEvents).filter(
                CurrentEvents.start >= start_of_tomorrow,
                CurrentEvents.end <= end_of_tomorrow
            ).all()

        
        if events_tomorrow:
            message = f"<br>Here are the events happening tomorrow {tomorrow.strftime('%A')} {tomorrow}:<br>"
            for event in events_tomorrow:
                message += f'<a href="{event.url}">{event.name}</a><br>'
            message += "<br>Feel free to ask a follow up question about a specific event!"
        else:
            message = "<br>There are no events happening tomorrow.<br>"

        
        dispatcher.utter_message(message)

        

class AskEventWeekAction(Action):
    def name(self):
        return "action_ask_events_week"

    def run(self, dispatcher, tracker, domain):
        # Calculate the dates for this week
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        current_time = today

        with Session() as session:
            
            past_events_this_week = session.query(CurrentEvents).filter(
                CurrentEvents.start >= start_of_week,
                CurrentEvents.start <= end_of_week,
                CurrentEvents.end < current_time
            ).all()

            # Query for upcoming events this week
            upcoming_events_this_week = session.query(CurrentEvents).filter(
                CurrentEvents.start >= start_of_week,
                CurrentEvents.start <= end_of_week,
                CurrentEvents.start > current_time
            ).all()

        first_message = f"<br>Here are the events happening this week {start_of_week.date()} to {end_of_week.date()}:<br>"

        
        if upcoming_events_this_week:
            upcoming_message = "<br>Upcoming events this week:<br><br>"
            for event in upcoming_events_this_week:
                upcoming_message += f'<a href="{event.url}">{event.name}</a><br>'
        else:
            upcoming_message = "<br>There are no upcoming events this week.<br>"

        
        if past_events_this_week:
            past_message = "<br>Past events this week:<br><br>"
            for event in past_events_this_week:
                past_message += f'<a href="{event.url}">{event.name}</a><br>'
        else:
            past_message = "<br>There were no past events this week.<br>"
        
        conclude_message = "<br>Feel free to ask a follow up question about a specific event!"

        
        dispatcher.utter_message(first_message + upcoming_message + past_message + conclude_message)

        
            
            
class TellMeMoreEventAction(Action):
    def name(self):
        return "action_tell_me_more_about_event"

    def run(self, dispatcher, tracker, domain):
        # must be in the form "...  the event [name]"
        user_message = tracker.latest_message.get('text').lower()
        match = re.search(".* the event (.+)", user_message)
        if match:
            queried_name = match.group(1)
            # Open database session
            with Session() as session:
                # Query for all location names
                names = session.query(CurrentEvents.name).all()  
                names = [n[0] for n in names]  # flatten

                # Find the closest match
                closest_match = process.extractOne(queried_name, names)[0]

                # Query for the matched location's details
                event = session.query(CurrentEvents).filter_by(name=closest_match).first()

                if event:
                    # Send the location details to the user
                    message = f"Here is information about the event <a href='{event.url}'>{event.name}</a><br>"
                    message += f"<br>Description: {event.description}<br>"
                    message += f"<br>Hosted by: {event.host}<br>"
                    message += f"<br>This event will be located at: {event.location}<br>"
                    dispatcher.utter_message(message)
                else:
                    # Handle no match found
                    dispatcher.utter_message("Sorry, I couldn't find that location.")
        else:
            dispatcher.utter_message("Please ask in the format: 'Tell me more about the event [name]'")










# List of common stop words to be removed
stop_words = {'and', 'or', 'but', 'the', 'is', 'at', 'which', 'on', 'for', 'by', 'from', 'up', 'to', 'with', 'a', 'an', 'in', 'of', 'it'}

# Function to clean and split text into words, removing punctuation and stop words
def clean_and_split(text):
    words = set(re.sub(r'[^\w\s]', '', text).lower().split())
    return words - stop_words

class AskSpecificKindEvent(Action):
    def name(self):
        return "action_ask_specific_kind_of_event"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get('text')
        match = re.search(".* related to: (.+)", user_message)
        if match:
            queried_keywords = clean_and_split(match.group(1))
            matched_events = []

            with Session() as session:
                events = session.query(CurrentEvents).all()

                for event in events:
                    event_keywords = clean_and_split(event.description + ' ' + event.name)
                    # Check if all queried keywords are in the event keywords
                    if queried_keywords.issubset(event_keywords):
                        matched_events.append(event)

                if matched_events:
                    message = "<br>Here are the events related to your query:<br>"
                    for event in matched_events:
                        message += f"<a href='{event.url}'>{event.name}</a><br>"
                        formatted_start_time = event.start.strftime('%Y-%m-%d %I:%M %p')
                        message += f"Starts {formatted_start_time}<br>"
                        message += f"Description: {event.description}<br><br>"
                    dispatcher.utter_message(message)
                else:
                    dispatcher.utter_message("Sorry, I couldn't find any related event.")
        else:
            dispatcher.utter_message("Please ask in the format: 'Is there any upcoming event related to: [various descriptions or names]'")

        

       


        
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