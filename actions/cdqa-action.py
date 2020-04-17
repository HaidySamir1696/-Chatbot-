# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


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
#from rasa_sdk import Action
from rasa_sdk.events import UserUtteranceReverted
from typing import Text, List, Dict, Any
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#import init_cdqa_pipeline
import  init_cdqa
from init_cdqa import CDQA_PIPELINE , process_query, init_cdqa_pipeline

if CDQA_PIPELINE is None:
    csv_file = "./data_pdf/csv/converted_pdfs.csv"
    model_file = "./models/cdqa/bert_qa.joblib"
    CDQA_PIPELINE = init_cdqa_pipeline(csv_file,model_file)

#for test
#query = "please send me the table of Word Address 1 ID Register Bit Assignments?"
#x= init_cdqa.process_query(query, CDQA_PIPELINE)

class ActionFaq(Action):

    def name(self) -> Text:
        return "action_faq_qa_model"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List:
        answer = init_cdqa.process_query(tracker.latest_message.get('text'), CDQA_PIPELINE)
        dispatcher.utter_message(answer)

            #deh hatl8y elcontext 3lasha dah simple bot bs la2 ana msh 3aiza kda
        return[UserUtteranceReverted()]
