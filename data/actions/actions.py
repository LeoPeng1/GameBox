# llThis files contains your custom actions which can be used to run
# custom Python code.

# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sqlite3






class Secure_Question(Action):
    def name(self) -> Text:
        return "action_display_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        username = tracker.get_slot("username")
        conn = sqlite3.connect('D:/Python/RASA/data/rasa.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT user_name, password, secure_question, answer 
                  FROM account_info 
                  WHERE user_name = ?''', (username,))
        results = cursor.fetchall()
        results = results[0]
        if results:
            dispatcher.utter_message(f"Your secure question is {results[2]}(shoud be like 'My answer is ')")
        else:
            dispatcher.utter_message("Sorry, your username is wrong.")

class Check_Subscription_Information(Action):
    def name(self) -> Text:
        return "action_check_subscription_information"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        password = tracker.get_slot("password")
        conn = sqlite3.connect('D:/Python/RASA/data/rasa.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT user_name, password, subscription_type, subscription_start_date, subscription_end_date
                  FROM account_info 
                  WHERE user_name = ?''', (username,))
        results = cursor.fetchall()
        results = results[0]
        if results:
            if password == results[1]:
                dispatcher.utter_message(f"Your subscription type is {results[2]} and it started on {results[3]} and will end on {results[4]}")
            else:
                dispatcher.utter_message("Sorry, your password is wrong.")
        else:
            dispatcher.utter_message("Sorry, your username is wrong.")



class Secure_Question(Action):
    def name(self) -> Text:
        return "action_reset_password"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        answer = tracker.get_slot("answer")
        new_password = tracker.get_slot("password")
        conn = sqlite3.connect('D:/Python/RASA/data/rasa.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT user_name, password, secure_question, answer 
                  FROM account_info 
                  WHERE user_name = ?''', (username,))
        results = cursor.fetchall()
        results = results[0]
        if answer == results[3]:
            cursor.execute('''UPDATE account_info SET password = ? WHERE user_name = ?''', (new_password, username))
            conn.commit()
            dispatcher.utter_message("Your password has been reset.")
        else:
            dispatcher.utter_message("Sorry, your answer is wrong.")

