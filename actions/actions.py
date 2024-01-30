# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from urllib.parse import urljoin
import requests

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionPokedexEntry(Action):

    def name(self) -> Text:
        return 'action_pokedex_entry'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pokemon_name = tracker.get_slot('pokemon')
        url = urljoin('https://pokeapi.co/api/v2/pokemon-species/', str(pokemon_name.lower()))
        data = requests.get(url).json()
        flavor_text = data['flavor_text_entries'][0]['flavor_text']

        dispatcher.utter_message(text=flavor_text)

        return []


class ActionGetType(Action):

    def name(self) -> Text:
        return 'action_get_type'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pokemon_name = tracker.get_slot('pokemon')
        pokemon_name = str(pokemon_name.lower())
        url = urljoin('https://pokeapi.co/api/v2/pokemon/', pokemon_name)
        data = requests.get(url).json()
        pokemon_types = data['types']
        match len(pokemon_types):
            case 1:
                pokemon_type = str(data['types'][0]['type']['name'])
            case 2:
                type_1 = str(data['types'][0]['type']['name'])
                type_2 = str(data['types'][1]['type']['name'])
                pokemon_type = f"{type_1} and {type_2}"

        response = f"{pokemon_name.capitalize()} is a {pokemon_type} type pokemon."

        dispatcher.utter_message(text=response)

        return []
