class Test:
    """Uses variations of the shuffle method and num_of_shoes for run.py
    to run tests and generate data.
    """

    def __init__(self):
        pass

    def find_dir(self):
        "Find and change the working directory."

        # Import necessary libraries
        import os
        import sys

        # Change working directory to /src
        os.getcwd()
        os.chdir('../')
        path = os.getcwd()
        dir = os.path.abspath(str(path))
        sys.path == dir
        sys.path.append("./src")

    def run_test(self, test_shuffle, test_shoes):
        "Run test where shuffle = test_shuffle and num_of_shoes = test_shoes."

        # Import necessary libraries
        from file_path import Path
        from game import Game

        # Define file path for shoe data
        shoe_fh = Path('shoe_data.csv').path

        # Define file path for hand data
        hand_fh = Path('hand_data.csv').path

        # Use test_shuffle and run through test_shoes using basic strategy
        decks = 6
        game = 'run'
        shuffle = test_shuffle
        num_of_shoes = test_shoes

        # Run blackjack game
        Game(decks, game, shuffle, shoe_fh, hand_fh).continue_play(num_of_shoes)
