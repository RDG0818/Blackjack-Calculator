from Card import *

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
