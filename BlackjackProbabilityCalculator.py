from Hand import *
from Deck import *
from Player import *
import copy
from concurrent.futures import ThreadPoolExecutor
from single_simulation import single_simulation

class BlackjackProbabilityCalculator:
    def __init__(self) -> None:
        self.deck = Deck()
        self.dealer = Player("Dealer")
        self.player = Player("Player")
        self.soft_17 = False

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
    
    def sequential_stand(self, num: int) -> tuple: # Finds probability chance of winning/losing/tieing through Monte Carlo Simulation
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
    
    def sequential_single_hit(self, num: int) -> tuple:
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

            