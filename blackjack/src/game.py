# Import necessary libraries
from create_shoe import Shoe
from shoe_stats import Stats
from play_shoe import Play


class Game:
    "Continuously plays through blackjack shoes."

    def __init__(self, decks, game, method, shoe_fh, hand_fh):
        "Initialize a new game object."

        self.new_shoe = Shoe(decks, game)
        self.game = game
        self.method = method
        self.shoe_fh = shoe_fh
        self.hand_fh = hand_fh

        if self.game == 'play':
            self.new_game()

    def new_game(self):
        """Create a new blackjack shoe of x number of decks.
        Define the type of game, (play or run), the shuffle method,
        and the csv file handles needed to store shoe and hand data.
        """

        # Play shoe
        Stats().create_stats(self.new_shoe)
        Play(self.new_shoe, self.method, self.shoe_fh, self.hand_fh)

        # Determine whether or not the user wants to continue play
        while True:
            print("\nWould you like to play another shoe?")
            next_shoe_input = input("Enter 'yes' to play or 'no' to quit ")
            if next_shoe_input == 'yes':
                # Set shoe_index to 0, set default stats, and play shoe
                self.new_shoe.shoe_index = 0
                Stats().create_stats(self.new_shoe)
                Play(self.new_shoe, self.method, self.shoe_fh, self.hand_fh)
            try:
                if next_shoe_input == 'no':
                    break
                else:
                    print("Please enter yes or no")
            except:
                print("Please enter yes or no")


    def continue_play(self, num_of_shoes):
        "If self.game == run, continously deal shoes until x = num_of_shoes."

        play_until = range(num_of_shoes)
        for i,n in enumerate(play_until):
            # Set index to 0, set default stats, and play shoe

            self.new_shoe.shoe_index = 0
            Stats().create_stats(self.new_shoe)
            Play(self.new_shoe, self.method, self.shoe_fh, self.hand_fh)
