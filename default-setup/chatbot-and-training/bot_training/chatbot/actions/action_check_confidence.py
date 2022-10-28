from typing import Dict, Text, List, Any
from rasa_sdk import Tracker
from rasa_sdk.events import EventType, SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action

class AskForSlotAction(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self) -> Text:
        return "action_check_confidence"

    def __init__(self) -> None:
        import csv

        self.LOWEST_CONFIDENCE = 0.6

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List['Event']:

        intent_ranking = tracker.latest_message.get('intent_ranking', [])
        if intent_ranking[0].get('name', '') == 'nlu_fallback':
            intent_ranking = [intent_ranking[1]]
        else:
            intent_ranking = [intent_ranking[0]]

        if intent_ranking[0].get("confidence", 0) < self.LOWEST_CONFIDENCE:
        	return [FollowupAction(name = "utter_ei_pakkunud_õigesti"), SlotSet("affirm_deny",None)]
        else: 
        	return [FollowupAction(name = "utter_not_confident"), SlotSet("affirm_deny",None)]

        return  []
