from typing import Dict, Text, List, Any
from rasa_sdk import Tracker
from rasa_sdk.events import EventType, SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action

class AskForSlotAction(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self) -> Text:
        return "action_ask_custom_fallback_form_affirm_deny"

    def __init__(self) -> None:
        import csv

        self.intent_mappings = {}
        with open('actions/action_files/intent_description_mapping.csv', #TODO find better place?
                  newline='',
                  encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                self.intent_mappings[row[0]] = row[1]

    

        self.bad_intent_mappings = {}
        with open('actions/action_files/bad_intent_description_mapping.csv', #TODO find better place?
                  newline='',
                  encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                self.bad_intent_mappings[row[0]] = row[1]
        
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
        
        # siit leiab intenti nime, mis jääb 60-80% vahemikku
        first_intent_names = [intent.get('name', '')
                              for intent in intent_ranking
                              if intent.get('name', '') not in ['out_of_scope', 'nlu_fallback']]

        # siin asendab intenti nime .csv failis oleva nime vastu, enne kui kliendile kuvab
        mapped_intents = [(name, self.intent_mappings.get(name, name))
                          for name in first_intent_names]

        # Siin on intentid, mida ei tohi kasutaja käest üle küsida
        bad_mapped_intents = [(name, self.bad_intent_mappings.get(name, name))
                          for name in first_intent_names]

        if mapped_intents != bad_mapped_intents:
            dispatcher.utter_message(response="utter_mille_kohta_küsimus_käis", intent=mapped_intents[0][1])
        else:
            return [FollowupAction(name = "direct_to_customer_support_form"), SlotSet("affirm_deny",None)]

        return []
    
