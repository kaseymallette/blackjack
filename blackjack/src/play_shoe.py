# Import necessary libraries
import pandas as pd
from os import path
from create_shoe import Shoe
from deal import Deal
from shuffle import Shuffle

class Play:
    "Plays through a blackjack shoe."

    def __init__(self, shoe, method, shoe_fh, hand_fh):
        "Initializes a new play object."
        self.method = method
        self.play_shoe(shoe, method, shoe_fh, hand_fh)


    def play_shoe(self, shoe, method, shoe_fh, hand_fh):
        """Given a shuffle method, shuffle the shoe and continously deal hands.
        Deal until there are only 75 cards (1 1/2 decks) left in the shoe.
        If shoe.game == 'play' and the user enters 'exit', play will stop.
        After the shoe ends or play has stopped, track shoe data in shoe_fh
        and hand data in hand_fh.
        """

        shoe.shoes_dealt +=1
        shuffle_shoe = Shuffle(shoe, method)

        while True:
            Deal(shoe)
            # To end play during the shoe, the user can enter 'exit'
            if shoe.game == 'play':
                deal_input = input("\nTo deal the next hand, press return ")
                try:
                    if deal_input == "exit":
                        break
                    elif deal_input != "":
                        print("If you want to stop playing, type 'exit' ")
                        print("Otherwise, press return ")
                    else:
                        pass
                except:
                    pass
            # Deal until 75 cards or less are left in the shoe
            if shoe.cards_remaining <= 75:
                print("\n--End of shoe--\n")
                break

        # Create variables from shoe_stats
        win = shoe.shoe_stats['player_win']
        loss = shoe.shoe_stats['player_loss']
        push = shoe.shoe_stats['push']
        doubles_won = shoe.shoe_stats['doubles_won']
        doubles_lost = shoe.shoe_stats['doubles_lost']
        dealer_bust = shoe.shoe_stats['dealer_bust']
        dealer_draw = shoe.shoe_stats['dealer_draw']
        dealer_stand = shoe.shoe_stats['dealer_stand']

        # Find the total number of hands won
        total = len(shoe.hands_played)
        shoe.shoe_stats['total_hands'] = total

        # Find the total number of hands won and pushed
        win_push = win + push
        shoe.shoe_stats['win_push'] = win_push

        # Find the percentage of doubles won
        total_doubles = doubles_won + doubles_lost
        if total_doubles > 0:
            doubles_pct = doubles_won / total_doubles
            shoe.shoe_stats['doubles_won_pct'] = round(doubles_pct, 3)

        # Find the shuffle method and number of shuffles of the same shoe
        shoe.shoe_stats['shuffle_method'] = self.method
        shoe.shoe_stats['num_of_shuffles'] = shoe.shoes_dealt

        # Convert continuous variables to percentages and round
        shoe.shoe_stats['win_pct'] = round(win / total, 3)
        shoe.shoe_stats['win_push_pct'] = round(win_push / total, 3)
        shoe.shoe_stats['dealer_bust_pct'] = round(dealer_bust / total, 3)
        shoe.shoe_stats['dealer_draw_pct'] = round(dealer_draw / total, 3)
        shoe.shoe_stats['dealer_stand_pct'] = round(dealer_stand / total, 3)

        # Find the dealer's average hand
        if len(shoe.dealer_hand) > 0:
            avg_hand = sum(shoe.dealer_hand)/len(shoe.dealer_hand)
            avg_hand_rounded = round(avg_hand, 3)
            shoe.shoe_stats['dealer_avg_hand'] = avg_hand_rounded

        # Print total hands, along with hands won, lost, and pushed
        if shoe.cards_remaining > 75:
            print("\n--End of play--\n")
        if total == 1:
            print(total, "hand played")
        if total > 1:
            print(total, "hands played")
        print("Won: ", win)
        print("Lost: ", loss)
        print("Pushed: ", push)

        # Copy shoe_stats to data and remove unnecessary and dublicate data
        data = shoe.shoe_stats.copy()
        data.pop('double')
        data.pop('num_of_splits')

        # Create a dataframe from data and transpose it
        df0 = pd.DataFrame.from_dict(data, orient='index')
        df1 = df0.transpose()

        # Change data types from float to int
        change_dtypes = {}
        change_to_int = ['player_win', 'player_loss', 'push', 'win_push',
                        'total_hands', 'doubles_won', 'doubles_lost',
                        'player_bj', 'dealer_bj', 'dealer_high_card',
                        'dealer_low_card', 'dealer_bust', 'dealer_draw',
                        'dealer_stand', 'num_of_shuffles']

        if type(shoe.shoe_stats['shuffle_method']) == int:
            change_to_int.append('shuffle_method')

        for key in change_to_int:
            change_dtypes[key] = int

        df1 = df1.astype(change_dtypes)

        # Check path for shoe csv
        check_path = path.exists(shoe_fh)

        # If csv doesn't exist, create csv and append shoe
        if check_path == False:
            df1.to_csv(shoe_fh)
        else:
            with open(shoe_fh, 'a') as fh:
                df1.to_csv(fh, header=False)

        # Create a df for hands played
        hand_list = shoe.hands_played
        for hand in hand_list:
            hand.append(method)

        hand_columns = ['dealer_up', 'player', 'move', 'outcome',
                        'dealer_outcome', 'dealer_bj', 'is_split',
                        'orig_hand', 'shuffle']

        df2 = pd.DataFrame(hand_list, columns=hand_columns)

        # Replace moves 0-2 with stand, hit, or double
        df2['move'] = df2['move'].replace([0], 'stand')
        df2['move'] = df2['move'].replace([1], 'hit')
        df2['move'] = df2['move'].replace([2], 'double')

        # Change the data types to strings
        df2['player'] = df2['player'].astype(str)
        df2['dealer_up'] = df2['dealer_up'].astype(str)
        df2['dealer_outcome'] = df2['dealer_outcome'].astype(str)
        df2['orig_hand'] = df2['orig_hand'].astype(str)

        # Check path for hand csv
        check_path_2 = path.exists(hand_fh)

        # If csv doesn't exist, create csv and append hands played
        if check_path_2 == False:
            df2.to_csv(hand_fh)
        else:
            with open(hand_fh, 'a') as fh2:
                df2.to_csv(fh2, header=False)

        # Clear values of shoe_stats, hands_played, and cards remaining
        shoe.shoe_stats.clear()
        shoe.hands_played.clear()
        shoe.cards_remaining = shoe.num*52
