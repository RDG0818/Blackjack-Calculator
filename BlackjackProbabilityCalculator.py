from Hand import *
from Deck import *
from Player import *

class BlackjackProbabilityCalculator:
    def __init__(self) -> None:
        self.deck = Deck()
        self.dealer = Player("Dealer")
        self.player = Player("Player")

    def get_card(self, name: str) -> Card:
        while True:
            rank = input(f"{name}'s card rank: ")
            while rank not in self.deck.ranks:
                rank = input("Enter a valid rank (A, 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K): ")
            suit = input(f"{name}'s card suit: ")
            while suit not in self.deck.suits:
                suit = input("Enter a valid suit (S, C, H, D): ")
            curr_card = Card(rank, suit)
            if curr_card not in self.deck.list:
                print("Card already chosen. Enter a different card.")
                continue
            self.deck.remove_card(curr_card)
            return curr_card
    
    def get_initial_hands(self) -> None:
        dealer_card = self.get_card("Dealer")
        self.dealer.hand.add_card(dealer_card)
        input_num = input("Cards in hand: ")
        while not input_num.isdigit():
            input_num = input("Enter a number: ")
        input_num = int(input_num)
        for _ in range(input_num):
            player_card = self.get_card("Player")
            self.player.hand.add_card(player_card)

    def play_dealer_hand(self) -> None:
        while self.dealer.hand_value < 17:
            self.dealer.hit(self.deck)

    
    def chance_of_bust(self):
        num_bust_cards = 0
        for card in self.deck.list:
            temp_hand = Hand(self.player.hand.cards + [card])
            if temp_hand.value() > 21:
                num_bust_cards += 1
        return round(num_bust_cards / self.deck.size(), 3)

    
    