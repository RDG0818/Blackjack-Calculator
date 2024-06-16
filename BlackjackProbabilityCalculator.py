from Hand import *
from Deck import *
from Player import *
import copy
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from single_simulation import single_simulation

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
    
    def chance_of_bust(self):
        num_bust_cards = 0
        for card in self.deck.list:
            temp_hand = Hand(self.player.hand.cards + [card])
            if temp_hand.value() > 21:
                num_bust_cards += 1
        return round(num_bust_cards / self.deck.size(), 3)

    def sequential_monte_carlo_simulation(self, num_of_times: int) -> tuple:
        wins = 0
        losses = 0
        ties = 0
        player_hand_value = self.player.hand_value()
        for _ in range(num_of_times):
            self.deck.shuffle()
            copy_list = self.deck.list[:]
            copy_dealer_hand = copy.deepcopy(self.dealer.hand)
            while copy_dealer_hand.value() < 17:
                copy_dealer_hand.add_card(copy_list.pop())
            if (copy_dealer_hand.value() < player_hand_value) or copy_dealer_hand.is_bust():
                losses += 1
            elif copy_dealer_hand.value() > self.player.hand_value():
                wins += 1
            else:
                ties += 1
        return (wins / num_of_times, losses / num_of_times, ties / num_of_times)

    def parallelized_monte_carlo_simulation(self, num: int) -> tuple:
        player_hand_value = self.player.hand_value()
        deck_list = self.deck.list[:]
        dealer_hand = self.dealer.hand

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(single_simulation, [player_hand_value] * num, [deck_list] * num, [dealer_hand] * num))     
        wins = 0
        losses = 0
        ties = 0
        for s in results:
            if (s == 'w'):
                wins += 1
            elif (s == 'l'):
                losses += 1
            else:
                ties += 1
        return (wins / num, losses / num, ties / num)
        