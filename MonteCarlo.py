from Blackjack import *
import random
import decimal

def dealer_action(dealer_upcard: int) -> int:
    """
    Perform the dealer's actions according to the game rules and return the dealer's final hand value.
    Intended for Monte Carlo functions.
    """
    dealer_hand = [dealer_upcard]
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    
    # Dealer draws cards until the hand value is at least 17
    while sum(dealer_hand) < 17:
        dealer_hand.append(random.choice(deck))
        
        # Handle soft aces during drawing
        while sum(dealer_hand) > 21 and 11 in dealer_hand:
            dealer_hand[dealer_hand.index(11)] = 1

    return sum(dealer_hand)

def monte_carlo_stand(simulations: int, player_hand_value: int, dealer_upcard: int) -> decimal.Decimal:
    """
    Simulate the outcome of standing in blackjack through Monte Carlo simulation.
    5 million simulations take about 15 seconds.
    """
    wins, losses = 0, 0
    
    for _ in range(simulations):
        dealer_value = dealer_action(dealer_upcard)
        
        if player_hand_value > 21:
            losses += 1
        elif dealer_value > 21 or dealer_value < player_hand_value:
            wins += 1
        elif dealer_value > player_hand_value:
            losses += 1
    
    return decimal.Decimal(wins - losses) / decimal.Decimal(simulations)

def monte_carlo_hit(simulations: int, player_hand: list, dealer_upcard: int) -> decimal.Decimal:
    """
    Simulate the outcome of hitting in blackjack through Monte Carlo simulation.
    """
    wins, losses = 0, 0
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    
    for _ in range(simulations):
        # Copy the player's hand to avoid modifying the original
        current_hand = player_hand[:]
        current_hand.append(random.choice(deck))
        player_hand_value = sum(current_hand)
        
        # Handle soft aces in the player's hand
        while player_hand_value > 21 and 11 in current_hand:
            current_hand[current_hand.index(11)] = 1
            player_hand_value = sum(current_hand)
        
        dealer_value = dealer_action(dealer_upcard)
        
        if player_hand_value > 21:
            losses += 1
        elif dealer_value > 21 or dealer_value < player_hand_value:
            wins += 1
        elif dealer_value > player_hand_value:
            losses += 1
    
    return decimal.Decimal(wins - losses) / decimal.Decimal(simulations)