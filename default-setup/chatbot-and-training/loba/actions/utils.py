import yaml


def get_kinnitamine_intent_examples(name):
    with open("data/nlu/common_kinnitamine_nlu.yml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

        for item in data["nlu"]:
            if "intent" in item and item["intent"] == name:
                items = [s.lower() for s in item["examples"].split("\n")]
                items = [s[2:] if s.startswith("- ") == True else s for s in items]
                return [s for s in items if s != ""]
        return []

def get_eitamine_intent_examples(name):
    with open("data/nlu/common_eitamine_nlu.yml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

        for item in data["nlu"]:
            if "intent" in item and item["intent"] == name:
                items = [s.lower() for s in item["examples"].split("\n")]
                items = [s[2:] if s.startswith("- ") == True else s for s in items]
                return [s for s in items if s != ""]
        return []

def get_next_action(intent_name):
    with open("data/rules.yml", "r", encoding="utf-8") as rules:
        rules_data = yaml.safe_load(rules)

        for r in rules_data["rules"]:
            for s in r["steps"]:
                for item in s:
                    if item == 'intent':
                        detected_intent = s['intent']
                        if detected_intent == intent_name:
                            return r["steps"][1]["action"]

def get_next_action2(intent_name):
    with open("data/stories.yml", "r", encoding="utf-8") as stories:
        stories_data = yaml.safe_load(stories)

        for r in stories_data["stories"]:
            for s in r["steps"]:
                for item in s:
                    if item == 'intent':
                        detected_intent = s['intent']
                        if detected_intent == intent_name:
                            return r["steps"][1]["action"]