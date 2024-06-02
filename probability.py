from Card import *
from hand_evaluation import *

def chance_of_bust(dealer_card, player_hand):
    used_cards = player_hand + [dealer_card]
    score_to_bust = 21 - hand_evaluation(player_hand)
    if score_to_bust > 11:
        return 0
    num_bust_cards = (13 - score_to_bust) * 4
    for card in used_cards:
        if card_value(card.rank) > score_to_bust:
            num_bust_cards -= 1
    return round(num_bust_cards / (52 - len(used_cards)), 3)
