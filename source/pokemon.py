import random

class Pokemon:
    # Type effectiveness chart where each key is a tuple (attack type, defender's type). The value is the damage multiplier.
    TYPE_CHART = {
        ('Fire', 'Grass'): 2.0,
        ('Fire', 'Bug'): 2.0,
        ('Fire', 'Water'): 0.5,
        ('Water', 'Fire'): 2.0,
        ('Water', 'Rock'): 2.0,
        ('Water', 'Grass'): 0.5,
        ('Grass', 'Water'): 2.0,
        ('Grass', 'Rock'): 2.0,
        ('Grass', 'Fire'): 0.5,
        ('Electric', 'Water'): 2.0,
        ('Electric', 'Grass'): 0.5,
        ('Electric', 'Rock'): 0.5,
        ('Bug', 'Grass'): 2.0,
        ('Bug', 'Psychic'): 2.0,
        ('Bug', 'Rock'): 0.5,
        ('Rock', 'Bug'): 2.0,
        ('Rock', 'Fire'): 2.0,
        ('Rock', 'Grass'): 0.5
        # Add more type interactions as needed
    }

    def __init__(self, name: str, type: str, description: str, health: int, moves: list):
        self.name = name
        self.type = type
        self.description = description
        self.health = health
        # Store the initial health for later restoration
        self.initial_health = health
        self.moves = moves

    def attack(self, move: str, other_pokemon: "Pokemon"):
        """
        Execute an attack on another Pokémon using a specified move.

        The attack can miss based on the move's hit chance. The damage is calculated based on the move's
        base damage and the type effectiveness. There's also a chance of landing a critical hit,
        which adds a damage multiplier, unless the move is weak against the opponent's type.

        Args:
            move (str): The move to use for the attack.
            other_pokemon (Pokemon): The opponent Pokémon to attack.
        """
        if random.random() > move['hit_chance']:
            # Missed attack if random value is higher than the hit chance
            print(f"{self.name} uses {move['name']}... but it misses!\n")
            return

        # Calculate damage based on type effectiveness
        base_damage = move['damage']
        effectiveness = self._get_type_effectiveness(move['type'], other_pokemon.type)
        damage = base_damage * effectiveness

        # Determine if the attack is a critical hit. 10% chance to deal double the damage when the attack type effectiveness is not weak against the opponent's type
        critical_hit = False
        if effectiveness != 0.5 and random.random() < 0.1:
            damage *= 2
            critical_hit = True

        # Apply damage to the opponent
        other_pokemon.health -= damage
        print(f"\n{self.name} uses {move['name']}!")
        if effectiveness > 1:
            print("It's super effective!")
        elif effectiveness < 1:
            print("It's not very effective...")

        if critical_hit:
            print("A critical hit!")

        print(f"{move['name']} deals {damage:.1f} damage to {other_pokemon.name}!")
        print(f"{other_pokemon.name} has {other_pokemon.health} health remaining.\n")

    def _get_type_effectiveness(self, attack_type: str, defender_type: str):
        """
        Get the effectiveness multiplier of an attack based on its type and the defending Pokémon.

        Args:
            attack_type (str): The type of the attack move.
            defender_type (str): The type of the defending Pokémon.

        Returns:
            float: The effectiveness multiplier (2.0 for super effective, 0.5 for not very effective).
        """
        return self.TYPE_CHART.get((attack_type, defender_type), 1.0)

    def is_fainted(self):
        return self.health <= 0
    
    def restore_health(self):
        self.health = self.initial_health

    def __str__(self):
        # Format the available Pokémon list's name, type and description to be displayed as a string
        return f"{self.name} [Type: {self.type}] - {self.description}"