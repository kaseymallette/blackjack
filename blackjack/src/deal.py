# Import necessary libraries
from create_shoe import Shoe
from shoe_stats import Stats
from hand import Hand
from player import Player
from outcome import Outcome


class Deal:
    "Deals a new hand by iterating through the cards in the shoe."

    def __init__(self, shoe):
        "Initializes a new deal object."
        self.deal_hand(shoe)

    def deal_hand(self, shoe):
        """Deals a hand using enum_shoe() to iterate through the shoe.
        If the dealer doesn't have blackjack, the player's hand is played.
        If the player doesn't bust, the dealer's hand is played.
        The outcome of the hand is then determined.
        """

        self.player_cards = []
        self.dealer_cards = []

        # Reset count for double and num_of_splits
        shoe.shoe_stats['double'] = 0
        shoe.shoe_stats['num_of_splits'] = 0

        # Deal two cards to the player and two cards to the dealer
        for i in range(4):
            shoe.enum_shoe()
            next_card = shoe.next_card
            # Alternate between player and dealer when dealing
            if (i % 2) == 0:
                self.player_cards.append(next_card)
            else:
                self.dealer_cards.append(next_card)

        # Create player and dealer hands
        player = Hand(self.player_cards[0], self.player_cards[1])
        dealer = Hand(self.dealer_cards[0], self.dealer_cards[1])

        # Deal the dealer's up card and player's hand
        dealer.dealer_up_card(player)
        player.player_cards(shoe)

        # Track when the dealer's up card is a 10
        if dealer.card_1.num == 10:
            Stats().track_stats(shoe, 'dealer_ten')

        # Check for dealer blackjack
        if dealer.soft_large == 21:
            Stats().track_stats(shoe, 'dealer_bj')
            player.is_blackjack = True
            print("Dealer blackjack")
            print(dealer.hand[0], dealer.hand[1])

        # Check for player blackjack
        if player.soft_large == 21:
            Stats().track_stats(shoe, 'player_bj')
            print("Player blackjack")

        # Play the hand
        if dealer.sum != 21:
            if player.sum != 21:
                Player(shoe, player, dealer)
                # If player stands and hand is soft, sum = soft_large
                if type(player.sum) == list:
                    player.sum = player.soft_large
                if type(dealer.sum) == list:
                    dealer.sum = dealer.soft_large
                # Print dealer's hand
                print("\nDealer's hand:")
                print(dealer.hand[0], dealer.hand[1])
                # If player doesn't bust, play dealer's hand
                if player.sum <= 21:
                    dealer.dealer_rules(shoe)

        # Determine the winner of the hand
        if shoe.shoe_stats['num_of_splits'] > 0:
            Outcome().split_tree(player, dealer, shoe)
        else:
            Outcome().win_hand(player, dealer, shoe)
            # Append player data to hands_played
            player.get_data()
            shoe.hands_played.append(player.data)

        # If the dealer doesn't bust, append hand to dealer_hand_sum
        if dealer.sum < 21:
            shoe.dealer_hand.append(dealer.sum)

        # Track when the dealer draws to make a hand
        if len(dealer.hand) > 2:
            if dealer.sum <= 21:
                if dealer.sum >= 17:
                    Stats().track_stats(shoe, 'dealer_draw')
            # Track when the dealer draws to 21
            if dealer.sum == 21:
                Stats().track_stats(shoe, 'dealer_21_draw')

        # Determine how many cards are remaining in the shoe
        player_len = len(player.hand)
        dealer_len = len(dealer.hand)
        cards_used = player_len + dealer_len
        shoe.cards_remaining = shoe.cards_remaining - cards_used
