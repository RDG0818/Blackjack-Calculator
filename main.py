from BlackjackProbabilityCalculator import *
from ProbabilityFunctions import *
import pandas as pd
import time

if __name__ == "__main__":
    blackjack = BlackjackProbabilityCalculator()
    blackjack.get_initial_hands()
    start = time.time()
    print(blackjack.monte_carlo_hit(1000000))
    end = time.time()
    print("Time:", end - start, "seconds")
    # dealer_upcards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
    
    # # Initialize dictionaries to store results
    # probability_distributions = {}
    # stand_expected_values = {}
    # hit_expected_values = {}
    
    # # Calculate distributions and expected values for each dealer upcard
    # for upcard in dealer_upcards:
    #     upcard_value = 11 if upcard == 'A' else int(upcard)
    #     probability_distributions[upcard] = blackjack.probability_distribution(upcard_value)
    #     stand_expected_values[upcard] = blackjack.stand_EV(upcard_value)
    #     hit_expected_values[upcard] = blackjack.hit_EV(upcard_value)
    
    # # Create dataframes from the results
    # df_probabilities = pd.DataFrame(probability_distributions)
    # df_overall_probabilities = pd.DataFrame(blackjack.probability_distribution().items(), columns=['Outcome', 'Probability'])
    # df_stand_ev = pd.DataFrame(stand_expected_values)
    # df_hit_ev = pd.DataFrame(hit_expected_values)
    
    # # Set index for overall probabilities and transpose
    # df_overall_probabilities.set_index('Outcome', inplace=True)
    # df_overall_probabilities = df_overall_probabilities.T
    
    # # Print the dataframes
    # print("\nOverall Dealer Probability Distribution:\n", df_overall_probabilities)
    # print("\nProbabilities for the dealer's results conditioned on the dealer's first card:\n", df_probabilities)
    # print("\nExpectations, conditioned on the dealer's first card, for the player's profit, when the player stands:\n", df_stand_ev)
    # print("\nExpectations, conditioned on the dealer's first card, for the player's profit, when the player hits:\n", df_hit_ev)