from BlackjackProbabilityCalculator import *
import unittest

class TestCard(unittest.TestCase):
    
    def setUp(self):
        self.card1 = Card('A', 'S')
        self.card2 = Card('5', 'D')
        self.card3 = Card('A', 'S')

    def test_card_creation(self):
        self.assertEqual(self.card1.rank, 'A')
        self.assertEqual(self.card1.suit, 'S')
        self.assertEqual(self.card2.rank, '5')
        self.assertEqual(self.card2.suit, 'D')

    def test_value(self):
        self.assertEqual(self.card1.value(), 11)
        self.assertEqual(self.card2.value(), 5)

    def test_equality(self):
        self.assertEqual(self.card1, self.card3)

    def test_str(self):
        self.assertEqual("AS", str(self.card1))
        self.assertNotEqual(str(self.card1), str(self.card2))


class TestDeck(unittest.TestCase):

    def setUp(self):
        self.deck = Deck()
        self.suits = ("S", "C", "H", "D")
        self.ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K")

    def test_deck_initialization(self):
        self.assertEqual(len(self.deck.list), 52)
        test_set = set()
        for suit in self.suits:
            for rank in self.ranks:
                test_set.add(Card(rank, suit))
        self.assertEqual(test_set, set(self.deck.list))

    def test_size(self):
        self.assertEqual(len(self.deck.list), self.deck.size())   

    def test_shuffle(self):
        initial_deck = self.deck.list[:]
        self.deck.shuffle()
        self.assertNotEqual(initial_deck, self.deck.list)

class TestHand(unittest.TestCase):

    def setUp(self):
        self.hand = Hand()

if __name__ == "__main__":
    unittest.main()