from player import Player
from game import Game

if __name__ == "__main__":
    player_1 = Player(input("Insert player's name: "))
    game = Game(player_1)
    game.play()