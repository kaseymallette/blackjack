# Import necessary libraries
from random import shuffle
from create_shoe import Shoe


class Shuffle:
    "Shuffles the cards based on the given method."

    def __init__(self, shoe, method):
        "Initialize a new shuffle_method."
        self.shuffle_method(shoe, method)


    def shuffle_method(self, shoe, method):
        """If the method is an integer i, the cards will be shuffled
        i times. If the method is a string, the method corresponds to
        three different casino shuffle methods, which split the shoe
        into two piles. The dealer then takes 3/4 of a deck from each pile
        and performs riffle-strip-riffle. A riffle laces the cards,
        while a strip takes sections of 10-20 cards from the top
        of the pile and places them on the bottom of the pile.
        """

        self.method = method
        shoe_list = shoe.return_shoe

        # Create empty lists to place the cards while shuffling
        self.middle = []
        self.group = []
        self.riffle = []
        self.strip = []
        self.pile_1 = []
        self.pile_2 = []

        # Take 3/4 of a deck from each pile (39 cards)
        self.pile_len = 39
        # Take sections of 16 cards when performing the shuffle strip
        self.strip_len = 16

        # Find how many cards are in half of the shoe
        try:
            self.half = int(len(shoe_list)/2)
        except:
            self.half = int((len(shoe_list)+1)/2)

        # Determine which shuffle method to use
        if type(self.method) == int:
            for i in range(self.method):
                shuffle(shoe_list)
        elif self.method == 'part_1':
            self.shuffle_1(shoe, shoe_list)
        elif self.method == 'part_2':
            self.shuffle_2(shoe, shoe_list)
        elif self.method == 'casino':
            self.entire_shuffle(shoe, shoe_list)
        else:
            self.method == 'none'


    def partition(self, cards, num):
        """Given a list of cards, split the cards into groups of
        num cards, where each group is a list in a list of lists.
        """

        self.group = []

        for i in range(0, len(cards), num):
            new_group = cards[i:i + num]
            self.group.append(new_group)


    def flatten_list(self, list, new_list):
        "Given a list of lists, flatten all elements into one list."

        for x in list:
            for y in x:
                new_list.append(y)


    def riffle_cards(self, pile_1, pile_2):
        """For two piles of cards, alternate between the two piles,
        appending one card from each pile until there are no more cards.
        """

        self.riffle = []

        index = 0
        while index < len(pile_1):
            self.riffle.append(pile_1[index])
            self.riffle.append(pile_2[index])
            index +=1


    def strip_cards(self, pile):
        "Partition the pile into sections, and then reverse the sections."

        self.strip = []
        self.partition(pile, self.strip_len)
        self.group = self.group[::-1]

        for x in self.group:
            for y in x:
                self.strip.append(y)


    def riffle_strip_riffle(self, pile_1, pile_2):
        "Perform riffle-strip-riffle, and then append cards to middle pile."

        # Riffle
        self.riffle_cards(pile_1, pile_2)

        # Strip
        self.strip_cards(self.riffle)

        # Split pile into two equal piles and riffle again
        self.partition(self.strip, self.pile_len)
        self.riffle_cards(self.group[0], self.group[1])

        # Place shuffled cards in middle pile
        self.middle.append(self.riffle)


    def middle_pile(self, pile):
        "Take cards from the middle pile to reshuffle."

        # Select top partition of middle pile
        self.group.clear()
        self.partition(self.middle[0], self.pile_len)

        # Remove cards in top partition
        for card in self.group[0]:
            self.middle[0].remove(card)

        # Shuffle the middle partiton with one of the side pile partitions
        self.riffle_strip_riffle(pile, self.group[0])

        # Reverse the middle pile so that the cards shuffled are on the bottom
        self.middle = self.middle[::-1]


    def clear_shuffle(self, shoe):
        "Clear the lists that are needed to perform the shuffle."

        lists = [self.group, self.riffle, self.pile_1, self.pile_2,
        self.strip, self.middle, shoe.shuffled_cards]

        for list in lists:
            list.clear()


    def start_shuffle(self, shoe, shoe_list):
        "Procedure for starting a shuffle."

        # Split shoe into two equal piles
        self.partition(shoe_list, self.half)
        top_half = self.group[0]
        bottom_half = self.group[1]

        # Take 3/4 of a deck at a time from each half
        self.partition(top_half, self.pile_len)
        self.pile_1 = self.group
        self.partition(bottom_half, self.pile_len)
        self.pile_2 = self.group

        # Shuffle until there are no more partitions
        self.shuffle_until = len(self.pile_1)


    def finish_shuffle(self, shoe):
        "Procedure for finishing a shuffle."

        # Flatten lists of lists and add to shuffled_cards
        self.flatten_list(self.middle, shoe.shuffled_cards)

        # Check card count
        expected = shoe.num
        shoe.count_cards(shoe.shuffled_cards)
        for count in shoe.card_count.values():
            if count == expected:
                self.error = False
            else:
                self.error = True

        # If all of the cards are there, use the list of shuffled cards
        if self.error == False:
            shoe.return_shoe = shoe.shuffled_cards


    def shuffle_part_1(self, shoe, shoe_list):
        """Divide the cards into two equal piles and take cards from the
        two side piles, shuffle, and place the cards in the middle pile.
        Then shuffle the cards from the middle pile with a side pile,
        alternating between the left and right piles.
        """

        # Start the shuffle
        self.start_shuffle(shoe, shoe_list)

        # Shuffle both piles together and add to middle
        self.riffle_strip_riffle(self.pile_1[0], self.pile_2[0])

        i = 1
        # Alternate between pile_1 and pile_2
        while i < self.shuffle_until:
            self.middle_pile(self.pile_1[i])
            self.middle_pile(self.pile_2[i])
            i +=1

        # Finish the shuffle
        self.finish_shuffle(shoe)


    def shuffle_part_2(self, shoe, shoe_list):
        """Divide the cards into two equal piles and take cards from
        the two side piles, shuffle, and place the cards in the middle.
        Repeat this procedure until all of the cards have been shuffled.
        """

        # Start the shuffle
        self.start_shuffle(shoe, shoe_list)

        i = 0
        # Shuffle 1 1/2 decks at a time using riffle_strip_riffle
        while i < self.shuffle_until:
            self.riffle_strip_riffle(self.pile_1[i], self.pile_2[i])
            i +=1

        # Finish the shuffle
        self.finish_shuffle(shoe)


    def entire_shuffle(self, shoe, shoe_list):
        "Shuffle using part_1 and then part_2."

        # For part_2, clear the cards from part_1
        if shoe.shuffled_cards != []:
            middle_1 = shoe.shuffled_cards.copy()
            self.clear_shuffle(shoe)
            self.shuffle_part_1(shoe, middle_1)
        else:
            self.shuffle_part_1(shoe, shoe_list)

        # Create a middle_2 to hold the cards from part_1
        middle_2 = shoe.shuffled_cards.copy()
        self.clear_shuffle(shoe)
        self.shuffle_part_2(shoe, middle_2)


    def shuffle_1(self, shoe, shoe_list):
        "If the shuffle method = 'part_1', use shuffle_1."

        # Clear the cards from the previous shoe
        if shoe.shuffled_cards != []:
            new_middle = shoe.shuffled_cards.copy()
            self.clear_shuffle(shoe)
            self.shuffle_part_1(shoe, new_middle)
        else:
            self.shuffle_part_1(shoe, shoe_list)


    def shuffle_2(self, shoe, shoe_list):
        "If the shuffle method = 'part_2, use shuffle_2.'"

        # Clear the cards from the previous shoe
        if shoe.shuffled_cards != []:
            new_middle = shoe.shuffled_cards.copy()
            self.clear_shuffle(shoe)
            self.shuffle_part_2(shoe, new_middle)
        else:
            self.shuffle_part_2(shoe, shoe_list)
