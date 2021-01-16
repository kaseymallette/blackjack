# Import necessary libraries
import pandas as pd
import numpy as np
from create_shoe import Shoe
from shoe_stats import Stats
from hand import Hand
from file_path import Path


class Player:
    """Allows the player to play the hand from available moves.
    0 = Stand - the hand remains as is.
    1 = Hit - additional cards are added until the player stands or sum > 21.
    2 = Double - option is available when the first two cards are dealt.
    3 = Split - option is available when the hand is a pair.
    """

    def __init__(self, shoe, hand, dealer):
        "Initialize a new move object, given the player and dealer hands."
        self.move(shoe, hand, dealer)

    def move(self, shoe, hand, dealer):
        """If shoe.game == 'play', use self.player_input() to play the hand.
        If shoe.game == 'run', use self.run() to play the hand.
        """

        self.game = shoe.game
        self.move = 0

        # Determine which function to use based on the type of game
        if self.game == 'play':
            self.player_input(shoe, hand)
        elif self.game == 'run':
            self.run(shoe, hand, dealer)
        else:
            # Set the default to player_input
            self.game == 'play'
            self.player_input(shoe, hand)

    def player_input(self, shoe, hand):
        "Display available moves and store input as self.move."

        while True:
            # If soft_large equals 21, player must stand
            if hand.soft_large == 21:
                move = 0
                break
            # If the hand is a pair, player can split up to three times
            elif hand.pair == 1:
                if len(hand.hand) == 2:
                    move = input("Stand: 0, Hit: 1, Double: 2, Split: 3 \n")
                    break
                else:
                    move = input("Stand: 0, Hit: 1 \n")
                    break
            # If the hand is a pair of aces, player cannot hit after split
            elif shoe.shoe_stats['num_of_splits'] > 0:
                if hand.card_1.is_ace == True:
                    if hand.card_2.is_ace == False:
                        move = 0
                        break
                else:
                    move = input("Stand: 0, Hit: 1, Double: 2 \n")
                    break
            # Given the first two cards, the player can stand, hit, or double
            elif len(hand.hand) == 2:
                move = input("Stand: 0, Hit: 1, Double: 2 \n")
                break
            # Otherwise, the player can stand or hit
            elif len(hand.hand) > 2:
                move = input("Stand: 0, Hit: 1 \n")
                break
            else:
                break

        # Let move = self.move
        try:
            self.move = int(move)
        except:
            dealer = 0
            print("Please enter a number from the following choices: ")
            Player(shoe, hand, dealer)

        # Store self.move in hand data
        if len(hand.hand) == 2:
            hand.move = self.move
            if hand.move == 3:
                hand.is_split = True

        # Play hand
        dealer = 0
        self.play(shoe, hand, dealer, self.move)


    def run(self, shoe, hand, dealer):
        """Read the csv of basic strategy and convert to numpy array.
        Use the array to find the column of the dealer's up card
        and the row of the player's hand. Use array[row][column]
        to find the player move for that particular hand.
        """

        # Find the path for the csv file for basic_strategy
        basic_strategy = Path('basic_strategy.csv')
        path = basic_strategy.path

        # Convert the csv to a dataframe
        df = pd.read_csv(path)

        # Convert the dataframe to a numpy array
        bs_array = df.to_numpy()

        # Determine data point for player
        player = hand.sum
        if hand.num == [[1, 11], [1, 11]]:
            player = 'ace, ace'
        elif hand.pair == True:
            if shoe.shoe_stats['num_of_splits'] >= 3:
                player = hand.sum
            if shoe.shoe_stats['num_of_splits'] < 3:
                if len(hand.hand) == 2:
                    player = hand.num
        else:
            player = hand.sum

        # Determine data point for dealer
        dealer_up = dealer.card_1.num
        if dealer_up == [1, 11]:
            dealer_up = 'A'

        # Change the type for player
        player = str(player)

        try:
            # Find the row
            player_column = bs_array[1::]
            player_result = np.where(player_column == player)
            row = int(player_result[0])
            row = row + 1

            # Find the column
            dealer_row = bs_array[0]
            dealer_result = np.where(dealer_row == dealer_up)
            column = int(dealer_result[0])

            # Find the corresponding player move
            move = bs_array[row][column]

            # If the move is a string, change to integer
            if type(move) == str:
                move = int(move)
        # If error, move = 0
        except:
            move = 0

        # Let self.move equal move
        self.move = move

        # Player can only split aces once
        if type(hand.sum) == list:
            if shoe.shoe_stats['num_of_splits'] > 0:
                if hand.card_1.is_ace == True:
                    if hand.card_2.is_ace == False:
                        self.move = 0

        # Stop when continouly splitting
        stop = False
        if shoe.shoe_stats['num_of_splits'] >= 3:
            stop = True

        # Store self.move in hand data
        if len(hand.hand) == 2:
            hand.move = self.move
            if hand.move == 3:
                hand.is_split = True

        # Play hand
        if stop == False:
            self.play(shoe, hand, dealer, self.move)


    def play(self, shoe, hand, dealer, move):
        "Using self.move, play hand."

        while True:
            # Stand
            if self.move == 0:
                if type(hand.sum) == list:
                    hand.sum = hand.soft_large
                break
            # Hit
            elif self.move == 1:
                hand.hit(shoe)
                # If hand is hard and player doesn't bust, play again
                if type(hand.sum) == int:
                    if hand.sum == 21:
                        break
                    elif hand.sum > 21:
                        print("Bust")
                        break
                    else:
                        Player(shoe, hand, dealer)
                        break
                # If hand is soft, play again
                else:
                    Player(shoe, hand, dealer)
                    break
            # Double
            elif self.move == 2:
                hand.hit(shoe)
                Stats().track_stats(shoe, 'double')
                if type(hand.sum) == list:
                    hand.sum = hand.soft_large
                break
            # Split
            elif self.move == 3:
                if hand.card_1.value == hand.card_2.value:
                    if shoe.shoe_stats['num_of_splits'] < 3:
                        hand.split(shoe)
                        Stats().track_stats(shoe, 'num_of_splits')
                        # Deal hand_1 and play
                        hand.hand_1.player_cards(shoe)
                        Player(shoe, hand.hand_1, dealer)
                        # Deal hand_2 and play
                        hand.hand_2.player_cards(shoe)
                        Player(shoe, hand.hand_2, dealer)
                        break
                    else:
                        print("You can only split up to three times.")
                        Player(shoe, hand, dealer)
                        break
                else:
                    print("You can only split a pair.")
                    Player(shoe, hand, dealer)
                    break
            # Refer back to Player if given input other than 0-3
            else:
                print("Please enter a number from the following choices: ")
                Player(shoe, hand, dealer)
                break
