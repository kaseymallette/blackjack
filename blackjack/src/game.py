# Import necessary libraries
from create_shoe import Shoe
from shoe_stats import Stats
from play_shoe import Play


class Game:
    "Continuously plays through blackjack shoes."

    def __init__(self, decks, game, method, shoe_fh, hand_fh):
        "Initialize a new game object."
        self.new_game(decks, game, method, shoe_fh, hand_fh)

    def new_game(self, decks, game, method, shoe_fh, hand_fh):
        """Create a new blackjack shoe of x number of decks.
        Define the type of game, (play or run), the shuffle method,
        and the csv file handles needed to store shoe and hand data.
        """

        self.new_shoe = Shoe(decks, game)
        self.game = game
        self.method = method
        self.shoe_fh = shoe_fh
        self.hand_fh = hand_fh

        # Set default stats for the shoe
        Stats().create_stats(self.new_shoe)

        # Play shoe
        Play(self.new_shoe, method, shoe_fh, hand_fh)

        if self.game == 'play':
            # Determine whether or not the user wants to continue play
            while True:
                print("\nWould you like to play another shoe?")
                next_shoe_input = input("Enter 'yes' to play or 'no' to quit ")
                if next_shoe_input == 'yes':
                    # Set shoe_index to 0, set default stats, and play shoe
                    self.new_shoe.shoe_index = 0
                    Stats().create_stats(self.new_shoe)
                    Play(self.new_shoe, method, shoe_fh, hand_fh)
                try:
                    if next_shoe_input == 'no':
                        break
                    else:
                        print("Please enter yes or no")
                except:
                    print("Please enter yes or no")


    def continue_play(self, num_of_shoes):
        "If self.game == run, continously deal shoes until x = num_of_shoes."

        index = 0
        play_until = num_of_shoes - 1
        while index < play_until:
            # Set index to 0, set default stats, and play shoe
            self.new_shoe.shoe_index = 0
            Stats().create_stats(self.new_shoe)
            Play(self.new_shoe, self.method, self.shoe_fh, self.hand_fh)
            index +=1
