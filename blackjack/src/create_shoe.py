# Import necessary libraries
from random import shuffle


class Suit:
    "Defines the unicode character for each suit: heart, club, diamond, spade."

    def __init__(self):
        "Initialize a new object with suit attributes."
        self.create_suits()


    def create_suits(self):
        "Create attributes to access each suit, as well as list of the suits."

        heart = u"\u2665"
        club = u"\u2663"
        diamond = u"\u2666"
        spade = u"\u2660"

        self.heart = heart
        self.club = club
        self.diamond = diamond
        self.spade = spade
        self.suits = [heart, club, diamond, spade]


class Value:
    "Defines the value of each card as both a string and an integer."

    def __init__(self):
        "Initialize a new object with value attributes."
        self.create_values()


    def create_values(self):
        """Create a dictionary to store card values, in which the key, value
        pairs represent the value, both as a string and an integer.
        """

        self.value_dict = {}
        self.int = [[1, 11], 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        self.str = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10",
        "jack", "queen", "king"]

        # Build a dictionary from two lists
        for key in self.str:
            for value in self.int:
                self.value_dict[key] = value
                self.int.remove(value)
                break


class Card:
    "Creates a card of suit x and value y."

    def __init__(self, suit, value):
        "Initialize a new card object given the suit and value"
        self.create_card(suit, value)


    def create_card(self, suit, value):
        """Instantiate a string object and a value object and use both objects
        to define the suit, the string value, and integer value of the card.
        Display the card as a string of the suit and value.
        """

        s = Suit()
        v = Value()

        if suit in s.suits:
            self.suit = suit
        if value in v.str:
            self.value = value

        # Define the card and its numerical value
        self.card = suit + value
        self.num = v.value_dict[value]

        # Determine if the card is an ace
        self.is_ace = False
        if value == 'ace':
            self.is_ace = True


class Deck:
    """Creates a deck arranged in new deck order, in which
    the suits are ordered by spades, diamonds, clubs, and hearts.
    The spades and diamonds appear in ascending order,
    while the clubs and hearts are in descending order.
    """

    def __init__(self):
        "Initialize a new deck object."
        self.new_deck()


    def new_deck(self):
        """Instantiate both a string object and a value object.
        Separate the suits into two groups and append the cards in each
        group according to the order in which they are arranged.
        """

        new_deck = []

        # Reverse the order of the suits
        card_suits = Suit().suits[::-1]

        # Define the values in both ascending and descending order
        ascending = Value().str
        descending = ascending[::-1]

        # Arrange spades and diamonds from ace to king
        for suit in card_suits[0:2]:
            for value in ascending:
                new_card = Card(suit, value).card
                new_deck.append(new_card)

        # Arrange clubs and diamonds from king to ace
        for suit in card_suits[2::]:
            for value in descending:
                new_card = Card(suit, value).card
                new_deck.append(new_card)

        # Return the deck as a list
        self.return_deck = new_deck


class Shoe:
    """Creates a shoe from an even number of decks, with attributes to
    find the number of cards remaining in the shoe, to iterate through
    the shoe, and to track the outcomes of the hands in the shoe.
    To play shoes using the input function, game = 'play',
    To run n number of shoes, game = 'run'.
    """

    def __init__(self, num, game):
        "Initialize a new shoe from the number of decks needed for the shoe."
        self.build_shoe(num, game)


    def build_shoe(self, num, game):
        """Create a new shoe of an even number of decks by instantiating
        a deck object. Wash or combine two decks at a time and append
        the cards to the shoe until all decks have been combined.
        """

        self.deck = Deck().return_deck
        self.num = num
        self.wash = int(num/2)
        self.game = game

        # Create empty lists and dictionaries
        self.return_shoe = []
        self.dealer_hand = []
        self.hands_played = []
        self.shuffled_cards = []
        self.shoe_stats = {}
        self.card_count = {}

        # Shuffle two decks at a time for num/2 times
        for i in range(self.wash):
            wash_decks = self.deck + self.deck

            # Section the list by creating groups of tuples
            clumps = []
            n = 8
            for i in range(0, len(wash_decks), n):
                value = wash_decks[i:i+n]
                if len(value) == n:
                    clump = tuple(value)
                    clumps.append(clump)

            # Wash the clumps togehter
            shuffle(clumps)

            # Flatten the list
            z = []
            for x in clumps:
                for y in x:
                    z.append(y)

            # Append the cards to return_shoe
            for card in z:
                self.return_shoe.append(card)

        # Find the number of cards left in the shoe
        self.cards_remaining = 52*num
        self.shoes_dealt = 0

        # Discard the first card of the shoe
        self.shoe_index = 0
        self.next_card = self.return_shoe[self.shoe_index]


    def enum_shoe(self):
        "Add a counter for next_card, which iterates through the shoe."

        self.shoe_index +=1
        self.next_card = self.return_shoe[self.shoe_index]


    def count_cards(self, list):
        "Track how many of each card are in the shoe."

        for card in list:
            count = list.count(card)
            self.card_count[card] = count
