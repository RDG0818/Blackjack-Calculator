from Card import *

def dealer_input():
    dealer_rank = input("Enter the dealer's card rank: ")
    dealer_suit = input("Enter the dealer card suit: ")
    dealer_card = Card(dealer_rank, dealer_suit)
    return dealer_card

def player_input():
    hand = []
    num_cards = int(input("Enter the amount of cards in your hand: "))
    for i in range(num_cards):
        card_rank = input(f"Enter the rank of card {i}: ")
        card_suit = input(f"Enter the suit of card {i}: ")
        hand.append(Card(card_rank, card_suit))
    return hand
