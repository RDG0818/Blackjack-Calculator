from Hand import *
from Deck import *
from Player import *
import copy
from concurrent.futures import ThreadPoolExecutor
from single_simulation import single_simulation
from collections import Counter
from math import factorial
import pandas as pd

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
            curr_card = Card(rank)
            if curr_card not in self.deck.list:
                print("Card already chosen. Enter a different card.")
                continue
            self.deck.remove_card(curr_card)
            return curr_card
    
    def get_rules(self):
        rules = {}

        rules['dealer_hits_soft_17'] = input("Does the dealer hit on a soft 17? (yes/no): ").strip().lower() == 'yes'
        rules['double_down_allowed'] = input("Is double down allowed? (yes/no): ").strip().lower() == 'yes'
        if rules['double_down_allowed']:
            rules['double_down_on_any_two_cards'] = input("Can you double down on any two cards? (yes/no): ").strip().lower() == 'yes'
            rules['double_down_after_splitting'] = input("Can you double down after splitting? (yes/no): ").strip().lower() == 'yes'

        rules['splitting_allowed'] = input("Is splitting allowed? (yes/no): ").strip().lower() == 'yes'
        if rules['splitting_allowed']:
            rules['resplit_aces'] = input("Can you resplit Aces? (yes/no): ").strip().lower() == 'yes'
            rules['max_splits'] = int(input("What is the maximum number of splits allowed?: "))

        rules['surrender_allowed'] = input("Is surrendering allowed? (yes/no): ").strip().lower() == 'yes'
        if rules['surrender_allowed']:
            rules['early_surrender'] = input("Is it early surrender? (yes/no): ").strip().lower() == 'yes'

        rules['blackjack_payout'] = input("What is the payout for a natural Blackjack? (3:2 or 6:5): ").strip()

        rules['number_of_decks'] = int(input("How many decks are used in the game?: "))
        self.deck = Deck(rules['number_of_decks'])

        rules['insurance_offered'] = input("Is insurance offered when the dealer shows an Ace? (yes/no): ").strip().lower() == 'yes'
        if rules['insurance_offered']:
            rules['insurance_payout'] = input("What is the payout for insurance? (typically 2:1): ").strip()

        rules['even_money_offered'] = input("If you have a Blackjack and the dealer shows an Ace, is even money offered? (yes/no): ").strip().lower() == 'yes'

        return rules

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

    def player_hand_min_11(self) -> None: # Checks if player hand is less than 11. If it is, it automatically adds another card.
        while self.player.hand_value < 11:
            self.player.hit(self.deck)

    def chance_of_bust(self):
        num_bust_cards = 0
        for card in self.deck.list:
            temp_hand = Hand(self.player.hand.cards + [card])
            if temp_hand.value() > 21:
                num_bust_cards += 1
        return round(num_bust_cards / self.deck.size(), 3)

    def dealer_action(self):
        self.deck.shuffle()
        dealt_cards = []
        while self.dealer.hand_value() < 17:
            card = self.deck.deal_card()
            dealt_cards.append(card)
            self.dealer.hand.add_card(card)
        dealer_value = self.dealer.hand_value()
        self.deck.list += dealt_cards
        for i in range(len(self.dealer.hand.cards) - 1, -1, -1):
            if self.dealer.hand.cards[i] in dealt_cards:
                del self.dealer.hand.cards[i]
        return dealer_value
    
    def monte_carlo_stand(self, num: int) -> tuple: # Finds probability chance of winning/losing/tieing through Monte Carlo Simulation
        wins = losses = ties = 0
        player_hand_value = self.player.hand_value()
        for _ in range(num):
            dealer_value = self.dealer_action()
            if player_hand_value > 21:
                losses += 1
            elif dealer_value > 21:
                wins += 1
            elif dealer_value > player_hand_value:
                losses += 1
            elif dealer_value < player_hand_value:
                wins += 1
            else:
                ties += 1
        return (wins / num, losses / num, ties / num)

    def parallelized_stand(self, num: int) -> tuple: # Similar to sequential_stand but it utilizes multithreading 
        player_hand_value = self.player.hand_value()
        deck_list = self.deck.list[:]
        dealer_hand = self.dealer.hand

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(single_simulation, [player_hand_value] * num, [deck_list] * num, [dealer_hand] * num)) 

        wins = losses = ties = 0
        for s in results:
            if (s == 'w'):
                wins += 1
            elif (s == 'l'):
                losses += 1
            else:
                ties += 1
        return (wins / num, losses / num, ties / num)
    
    def monte_carlo_hit(self, num: int) -> tuple:
        wins = losses = ties = 0
        for _ in range(num):
            self.deck.shuffle()
            card = self.deck.deal_card()
            dealt_cards = [card]
            self.player.hand.add_card(card)
            player_hand_value = self.player.hand_value()
            dealer_value = self.dealer_action()
            self.deck.list += dealt_cards
            self.player.hand.cards.remove(dealt_cards[0])
            if player_hand_value > 21:
                losses += 1
            elif dealer_value > 21:
                wins += 1
            elif dealer_value > player_hand_value:
                losses += 1
            elif dealer_value < player_hand_value:
                wins += 1
            else:
                ties += 1
        return (wins / num, losses / num, ties / num)

    def get_combinations(self, target: int) -> list: 
        def backtracking(start: int, target: int, path: list, result: list):
            if target == 0:
                result.append(path[:])
                return
            if target < 0:
                return
            for i in range(start, 12):
                path.append(i)
                backtracking(i, target - i, path, result)
                path.pop()
        result = []
        backtracking(1, target, [], result)
        return result

    def probability_distribution(self, dealer_upcard = None) -> dict: 
        def backtracking(path: list, result: dict):
            # Handle the conversion of a soft ace (11) to a hard ace (1) if it prevents busting
            if 11 in path and sum(path) >= 22:
                path = path[:]
                path[path.index(11)] = 1

            # Calculate probabilities and update the result dictionary
            total = sum(path)
            if total >= 17:
                total_probability = 1
                start = 0 if dealer_upcard == None else 1
                for i in range(start, len(path)):
                    total_probability *= (1/13) if path[i] != 10 else (4/13)
                if (len(path) == 2) and (10 in path) and (11 in path):
                    result["blackjack"] += total_probability
                elif total <= 21:
                    result[total] += total_probability
                else:
                    result["bust"] += total_probability
                return
            
            # Recursively explore the next possible card values
            for i in range(2, 12):
                path.append(i)
                backtracking(path, result)
                path.pop()

        # Initialize the result dictionary
        result = {num : 0 for num in range(17, 22)}
        result["bust"] = 0
        result["blackjack"] = 0

        # Start the backtracking process
        if dealer_upcard:
            backtracking([dealer_upcard], result)
        else:
            backtracking([], result)
        return result

    def stand_EV(self, num):
        probabilities = self.probability_distribution(num)
        stand_EV = {"blackjack" : 0, 21 : 0, 20 : 0, 19 : 0, 18 : 0, 17 : 0, "<=16" : 0}
        for player in stand_EV.keys():
            if player == "blackjack":
                for value, prob in probabilities.items():
                    if (value != "blackjack"):
                        stand_EV[player] += prob
                stand_EV[player] *= 1.5
            elif player == "<=16":
                for value, prob in probabilities.items():
                    if (value != "bust"):
                        stand_EV[player] -= prob
                    else:
                        stand_EV[player] += prob
            else:
                for value, prob in probabilities.items():
                    if (value == "blackjack"):
                        stand_EV[player] -= prob
                    elif (value == "bust"):
                        stand_EV[player] += prob
                    elif (value < player):
                        stand_EV[player] += prob
                    elif (value > player):
                        stand_EV[player] -= prob
        return stand_EV
