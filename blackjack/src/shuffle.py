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
        if self.method == 'computer':
            shuffle(shoe_list)
        elif self.method == 'riffle_perfect':
            self.dealer_shuffle(shoe, shoe_list, 'perfect')
        elif self.method == 'riffle_clumpy':
            self.dealer_shuffle(shoe, shoe_list, 'clumpy')
        else:
            print("Error! Please enter a shuffle method")


    def dealer_shuffle(self, shoe, shoe_list, riffle):
        """Follows the pattern of riffle-strip-riffle, where riffle can
        take the values of perfect (loops through one card from each pile),
        or clumpy (cards from each pile are taken at a random distribution).
        """

        def partition(cards, num):
            """Given a list of cards, split the cards into groups of
            num cards, where each group is a list in a list of lists."""

            self.group = []
            for i in range(0, len(cards), num):
                new_group = cards[i:i + num]
                self.group.append(new_group)


        def flatten_list(list, new_list):
            "Given a list of lists, flatten all elements into one list."

            for x in list:
                for y in x:
                    new_list.append(y)


        def riffle_perfect(pile_1, pile_2):
            """For two piles of cards, alternate between the two piles,
            appending one card from each pile until there are no more cards.
            """

            self.riffle = []
            n = iter(pile_2)

            # Iterate through pile_1 and append next of pile_2
            for i in iter(pile_1):
                self.riffle.append(i)
                self.riffle.append(next(n))


        def riffle_clumpy(pile_1, pile_2):
            """For two piles of cards, use a random distribution
            to alternate between the two piles in order to create a clumpy
            riffle."""

            self.riffle = []
            riffle = []

            # Create a random distribution
            dist = [12,10,8,6,4,2,2,2,1,1,1,1]
            shuffle(dist)
            dist_iter = iter(dist)

            # Iterate through pile_1
            for i in iter(pile_1):
                # Use next(dist) to find how many cards to take from pile_1
                take = next(dist_iter)
                cards = pile_1[0:take]
                riffle.append(cards)
                # Remove cards from pile_1
                for card in cards:
                    pile_1.remove(card)
                # Use next(dist) to find how many cards to take from pile_2
                take_2 = next(dist_iter)
                cards_2 = pile_2[0:take_2]
                riffle.append(cards_2)
                # Remove cards from pile_2
                for card in cards_2:
                    pile_2.remove(card)

            # Flatten the list of cards
            self.flatten_list(riffle, self.riffle)


        def strip_cards(pile):
            "Partition the pile into sections, and then reverse the sections."

            self.strip = []
            partition(pile, self.strip_len)
            self.group = self.group[::-1]

            for x in self.group:
                for y in x:
                    self.strip.append(y)


        def riffle_strip_riffle(pile_1, pile_2, riffle):
            "Perform riffle-strip-riffle, and then append cards to middle pile."

            # Riffle
            if riffle == 'perfect':
                riffle_perfect(pile_1, pile_2)
            else:
                riffle_clumpy(pile_1, pile_2)

            # Strip
            strip_cards(self.riffle)
            partition(self.strip, self.pile_len)

            # Riffle
            if riffle == 'perfect':
                riffle_perfect(self.group[0], self.group[1])
            else:
                riffle_clumpy(self.group[0], self.group[1])

            # Place shuffled cards in middle pile
            self.middle.append(self.riffle)


        def middle_pile(pile, riffle):
            "Take cards from the middle pile to reshuffle."

            # Select top partition of middle pile
            self.group.clear()
            partition(self.middle[0], self.pile_len)

            # Remove cards in top partition
            for card in self.group[0]:
                self.middle[0].remove(card)

            # Shuffle the middle partiton with one of the side pile partitions
            riffle_strip_riffle(pile, self.group[0], riffle)

            # Reverse the middle pile so that the cards shuffled are on the bottom
            self.middle = self.middle[::-1]


        def clear_shuffle(shoe):
            "Clear the lists that are needed to perform the shuffle."

            lists = [self.group, self.riffle, self.pile_1, self.pile_2,
                    self.strip, self.middle, shoe.shuffled_cards]

            for list in lists:
                list.clear()


        # Start shuffle
        # Split shoe into two equal piles
        partition(shoe_list, self.half)
        top_half = self.group[0]
        bottom_half = self.group[1]

        # Take 3/4 of a deck at a time from each half
        partition(top_half, self.pile_len)
        self.pile_1 = self.group
        partition(bottom_half, self.pile_len)
        self.pile_2 = self.group

        # Shuffle until there are no more partition
        self.shuffle_until = len(self.pile_1)

        # Shuffle both piles together and add to middle
        riffle_strip_riffle(self.pile_1[0], self.pile_2[0], riffle)

        # Alternate between pile_1 and pile_2
        i = 1
        while i < self.shuffle_until:
            middle_pile(self.pile_1[i], riffle)
            middle_pile(self.pile_2[i], riffle)
            i +=1

        # Flatten lists of lists and add to shuffled_cards
        flatten_list(self.middle, shoe.shuffled_cards)

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
        else:
            print("Error! You didn't shuffle through all of the cards")
