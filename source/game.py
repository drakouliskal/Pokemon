from typing import Tuple
import random

from player import Player
from pokemon import Pokemon



class Game:
    POKEMON_LIST: Tuple[Pokemon] = (
        Pokemon("Pikachu", "Electric", "When several of these Pokémon gather, their electricity could build and cause lightning storms.", 100, [
            {'name': "Thunder Shock", 'type': "Electric", 'damage': 20, 'hit_chance': 0.80},
            {'name': "Quick Attack", 'type': "Normal", 'damage': 10, 'hit_chance': 0.95}
        ]),
        Pokemon("Charmander", "Fire", "The flame at the tip of its tail makes a sound as it burns. You can only hear it in quiet places.", 90, [
            {'name': "Ember", 'type': "Fire", 'damage': 25, 'hit_chance': 0.85},
            {'name': "Scratch", 'type': "Normal", 'damage': 15, 'hit_chance': 0.80}
        ]),
        Pokemon("Bulbasaur", "Grass", "A strange seed was planted on its back at birth. The plant sprouts and grows with this Pokémon.", 110, [
            {'name': "Vine Whip", 'type': "Grass", 'damage': 20, 'hit_chance': 0.85},
            {'name': "Tackle", 'type': "Normal", 'damage': 10, 'hit_chance': 0.90}
        ]),
        Pokemon("Squirtle", "Water", "Shoots water at prey while in the water. Withdraws into its shell when in danger.", 95, [
            {'name': "Water Gun", 'type': "Water", 'damage': 20, 'hit_chance': 0.85},
            {'name': "Tackle", 'type': "Normal", 'damage': 10, 'hit_chance': 0.90}
        ]),
        Pokemon("Weedle", "Bug", "Often found in forests, eating leaves. It has a sharp venomous stinger on its head.", 85, [
            {'name': "Poison Sting", 'type': "Bug", 'damage': 15, 'hit_chance': 1.00},
            {'name': "Fury Attack", 'type': "Normal", 'damage': 20, 'hit_chance': 0.85}
        ]),
        Pokemon("Onix", "Rock", "As it grows, the stone portions of its body harden to become similar to a diamond, but colored black.", 115, [
            {'name': "Rock Throw", 'type': "Rock", 'damage': 35, 'hit_chance': 0.70},
            {'name': "Tackle", 'type': "Normal", 'damage': 10, 'hit_chance': 0.90}
        ]),
    )


    def __init__(self, player: Player):
        self.player = player


    def play(self):
        """
        Start the main game loop, presenting the main menu to the player and handling their choices.
        """
        while True:
            print("Main Menu:")
            if self.player.current_pokemon is None:
                print("1. Choose your Pokémon")
            else:
                print(f"1. Change {self.player.current_pokemon.name} with another Pokémon")
            print("2. Initiate a battle")
            print("3. Exit")
            choice = input("Choose an option: ")
            
            if choice == '1':
                self.pick_pokemon()
            elif choice == '2':
                self.battle()
            elif choice == '3':
                print("Exiting the game.")
                break
            else:
                print("Invalid choice. Please try again.\n")


    def pick_pokemon(self):
        """
        Allow the player to choose a Pokémon from the available list, POKEMON_LIST and set it as their current Pokémon.
        """
        # Display available Pokémon
        self._list_pokemon()
        picked_pokemon = self._choice_validation("Choose a Pokémon by number: ", self.POKEMON_LIST)

        # Exit if choice is invalid
        if picked_pokemon is None:
            return

        # Set the chosen Pokémon as the player's current Pokémon
        self.player.choose_pokemon(self.POKEMON_LIST[picked_pokemon])
        print(f"You have selected {self.player.current_pokemon.name}.\n")


    def battle(self):
        """
        Initiate a battle sequence between the player's current Pokémon and an opposing Pokémon of their choice.

        If the player has not chosen a Pokémon, the battle cannot proceed.
        After the battle, both Pokémon's health is restored to full in order to accommodate for future battles.
        """
        if self.player.current_pokemon is None:
            print("You have no Pokémon selected. Choose a Pokémon first.\n")
            return

        # Allow the user to select opponent
        self._list_pokemon()
        picked_opponent = self._choice_validation("Choose an opponent Pokémon by number: ", self.POKEMON_LIST)

        # Exit if choice is invalid
        if picked_opponent is None:
            return

        opponent = self.POKEMON_LIST[picked_opponent]

        # Initiate battle sequence
        print(f"\nBattle Start: {self.player.current_pokemon.name} vs {opponent.name}\n")
        self._fight(opponent)

        # Restore health after the battle
        self.player.current_pokemon.restore_health()
        opponent.restore_health()


    def _list_pokemon(self):
        print("\nAvailable Pokémon:")
        # Display Pokémon index, name, type and description.
        for i, pokemon in enumerate(self.POKEMON_LIST):
            print(f"{i + 1}. {pokemon}")
        print()


    def _choice_validation(self, input_text: str, validated_list: list):
        """
        Validate the player's input when selecting an option from a list.

        Args:
            input_text (str): The prompt to display to the player.
            validated_list (list): The list of valid choices. Input should not exceed its length.

        Returns:
            int or None: The index of the chosen item in the list, or None if the input is invalid.
        """
        # Get input from the player
        choice_input = input(input_text)
        # Exit if input is not a digit
        if not choice_input.isdigit():
            print("Invalid choice.\n")
            return
        
        # Convert input to list index
        choice = int(choice_input) - 1
        # Exit if choice is out of valid range
        if choice < 0 or choice >= len(validated_list):
            print("Invalid choice.\n")
            return

        return choice


    def _fight(self, opponent_pokemon: Pokemon):
        """
        Handle the battle sequence alternating turns between the player's Pokémon and the opposing one.
        Each Pokémon selects and executes a move, and the battle continues until a Pokémon's health is depleted.

        Args:
            opponent_pokemon (Pokemon): The opponent's Pokémon object.
        """
        while True:
            # Player selects a move from the displayed available moves.
            print("Choose a move:")
            for i, move in enumerate(self.player.current_pokemon.moves):
                print(f"{i + 1}. {move['name']}")

            move_choice = self._choice_validation("Select a move: ", self.player.current_pokemon.moves)
            if move_choice is not None:
                # Player attacks
                self.player.current_pokemon.attack(self.player.current_pokemon.moves[move_choice], opponent_pokemon)
                # End battle if opponent faints
                if opponent_pokemon.is_fainted():
                    print(f"{opponent_pokemon.name} has fainted! {self.player.name} wins!\n")
                    break     

                # Opponent attacks randomly
                opponent_move = random.choice(opponent_pokemon.moves)
                # End battle if player's Pokémon faints
                opponent_pokemon.attack(opponent_move, self.player.current_pokemon)
                if self.player.current_pokemon.is_fainted():
                    print(f"{self.player.current_pokemon.name} has fainted! {self.player.name} loses!\n")
                    break
            else:
                print("Invalid move choice. Try again.\n")
