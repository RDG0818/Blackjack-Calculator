from Card import *

suits = ["S", "C", "H", "D"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
deck = []
for suit in suits:
    for rank in ranks:
        deck.append(Card(rank, suit))
dict_deck = {rank: 4 for rank in ranks}

def card_value(rank):
    if rank in "23456789":
        return int(rank)
    elif rank in "TJQK":
        return 10
    elif rank == "A":
        return 11
    return 0

def hand_evaluation(hand):
    score = 0
    num_aces = 0
    for card in hand:
        score += card_value(card.rank)
        if card.rank == "A":
            num_aces += 1
    while score > 21 and num_aces > 0:
        score -= 10
        num_aces -= 1
    return score

def dealer_input():
    dealer_rank = input("Enter the dealer's card rank (A, 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K): ")
    while (dealer_rank not in ranks):
        dealer_rank = input("Enter a valid rank (A, 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K): ")
    dealer_suit = input("Enter the dealer card suit (S C H D): ")
    while (dealer_suit not in suits):
        dealer_suit = input("Enter a valid suit (S C H D): ")
    dealer_card = Card(dealer_rank, dealer_suit)
    deck.remove(dealer_card)
    return dealer_card

def player_card_input(i):
    card_rank = input(f"Enter the rank of card {i + 1} (A, 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K): ")
    while (card_rank not in ranks):
        card_rank = input("Enter a valid rank (A, 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K): ")
    card_suit = input(f"Enter the suit of card {i + 1} (S C H D): ")
    while (card_suit not in suits):
        card_suit = input("Enter a valid suit (S C H D): ")
    return Card(card_rank, card_suit)

def create_hand():
    hand = []
    num_cards = input("Enter the amount of cards in your hand: ")
    while (not num_cards.isdigit()):
        num_cards = input("Enter a valid number: ")
    num_cards = int(num_cards)
    for i in range(num_cards):
        temp_card = player_card_input(i)
        while (temp_card not in deck):
            print("Card already selected")
            temp_card = player_card_input(i)
        hand.append(temp_card)
        deck.remove(temp_card)
    return hand

def chance_of_bust(dealer_card, player_hand):
    num_bust_cards = 0
    for card in deck:
        temp_hand = player_hand + [card]
        if hand_evaluation(temp_hand) > 21:
            num_bust_cards += 1
    return round(num_bust_cards / (len(deck)), 3)
