# Import necessary libraries
from create_shoe import Suit, Value, Card, Shoe
from shoe_stats import Stats


class Hand:
    """Creates a hand of card objects with functions that allow for
    finding the sum of the hand, adding cards to the hand, splitting
    the cards into two hands if the hand is a pair, defining rules
    for the dealer's hand, and dealing the player cards diagonally.
    """

    def __init__(self, card_1, card_2):
        "Initialize a new hand, composed of two cards, card_1 and card_2."
        self.new_hand(card_1, card_2)


    def new_hand(self, card_1, card_2):
        """Create a hand by instantiating two card objects from card strings.
        Create a list of the card objects, as well as a list of the integer
        values and string values of the hand. Add instance attributes
        so that the hand can be summed and split.
        """

        self.card_1 = Card(card_1[0], card_1[1:])
        self.card_2 = Card(card_2[0], card_2[1:])

        self.cards = [self.card_1, self.card_2]
        self.hand = [self.card_1.card, self.card_2.card]
        self.num = [self.card_1.num, self.card_2.num]

        # Let self.data contain all of the data for a particualr hand
        self.data = []

        # Create instance attributes for the hand
        setattr(self, 'dealer_up', 0)
        setattr(self, 'player', 0)
        setattr(self, 'move', 0)
        setattr(self, 'outcome', 0)
        setattr(self, 'dealer_outcome', 0)
        setattr(self, 'dealer_card', 0)
        setattr(self, 'is_soft', False)

        # Create instance attributes for summing the hand
        setattr(self, 'sum', 0)
        setattr(self, 'soft_small', 0)
        setattr(self, 'soft_large', 0)
        setattr(self, 'ace_count', 0)
        setattr(self, 'blackjack', 0)
        setattr(self, 'is_blackjack', False)

        # Create instance attributes for splitting the hand
        setattr(self, 'pair', 0)
        setattr(self, 'is_split', False)
        setattr(self, 'hand_1', 0)
        setattr(self, 'hand_2', 0)
        setattr(self, 'orig_hand', 0)

        # If the hand is a pair, self.pair = 1
        if self.card_1.value == self.card_2.value:
            self.pair = 1


    def find_sum(self):
        """Use is_soft to determine if the hand contains any aces.
        For hard hands (with no aces) add each card to self.sum.
        For soft hands (with at least one ace), add each card to
        self.soft_small and self.soft_large. If there is only one ace,
        the ace counts as 1 or 11. If there is more than one ace,
        the first ace counts as 1 or 11, and the remaining aces count as 1.
        The type of hard hands is an integer, while the type of soft hands
        is a list of both possible values, soft_small and soft_large.
        """

        # To find the sum of soft hands, use add_to_soft
        def add_to_soft(card_1, card_2):
            "Add card_1 to soft_small and card_2 to soft_large"

            self.soft_small = self.soft_small + card_1
            self.soft_large = self.soft_large + card_2

        # Set constansts to 0
        self.sum = 0
        self.soft_small = 0
        self.soft_large = 0
        self.ace_count = 0

        # If the hand contains an ace, is_soft is True
        for card in self.cards:
            if card.is_ace == True:
                self.is_soft = True

        # Add each card in self.cards
        for card in self.cards:
            if self.is_soft == True:
                if card.is_ace == False:
                    add_to_soft(card.num, card.num)
                else:
                    self.ace_count = self.ace_count + 1
                    # The first ace counts as 1 or 11
                    if self.ace_count == 1:
                        add_to_soft(card.num[0], card.num[1])
                    # Additional aces only count as 1
                    if self.ace_count > 1:
                        add_to_soft(card.num[0], card.num[0])
            else:
                self.sum = self.sum + card.num

        # Create rules for when to use soft_small and soft_large
        if self.ace_count > 0:
            # The sum of soft hands is a list
            self.sum = [self.soft_small, self.soft_large]
            # If there are only two cards, and the cards equal 21: blackjack
            if self.soft_large == 21:
                if len(self.hand) == 2:
                    self.sum = self.soft_large
                    self.blackjack == 1
            # If soft_large is greater than 21, sum = soft_small
            if self.soft_large > 21:
                self.sum = self.soft_small
            # If soft_large is between 18 and 21, sum = soft_large
            if self.soft_large <=21:
                if self.soft_large > 18:
                    self.sum = self.soft_large


    def hit(self, shoe):
        """Add additional cards to the hand by using shoe.enum_shoe(),
        which iterates through the cards in the shoe. Append each card
        to self.cards, self.hand, and self.num. Find the sum of the hand,
        then print the card and new sum.
        """

        shoe.enum_shoe()
        deal_card = shoe.next_card
        new_card = Card(deal_card[0], deal_card[1:])

        # Append the card
        self.cards.append(new_card)
        self.hand.append(new_card.card)
        self.num.append(new_card.num)

        # Find the sum of the hand
        self.find_sum()

        # Print the new card and new sum
        print("Card: ", new_card.card)
        print("Hand: ", self.sum)


    def split(self, shoe):
        """Create two hands, in which self.hand_1 contains the first card
        of the pair and self.hand_2 contains the second card. Use
        shoe.enum_shoe() to get cards from the shoe to add to each hand.
        """

        shoe.enum_shoe()
        self.hand_1 = Hand(self.hand[0], shoe.next_card)

        shoe.enum_shoe()
        self.hand_2 = Hand(self.hand[1], shoe.next_card)


    def dealer_up_card(self, player):
        "Find the sum of the dealer's hand and print the dealer's up card."

        self.find_sum()
        up_card = self.card_1

        # Assign dealer's up card to player.dealer_up for hand data
        player.dealer_up = str(up_card.num)
        if up_card.num == [1,11]:
            player.dealer_up = 'A'

        # Print the card
        print("\nDealer: ", up_card.card, "\n")


    def player_cards(self, shoe):
        "Find the sum of the player's hand and print the cards diagonally."

        self.find_sum()

        # Assign hand to self.player for hand data
        if self.num == [[1, 11], [1, 11]]:
            self.player = 'ace, ace'
        elif self.pair == True:
            if shoe.shoe_stats['num_of_splits'] >= 3:
                self.player = self.sum
            else:
                self.player = self.num[0:2]
        else:
            self.player = self.sum

        # Print the hand
        print("Player's hand:    ", self.hand[0])
        print("(", self.sum,")","        ", self.hand[1], "\n")


    def hand_move(self, move):
        "Given an integer from 0 to 3, write the player move as a string."

        if move == 0:
            self.move = 'stand'
        elif move == 1:
            self.move = 'hit'
        elif move == 2:
            self.move = 'double'
        elif move == 3:
            self.move = 'split'
        else:
            pass


    def dealer_rules(self, shoe):
        """Dealer stands on all 17s.
        For soft hands, the dealer stands when soft_large is between 17 and 21.
        For hard hands, the dealer stands when the sum is between 17 and 21.
        Use Stats().track_stats to count how many times the dealer busts.
        """

        while True:

            # Define when to stand on soft_large
            if type(self.sum) == list:
                if self.soft_large <=21:
                    if self.soft_large >= 17:
                        self.sum = self.soft_large
                    else:
                        self.hit(shoe)
                        continue

            # Evaluate the dealer's hand
            if self.sum > 21:
                print("Dealer busts")
                break
            elif self.sum >= 17:
                print("Dealer has: ", self.sum)
                break
            else:
                self.hit(shoe)
                continue


    def find_outcome(self, outcome):
        "Assign the hand an outcome."

        self.outcome = outcome


    def get_data(self):
        "Get the data for the hand."

        self.data = [self.dealer_up, self.player, self.move, self.outcome,
                    self.dealer_outcome, self.dealer_card, self.is_blackjack,
                    self.is_split, self.orig_hand]
