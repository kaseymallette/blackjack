# import necessary libraries
from create_shoe import Shoe


class Stats:
    "Defines and tracks the statistics of each shoe."

    def __init__(self):
        "Initialize a new object with no attributes."

    def create_stats(self, shoe):
        "Define stats and set the default of each stat to 0."

        stats = ['player_win', 'player_loss', 'push', 'win_push', 'total_hands',
        'win_pct', 'win_push_pct', 'num_of_splits', 'double', 'doubles_won',
        'doubles_lost', 'doubles_won_pct', 'player_bj', 'dealer_bj',
        'dealer_high_card', 'dealer_low_card', 'dealer_bust', 'dealer_draw',
        'dealer_stand', 'dealer_bust_pct', 'dealer_draw_pct','dealer_stand_pct',
        'dealer_avg_hand', 'num_of_shuffles', 'shuffle_method']

        for key in stats:
            shoe.shoe_stats.setdefault(key, 0)

    def track_stats(self, shoe, stat):
        """When a stat is called, add 1 to the sum of its count.
        For the outcome of each hand, if stat = outcome, print the outcome.
        """

        shoe.shoe_stats[stat] = shoe.shoe_stats[stat] + 1

        # Print 'player wins' and track doubles won
        if stat == 'player_win':
            print('Player wins')
            if shoe.shoe_stats['double'] == 1:
                Stats().track_stats(shoe, 'doubles_won')

        # Print 'dealer wins' and track doubles lost
        elif stat == 'player_loss':
            print('Dealer wins')
            if shoe.shoe_stats['double'] == 1:
                Stats().track_stats(shoe, 'doubles_lost')

        # If the hand is tied, print 'push'
        elif stat == 'push':
            print('Push')

        else:
            pass
