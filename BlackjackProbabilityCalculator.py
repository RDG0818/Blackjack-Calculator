from Hand import *
from Deck import *
from Player import *
import copy
from concurrent.futures import ThreadPoolExecutor

class BlackjackProbabilityCalculator:
    def __init__(self) -> None:
        self.deck = Deck()
        self.dealer = Player("Dealer")
        self.player = Player("Player")

    def get_card_from_input(self, player_name: str) -> Card:
        """Prompt the user to input a card rank and return a valid Card object."""
        while True:
            rank = input(f"{player_name}'s card rank: ").upper()
            while rank not in self.deck.ranks:
                rank = input("Enter a valid rank (A, 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K): ").upper()
            card = Card(rank)
            if card not in self.deck.list:
                print("Card already chosen. Enter a different card.")
                continue
            self.deck.remove_card(card)
            return card

    def get_initial_hands(self) -> None:
        """Initialize the dealer's and player's hands by prompting for their cards."""
        dealer_card = self.get_card_from_input("Dealer")
        self.dealer.hand.add_card(dealer_card)

        num_cards = input("Number of cards in player's hand: ")
        while not num_cards.isdigit():
            num_cards = input("Enter a valid number: ")
        num_cards = int(num_cards)

        for _ in range(num_cards):
            player_card = self.get_card_from_input("Player")
            self.player.hand.add_card(player_card)

    def dealer_action(self) -> int:
        """Perform the dealer's actions according to the game rules and return the dealer's final hand value. Intended for monte_carlo functions."""
        self.deck.shuffle()
        dealt_cards = []

        # Dealer draws cards until the hand value is at least 17
        while self.dealer.hand_value() < 17:
            card = self.deck.deal_card()
            dealt_cards.append(card)
            self.dealer.hand.add_card(card)

        dealer_value = self.dealer.hand_value()

        # Return the dealt cards to the deck
        self.deck.list.extend(dealt_cards)
        
        # Remove dealt cards from the dealer's hand
        self.dealer.hand.cards = [card for card in self.dealer.hand.cards if card not in dealt_cards]

        return dealer_value
    
    def monte_carlo_stand(self, simulations: int) -> tuple:
        """Simulate the outcome of standing in blackjack through Monte Carlo simulation. 1 million simulations takes about 15 seconds."""
        wins, losses, ties = 0, 0, 0
        player_hand_value = self.player.hand_value()
        
        for _ in range(simulations):
            dealer_value = self.dealer_action()
            
            if player_hand_value > 21:
                losses += 1
            elif dealer_value > 21 or dealer_value < player_hand_value:
                wins += 1
            elif dealer_value > player_hand_value:
                losses += 1
            else:
                ties += 1
        
        total_simulations = simulations
        win_probability = wins / total_simulations
        loss_probability = losses / total_simulations
        tie_probability = ties / total_simulations
        
        return win_probability, loss_probability, tie_probability
    
    def monte_carlo_hit(self, simulations: int) -> tuple:
        """Simulate the outcome of hitting in blackjack through Monte Carlo simulation. 1 million simulations takes about 25 seconds."""
        wins, losses, ties = 0, 0, 0
        
        for _ in range(simulations):
            self.deck.shuffle()
            
            # Deal a card to the player and add it to their hand
            card = self.deck.deal_card()
            dealt_cards = [card]
            self.player.hand.add_card(card)
            
            player_hand_value = self.player.hand_value()
            dealer_value = self.dealer_action()
            
            # Return dealt card to the deck and remove from player's hand
            self.deck.list += dealt_cards
            self.player.hand.cards.remove(card)
            
            # Determine the outcome
            if player_hand_value > 21:
                losses += 1
            elif dealer_value > 21 or dealer_value < player_hand_value:
                wins += 1
            elif dealer_value > player_hand_value:
                losses += 1
            else:
                ties += 1
    
        total_simulations = simulations
        win_probability = wins / total_simulations
        loss_probability = losses / total_simulations
        tie_probability = ties / total_simulations
    
        return win_probability, loss_probability, tie_probability

