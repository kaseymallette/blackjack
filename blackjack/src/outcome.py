# import necessary libraries
from create_shoe import Card, Shoe
from shoe_stats import Stats
from hand import Hand


class Outcome:
    "Determines the winner of the hand."

    def __init__(self):
        "Set the instance attribute 'outcome' equal to 0."
        setattr(self, 'outcome', 0)

    def win_hand(self, player, dealer, shoe):
        "Evaluate both the player and dealer hands to find the outcome."

        # For soft hands, determine the sum of the hand
        if type(player.sum) == list:
            if player.soft_large <= 18:
                player.sum = player.soft_large
            else:
                player.sum = player.soft_small
        if type(dealer.sum) == list:
            if dealer.soft_large < 17:
                dealer.sum = dealer.soft_large
            else:
                dealer.sum = dealer.soft_small

        # Find the outcome of the hand
        # Check for player blackjack
        if player.blackjack == 1:
            if dealer.blackjack == 0:
                outcome = 'win'
            if dealer.blackjack == 1:
                outcome = 'push'
        # Check for dealer blackjack
        elif dealer.blackjack == 1:
            if player.blackjack == 0:
                outcome = 'loss'
        # If the player busts, the player loses the hand
        elif player.sum > 21:
            print("\nPlayer: Bust")
            print("Dealer: ", dealer.sum)
            outcome = 'loss'
        # If the dealer busts and the player doesn't, the player wins
        elif player.sum <= 21:
            if dealer.sum > 21:
                print("\nPlayer: ", player.sum)
                print("Dealer: Bust")
                outcome = 'win'
            # If neither the player nor the dealer busts, evaluate both hands
            if dealer.sum <= 21:
                print("\nPlayer: ", player.sum)
                print("Dealer: ", dealer.sum)
                if player.sum > dealer.sum:
                    outcome = 'win'
                elif player.sum < dealer.sum:
                    outcome = 'loss'
                else:
                    outcome = 'push'
        else:
            outcome = 'none'

        # Track outcome in Stats()
        if outcome == 'win':
            self.outcome = 'win'
            Stats().track_stats(shoe, 'player_win')
        elif outcome == 'loss':
            self.outcome = 'loss'
            Stats().track_stats(shoe, 'player_loss')
        elif outcome == 'push':
            self.outcome = 'push'
            Stats().track_stats(shoe, 'push')
        else:
            pass

        # Track outcome in hand data
        player.outcome = self.outcome


    def split_tree(self, player, dealer, shoe):
        """Run through all of the possible hands that can be split
        and determine the winner. Use hasattr to see if the hand has been split.
        If hasattr is true, use getattr to add the new hands to hands_split.
        If a hand in hands_split has been split, do not include the hand.
        For each hand that is split, create a new entry in hands_played.
        """

        hand = player
        hands_split = []
        split_attr = [hand, hand.hand_1, hand.hand_2,
        hand.hand_1.hand_1, hand.hand_1.hand_2,
        hand.hand_2.hand_1, hand.hand_2.hand_2]

        # If the hand has attribute 'hand_1', the hand has been split
        for attr in split_attr:
            new_attr = hasattr(attr, 'hand_1')
            if new_attr == True:
                new_hand_1 = getattr(attr, 'hand_1')
                new_hand_2 = getattr(attr, 'hand_2')
                hands_split.append(new_hand_1)
                hands_split.append(new_hand_2)

        # Determine the winner of each hand that has been split
        for new_hand in hands_split:
            if isinstance(new_hand, Hand) == True:
                possible_split = getattr(new_hand, 'hand_1')
                if possible_split == 0:
                    new_outcome = Outcome()
                    new_outcome.win_hand(new_hand, dealer, shoe)

                    # Store outcome in hand data
                    new_hand.outcome = new_outcome.outcome

                    # Add dealer up card to hand data
                    dealer_up = dealer.card_1.num
                    if dealer_up == [1,11]:
                        dealer_up = 'A'
                    new_hand.dealer_up = dealer_up

                    # Change is_split to True and add orig_hand to data
                    new_hand.is_split = True
                    if player.num == [[1,11],[1,11]]:
                        new_hand.orig_hand = 'ace, ace'
                    else:
                        new_hand.orig_hand = player.num

                    # Track when the dealer's up card is a high card
                    if dealer_up in [7,8,9,10,'A']:
                        Stats().track_stats(shoe, 'dealer_high_card')
                        new_hand.dealer_card = 'high'

                    # Track when the dealer's up card is a low card
                    if dealer_up in [2,3,4,5,6]:
                        Stats().track_stats(shoe, 'dealer_low_card')
                        new_hand.dealer_card = 'low'


                    # Find the outcome of the dealer's hand
                    if len(dealer.hand) == 2:
                        # Dealer stnads
                        Stats().track_stats(shoe, 'dealer_stand')
                        new_hand.dealer_outcome = 'stand'
                    else:
                        # Dealer draws to make a hand
                        if dealer.sum <= 21:
                            if dealer.sum >= 17:
                                Stats().track_stats(shoe, 'dealer_draw')
                                new_hand.dealer_outcome = 'draw'
                        # Dealer busts
                        if dealer.sum > 21:
                            Stats().track_stats(shoe, 'dealer_bust')
                            new_hand.dealer_outcome = 'bust'

                    # Find data for new_hand and append to hands_played
                    new_hand.get_data()
                    shoe.hands_played.append(new_hand.data)
