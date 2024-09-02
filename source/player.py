from pokemon import Pokemon

class Player:
    def __init__(self, name: str):
        self.name = name
        self.current_pokemon = None

    def choose_pokemon(self, pokemon: Pokemon):
        self.current_pokemon = pokemon
        print(f"{self.name} has chosen {self.current_pokemon.name}!\n")

    def change_pokemon(self, pokemon: Pokemon):
        self.choose_pokemon(pokemon)