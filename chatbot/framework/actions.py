from rasa_sdk.events import UserUtteranceReverted
from typing import Text, List, Dict, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from qa_system import init_QA_PIPELINE, process_query

# Initialize QA Pipeline on action bootsrtaping
init_QA_PIPELINE()

class ActionFaq(Action):
    """
        Question and Answer action used by RASA Framework to retrieve response on document related questions.
    """

    def name(self) -> Text:
        return "action_faq_qa_model"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List:
        # TODO: Retrieve Document name extracted by RASA
        DOC_FILE = None
        answer = process_query(query=tracker.latest_message.get('text'), document=DOC_FILE)
        dispatcher.utter_message(answer)

        return[UserUtteranceReverted()]
