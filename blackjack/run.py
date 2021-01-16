# Import necessary libraries
import sys
sys.path.append("./src")
from file_path import Path
from game import Game

# Define file path for shoe data
shoe_fh = Path('blackjack_run.csv').path

# Define file path for hand data
hand_fh = Path('blackjack_hands.csv').path

# Run through 25 shoes using basic strategy
decks = 6
game = 'run'
shuffle = 1
num_of_shoes = 25

# Run blackjack game
Game(decks, game, shuffle, shoe_fh, hand_fh).continue_play(num_of_shoes)
