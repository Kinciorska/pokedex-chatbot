# Pokedex Chatbot

## Overview

Pokédex is a chatbot built using the Rasa Open Source framework, designed to emulate the functionality of a Pokédex from the popular Pokémon series. The chatbot provides an interactive and dynamic user experience by allowing users to input questions related to Pokémon and receive detailed information about them.

## Features

 - **Pokédex entry**: The Pokédex will provide the entry of the desired Pokémon.

 - **Type effectiveness**: The user can inquire about the strengths and weaknesses of different Pokémon types.

## Getting Started

To get started with the Pokedex, follow these steps:

1. Clone the repository
    ```
   git clone https://github.com/Kinciorska/pokedex-chatbot.git
   
2. Change into the correct directory
   ```
   cd pokedex-chatbot
   ```

3. Install the necessary dependencies:
    ``` 
   pip install -r requirements.txt
    ```
4. Train the chatbot: 
    ```
   rasa train
   ``` 
5. Run the chatbot in one commandline:
   ```
   rasa shell
   ```
6. Run action server in a second commandline:
   ```
   rasa run actions
   ```

## License

This project is licensed under the [GNU General Public License v3.0.](LICENSE)
