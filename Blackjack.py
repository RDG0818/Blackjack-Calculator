from Card import Card
from Hand import Hand
from Deck import Deck
from Player import Player

class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.dealer = Player("Dealer")
        self.player = Player("Player")
    
    def start_game(self):
        """Start a new game of blackjack."""
        self.deck.shuffle()
        self.dealer.hand.clear()
        self.player.hand.clear()
        self.get_initial_hands()
        self.display_hands(initial=True)
        
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

    def get_initial_hands(self):
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

    def deal_card(self, player: Player):
        """Deal a card to a player from the deck."""
        card = self.deck.draw_card()
        player.hand.add_card(card)
        return card

    def player_turn(self):
        """Handle the player's turn."""
        while True:
            action = input("Choose action: [h]it, [s]tand: ").lower()
            if action == 'h':
                self.deal_card(self.player)
                self.display_hands()
                if self.player.hand.value() > 21:
                    print("Player busts!")
                    break
            elif action == 's':
                print("Player stands.")
                break

    def dealer_turn(self):
        """Handle the dealer's turn."""
        while self.dealer.hand.value() < 17:
            self.deal_card(self.dealer)
        self.display_hands()

    def evaluate_hands(self):
        """Evaluate and display the result of the game."""
        player_value = self.player.hand.value()
        dealer_value = self.dealer.hand.value()

        if player_value > 21:
            result = "Player busts! Dealer wins!"
        elif dealer_value > 21 or player_value > dealer_value:
            result = "Player wins!"
        elif player_value < dealer_value:
            result = "Dealer wins!"
        else:
            result = "Push! It's a tie!"

        print(result)

    def display_hands(self, initial=False):
        """Display the current hands of player and dealer."""
        print("\nDealer's hand:")
        if initial:
            print(f"{self.dealer.hand.cards[0]} [hidden]")
        else:
            print(self.dealer.hand)

        print("\nPlayer's hand:")
        print(self.player.hand)
        print()

    def play_game(self):
        """Play a round of blackjack."""
        self.start_game()
        self.player_turn()
        if self.player.hand.value() <= 21:
            self.dealer_turn()
        self.evaluate_hands()

# To use the class, create an instance and call play_game()
# game = Blackjack()
# game.play_game()