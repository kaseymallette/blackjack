# Import necessary libraries
import sys
sys.path.append("./src")
from file_path import Path
from game import Game

# Define file path for shoe data
shoe_fh = Path('blackjack_play.csv').path

# Define file path for hand data
hand_fh = Path('blackjack_hands.csv').path

# Play a six deck shoe allowing for user input
decks = 6
game = 'play'
shuffle = 'python'

# Play blackjack game
Game(decks, game, shuffle, shoe_fh, hand_fh)
