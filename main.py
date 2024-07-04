from BlackjackProbabilityCalculator import *
from ProbabilityFunctions import *
import pandas as pd
import time

if __name__ == "__main__":
    blackjack = BlackjackProbabilityCalculator()
    
    dealer_upcards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
    
    # Print the dataframes
    print("\nOverall Dealer Probability Distribution:\n", create_dealer_prob_dist_table(dealer_upcards))
    print("\nProbabilities for the dealer's results conditioned on the dealer's first card:\n", create_dealer_prob_table(dealer_upcards))
    print("\nExpectations, conditioned on the dealer's first card, for the player's profit, when the player stands:\n", create_stand_EV_table(dealer_upcards))
    print("\nExpectations, conditioned on the dealer's first card, for the player's profit, when the player hits:\n", create_hit_EV_table(dealer_upcards))
    print("\nExpectations, conditioned on the dealer's first card, for the player's profit, when the player hits with a soft hand:\n", create_soft_hit_EV_table(dealer_upcards))
    print("\nExpectations, conditioned on the dealer's first card, for the player's profit, when the player plays optimally:\n", create_optimal_values_table(dealer_upcards))
    print("\nExpectations, conditioned on the dealer's first card, for the player's profit, when the player plays optimally and has a soft hand\n", create_soft_optimal_values_table(dealer_upcards))
    print("\nOptimal Move Chart:\n", create_optimal_table(dealer_upcards))
    print("\nOptimal Soft Move Chart:\n", create_soft_optimal_table(dealer_upcards))