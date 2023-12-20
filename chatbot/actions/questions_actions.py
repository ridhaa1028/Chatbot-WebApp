import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

class WhatCanChatbotDoAction(Action):
    def name(self):
        return "action_what_can_chatbot_do"

    def run(self, dispatcher, tracker, domain):
        message = (
            "This chatbot is designed to answer any questions you might have regarding classes at Rowan University and any upcoming events.<br>"
            "Our coolest feature is our schedule maker. It allows you to enter the course numbers you are interested in and it will make a schedule for you!<br>"
            "You can also ask the chatbot to give you a description of a course, prerequisites for a course, and particular sections of a course. Lastly, it can "
            "answer some questions pertaining to infrastructure, departments, and even upcoming events!<br>"
        )
        dispatcher.utter_message(message)

class GetCourseInformationAction(Action):
    def name(self):
        return "action_get_course_information"

    def run(self, dispatcher, tracker, domain):
        message = (
            "The user can receive course information by asking to see all available classes. Alternatively, the user can ask "
            "about a specific course to receive its description, the professors teaching it, and the course’s availability.<br>"
            "The user must use the correct format when asking for course information to ensure that the chatbot is providing "
            "accurate information. Examples of this format are shown below:<br>"
            "<ul>"
            "<li>List all classes</li>"
            "<li>I’m interested in Chemistry I</li>"
            "<li>Can you list the courses taught by John D Jambro?</li>"
            "</ul>"
        )
        dispatcher.utter_message(message)

class AnsweringQuestionsCorrectlyAction(Action):
    def name(self):
        return "action_answering_questions_correctly"

    def run(self, dispatcher, tracker, domain):
        message = (
            "It is necessary to use the correct format when asking questions to ensure the chatbot can accurately provide the "
            "user with answers. If trying to ask about something specific, the user should double-check that they are using "
            "the full name of the course, instructor, or infrastructure. Some examples of this proper format are listed "
            "below:<br>"
            "<ul>"
            "<li>Where is Lot A-1 located?</li>"
            "<li>Can you list the courses taught by Daniel Bogart?</li>"
            "<li>I want information on Principles of Finance</li>"
            "</ul>"
            "If the user is still facing issues receiving answers, they should double-check their spelling or try phrasing "
            "their question differently.<br>"
        )
        dispatcher.utter_message(message)


class CourseInformationTypesAction(Action):
    def name(self):
        return "action_course_information_types"

    def run(self, dispatcher, tracker, domain):
        message = (
            "This chatbot is able to list all courses, the instructors of specific courses, course descriptions, and "
            "availability of courses. In order to receive accurate information, it is important that the user asks questions "
            "using the proper format. Examples of this can be seen below:<br>"
            "<ul>"
            "<li>Can you list the courses taught by Nancy Tinkham?</li>"
            "<li>Tell me about the course Discrete Structures</li>"
            "<li>Give me a full description of Foundations of Computer Science</li>"
            "<li>Show me all classes</li>"
            "</ul>"
        )
        dispatcher.utter_message(message)

class InformAboutEventsAction(Action):
    def name(self):
        return "action_inform_about_events"

    def run(self, dispatcher, tracker, domain):
        message = (
            "Certainly! Here's how I can assist you with events:<br><br>"
            "1. **Events Right Now:**<br>"
            "   - Ask about events happening right now, like 'Is there an event going on right now?'<br>"
            "   - Questions like 'What events are happening at this time?' are also welcome.<br><br>"
            "2. **Events Tomorrow:**<br>"
            "   - Inquire about events taking place tomorrow, such as 'Is there an event going on tomorrow?'.<br>"
            "   - You can also ask 'What events are going on tomorrow?'.<br><br>"
            "3. **Events This Week:**<br>"
            "   - Ask about upcoming events for the week, like 'Is there an event upcoming this week?'.<br>"
            "   - Questions such as 'What events are going on in the coming week?' are accepted.<br><br>"
            "4. **Tell Me More About an Event:**<br>"
            "   - Request more details about a specific event using phrases like 'Tell me more about the event [name]'.<br>"
            "   - For example, 'Tell me more about the event Yoga Flow'.<br><br>"
            "5. **Specific Kind of Event:**<br>"
            "   - Ask if there are events related to a specific theme, e.g., 'Is there any upcoming event related to: [topic]'.<br>"
            "   - For instance, 'Is there any upcoming event related to: Basketball'.<br><br>"
            "Feel free to explore events, and let me know if you have any specific inquiries! 😊"
        )
        dispatcher.utter_message(message)