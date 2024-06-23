from Hand import *
import random
import copy

def remove_used_cards(items: list, items_to_remove: list):
    for i in range(len(items) - 1, -1, -1):
        if items[i] in items_to_remove:
            del items[i]

def single_simulation(player_hand_value: int, deck_list: list, dealer_hand: Hand) -> str: # only used with monte_carlo_simulation 
    random.shuffle(deck_list)
    dealt_cards = []
    while dealer_hand.value() < 17:
        card = deck_list.pop()
        dealt_cards.append(card)
        dealer_hand.add_card(card)
    value = dealer_hand.value()
    deck_list += dealt_cards
    
    if (value < player_hand_value) or dealer_hand.is_bust():
        remove_used_cards(dealer_hand.cards, dealt_cards)
        return 'l'
    elif value > player_hand_value:
        remove_used_cards(dealer_hand.cards, dealt_cards)
        return 'w'
    else:
        remove_used_cards(dealer_hand.cards, dealt_cards)
        return 't'