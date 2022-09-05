from typing import Dict, Text, List, Any
from rasa_sdk import Tracker
from rasa_sdk.events import EventType, SlotSet, FollowupAction, UserUttered
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action
from .utils import get_kinnitamine_intent_examples, get_eitamine_intent_examples, get_next_action, get_next_action2
from rasa_sdk import Action

class ActionDealWithAffirmationAnswer(Action):
    """Previously bot asked for an affirmation of the intent if NLU threshold is not met. Now we deal with it"""

    def name(self) -> Text:
        return "action_react_to_affirm_deny_in_custom_fallback_form"

    def __init__(self) -> None:
        self.affirm_list = get_kinnitamine_intent_examples("kinnitamine")
        # self.next_action = get_next_action(intent_name)

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List['Event']:
	
        affirmdeny_value = tracker.get_slot("affirm_deny")
        intent = tracker.latest_message['intent'].get('name')

        events = tracker.events_after_latest_restart()[-25:]
        events_with_utterances = list()
        for event in events:
            if "parse_data" in event.keys():
                events_with_utterances.append(event)
        
        if intent == "kinnitamine": # Kinnitus tuvastatud läbi intendi
            if events_with_utterances[-2]["parse_data"]["intent_ranking"][0]["name"] == "nlu_fallback":
                vastus = events_with_utterances[-2]["parse_data"]["intent_ranking"][1]["name"]
                if get_next_action(vastus) != None: #kontrollib rules ja kui sealt saab sisendi siis teeb...
                    response = get_next_action(vastus)
                    return [FollowupAction(name=response), SlotSet("affirm_deny",None)]
                else: # kui ei saanud rulesist sisendit, siis kontrollid stories sisendi ja teeb...
                    response = get_next_action2(vastus)
                    return [FollowupAction(name=response), SlotSet("affirm_deny",None)]
            
        else:
            response = "utter_"+events_with_utterances[-2]["parse_data"]["intent_ranking"][0]["name"]
            return[FollowupAction(name = "utter_ei_pakkunud_õigesti"), SlotSet("affirm_deny",None)]
        return [SlotSet("affirm_deny",None)]