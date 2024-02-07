# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from .utils import pokemon_type_effectiveness

from typing import Any, Text, Dict, List
from urllib.parse import urljoin
import requests

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionPokedexEntry(Action):

    def name(self) -> Text:
        return 'action_pokedex_entry'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pokemon_name = tracker.get_slot('pokemon')
        try:
            url = urljoin('https://pokeapi.co/api/v2/pokemon-species/', str(pokemon_name.lower()))
            data = requests.get(url).json()
            flavor_text = data['flavor_text_entries'][0]['flavor_text']

            dispatcher.utter_message(text=flavor_text)

        except requests.exceptions.JSONDecodeError:
            response = "I didn't understand which pokemon are you talking about."

            dispatcher.utter_message(text=response)

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
        first_type = str(data['types'][0]['type']['name'])
        match len(pokemon_types):
            case 1:
                pokemon_type = str(data['types'][0]['type']['name'])
            case 2:
                type_1 = str(data['types'][0]['type']['name'])
                type_2 = str(data['types'][1]['type']['name'])
                pokemon_type = f"{type_1} and {type_2}"

        response = f"{pokemon_name.capitalize()} is a {pokemon_type} type pokemon."

        dispatcher.utter_message(text=response)

        return [SlotSet('pokemon_type', first_type)]


class ActionGetTypeVulnerability(Action):

    def name(self) -> Text:
        return 'action_get_type_vulnerability'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        type_name = tracker.get_slot('pokemon_type')
        if type_name is None:
            response = ("Sorry, I didn't understand what type are you asking about. "
                        "Can you repeat the question please? ")
            dispatcher.utter_message(text=response)
        else:
            try:
                type_name = str(type_name.lower())
                type_vulnerability = pokemon_type_effectiveness[type_name]['vulnerable_to']
                response = f"{type_name.capitalize()} type pokemons are vulnerable to {type_vulnerability} attacks."

                dispatcher.utter_message(text=response)

            except KeyError:
                response = ("Sorry, I didn't understand what type are you asking about. "
                            "Can you repeat the question please? ")

                dispatcher.utter_message(text=response)

        return []


class ActionGetTypeStrength(Action):

    def name(self) -> Text:
        return 'action_get_type_strength'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        type_name = tracker.get_slot('pokemon_type')
        if type_name is None:
            response = ("Sorry, I didn't understand what type are you asking about. "
                        "Can you repeat the question please? ")

            dispatcher.utter_message(text=response)

        else:
            try:
                type_name = str(type_name.lower())
                type_vulnerability = pokemon_type_effectiveness[type_name]['strong_against']
                response = f"{type_name.capitalize()} type attacks are strong against {type_vulnerability} pokemons."

                dispatcher.utter_message(text=response)

            except KeyError:
                response = ("Sorry, I didn't understand what type are you asking about. "
                            "Can you repeat the question please? ")

                dispatcher.utter_message(text=response)

        return []


class ActionGetImage(Action):

    def name(self) -> Text:
        return 'action_get_image'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pokemon_name = tracker.get_slot('pokemon')
        pokemon_name = str(pokemon_name.lower())
        try:
            url = urljoin('https://pokeapi.co/api/v2/pokemon/', pokemon_name)
            data = requests.get(url).json()
            pokemon_image = data['sprites']['other']['official-artwork']['front_default']

            dispatcher.utter_message(image=pokemon_image)

        except requests.exceptions.JSONDecodeError:
            response = " Can you check the spelling please?"

            dispatcher.utter_message(text=response)

        return []


class ActionGetShinyImage(Action):

    def name(self) -> Text:
        return 'action_get_shiny_image'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pokemon_name = tracker.get_slot('pokemon')
        if pokemon_name is None:
            response = ("Sorry, I didn't understand what pokemon are you asking about. "
                        "Can you repeat the question please? ")

            dispatcher.utter_message(text=response)

            return [SlotSet('pokemon', None)]

        else:
            try:
                pokemon_name = str(pokemon_name.lower())
                url = urljoin('https://pokeapi.co/api/v2/pokemon/', pokemon_name)
                data = requests.get(url).json()
                pokemon_image = data['sprites']['other']['official-artwork']['front_shiny']
                response = "Yes, here it is:"

                dispatcher.utter_message(text=response, image=pokemon_image)

            except requests.exceptions.JSONDecodeError:
                response = ("Sorry, I didn't understand which pokemon are you talking about. "
                            "Can you check the spelling please?")

                dispatcher.utter_message(text=response)

            return []
