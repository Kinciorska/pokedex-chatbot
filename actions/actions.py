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
