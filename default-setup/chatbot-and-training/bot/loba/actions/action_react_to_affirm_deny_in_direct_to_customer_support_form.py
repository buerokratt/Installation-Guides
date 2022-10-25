from typing import Dict, Text, List, Any
from rasa_sdk import Tracker
from rasa_sdk.events import EventType, SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action
from .utils import get_kinnitamine_intent_examples, get_eitamine_intent_examples, get_next_action, get_next_action2

class ActionDealWithAffirmationAnswer(Action):
    """Previously bot asked for an affirmation of the intent if NLU threshold is not met. Now we deal with it"""

    def name(self) -> Text:
        return "action_react_to_affirm_deny_in_direct_to_customer_support_form"

    def __init__(self) -> None:
        self.affirm_list = get_kinnitamine_intent_examples("common_kinnitamine")
        self.deny_list = get_eitamine_intent_examples("common_eitamine")
        
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List['Event']:
	
        affirmdeny_value = tracker.get_slot("affirm_deny")
        intent = tracker.latest_message['intent'].get('name')

        if intent == "common_kinnitamine": #Siin suunatakse klienditeenindajale intenti kaudu
            dispatcher.utter_message(response="utter_common_klienditeenindajale_suunamine")
            return [SlotSet("affirm_deny",None)]
        elif affirmdeny_value.lower() in self.affirm_list: #Siin suunatakse klienditeenindajale listi kaudu
            dispatcher.utter_message(response="utter_common_klienditeenindajale_suunamine")
            return [SlotSet("affirm_deny",None)]
        elif intent == "common_eitamine": # Bot ütleb selge, head päeva intent eituse kaudu
            dispatcher.utter_message(response="utter_common_ei_suuna_klienditeenindajale")
            return [SlotSet("affirm_deny",None)]
        elif affirmdeny_value.lower() in self.deny_list: # Bot ütleb selge, head päeva eituse listi kaudu
            dispatcher.utter_message(response="utter_common_ei_suuna_klienditeenindajale")
            return [SlotSet("affirm_deny",None)]
        elif intent == "nlu_fallback": # Fallbacki puhul küsib korra uuesti, kas tahtis klienditeendindajat
            dispatcher.utter_message(response="utter_fallback_kontroll")
            return [SlotSet("affirm_deny","kontroll")]
            # FollowupAction(name = "utter_fallback_kontroll")
        else:
            events = tracker.events_after_latest_restart()[-25:]
            events_with_utterances = list()
            for event in events:
                if "parse_data" in event.keys():
                    events_with_utterances.append(event)    
            vastus = events_with_utterances[-1]["parse_data"]["intent_ranking"][0]["name"]
            if get_next_action(vastus) != None: #kontrollib rules ja kui sealt saab sisendi siis teeb...
                response = get_next_action(vastus)
                return [FollowupAction(name=response), SlotSet("affirm_deny",None)]
            else: # kui ei saanud rulesist sisendit, siis kontrollid stories sisendi ja teeb...
                response = get_next_action2(vastus)
                return [FollowupAction(name=response), SlotSet("affirm_deny",None)]
        return [SlotSet("affirm_deny",None)]
