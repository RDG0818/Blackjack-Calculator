from Hand import *
import random
import copy

def single_simulation(player_hand_value: int, deck_list: list, dealer_hand: Hand) -> str: # only used with monte_carlo_simulation 
    random.shuffle(deck_list)
    copy_list = deck_list[:]
    copy_dealer_hand = copy.deepcopy(dealer_hand)
    while copy_dealer_hand.value() < 17:
        copy_dealer_hand.add_card(copy_list.pop())
    if (copy_dealer_hand.value() < player_hand_value) or copy_dealer_hand.is_bust():
        return 'l'
    elif copy_dealer_hand.value() > player_hand_value:
        return 'w'
    else:
        return 't'