from ProbabilityFunctions import *
import pandas as pd

def create_dealer_prob_dist_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a probability distribution table for the dealer's possible outcomes.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the probability distribution of the dealer's outcomes.
    """
    overall_prob_df = pd.DataFrame(probability_distribution().items(), columns=['Outcome', 'Probability']).round(4)
    overall_prob_df.set_index('Outcome', inplace=True)
    return overall_prob_df.T

def create_dealer_prob_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of dealer probabilities for each upcard value.

    :param dealer_upcards: List of dealer upcard values.
    :return: Dictionary mapping each upcard to its probability distribution.
    """
    dealer_probabilities = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        dealer_probabilities[upcard] = probability_distribution(upcard_value)
    return dealer_probabilities

def create_dealer_prob_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a probability table for the dealer's outcomes.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the probability distribution of the dealer's outcomes.
    """
    return pd.DataFrame(create_dealer_prob_dict(dealer_upcards))

def create_stand_EV_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of expected values for standing with each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: Dictionary mapping each upcard to its expected value when standing.
    """
    stand_expected_values = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        stand_expected_values[upcard] = stand_EV(upcard_value)
    return stand_expected_values

def create_stand_EV_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of expected values for standing with each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the expected values when standing.
    """
    return pd.DataFrame(create_stand_EV_dict(dealer_upcards))

def create_hit_EV_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of expected values for hitting with each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: Dictionary mapping each upcard to its expected value when hitting.
    """
    hit_expected_values = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        hit_expected_values[upcard] = hit_EV(upcard_value)
    return hit_expected_values

def create_hit_EV_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of expected values for hitting with each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the expected values when hitting.
    """
    return pd.DataFrame(create_hit_EV_dict(dealer_upcards))

def create_soft_hit_EV_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of expected values for hitting with a soft hand and each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: Dictionary mapping each upcard to its expected value when hitting with a soft hand.
    """
    soft_hit_expected_values = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        soft_hit_expected_values[upcard] = soft_hit_EV(upcard_value)
    return soft_hit_expected_values

def create_soft_hit_EV_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of expected values for hitting with a soft hand and each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the expected values when hitting with a soft hand.
    """
    return pd.DataFrame(create_soft_hit_EV_dict(dealer_upcards))

def create_optimal_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of optimal expected values for each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: Dictionary mapping each upcard to its optimal expected value.
    """
    stand_expected_values = create_stand_EV_dict(dealer_upcards)
    hit_expected_values = create_hit_EV_dict(dealer_upcards)
    optimal_expected_values = {}
    for upcard in dealer_upcards:
        optimal_expected_values[upcard] = {"BJ": stand_expected_values[upcard]["BJ"]}
        for value in range(21, 10, -1):
            optimal_expected_values[upcard][value] = max(stand_expected_values[upcard][value], hit_expected_values[upcard][value])
    return optimal_expected_values

def create_optimal_values_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of optimal expected values for each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the optimal expected values.
    """
    return pd.DataFrame(create_optimal_dict(dealer_upcards))

def create_optimal_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of optimal moves (Stand or Hit) for each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the optimal moves.
    """
    stand_expected_values = create_stand_EV_dict(dealer_upcards)
    hit_expected_values = create_hit_EV_dict(dealer_upcards)
    optimal_moves = {}
    for upcard in dealer_upcards:
        optimal_moves[upcard] = {}
        for value in range(21, 10, -1):
            optimal_moves[upcard][value] = "Stand" if stand_expected_values[upcard][value] > hit_expected_values[upcard][value] else "Hit"
    return pd.DataFrame(optimal_moves)

def create_soft_optimal_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of optimal expected values for soft hands and each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: Dictionary mapping each upcard to its optimal expected value for soft hands.
    """
    stand_expected_values = create_stand_EV_dict(dealer_upcards)
    soft_hit_expected_values = create_soft_hit_EV_dict(dealer_upcards)
    soft_optimal_expected_values = {}
    for upcard in dealer_upcards:
        soft_optimal_expected_values[upcard] = {"BJ": stand_expected_values[upcard]["BJ"]}
        for value in range(21, 11, -1):
            soft_optimal_expected_values[upcard][value] = max(stand_expected_values[upcard][value], soft_hit_expected_values[upcard][value])
    return soft_optimal_expected_values

def create_soft_optimal_values_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of optimal expected values for soft hands and each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the optimal expected values for soft hands.
    """
    return pd.DataFrame(create_soft_optimal_dict(dealer_upcards))

def create_soft_optimal_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of optimal moves (Stand or Hit) for soft hands and each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the optimal moves for soft hands.
    """
    stand_expected_values = create_stand_EV_dict(dealer_upcards)
    soft_hit_expected_values = create_soft_hit_EV_dict(dealer_upcards)
    soft_optimal_moves = {}
    for upcard in dealer_upcards:
        soft_optimal_moves[upcard] = {}
        for value in range(21, 11, -1):
            soft_optimal_moves[upcard][value] = "Stand" if stand_expected_values[upcard][value] > soft_hit_expected_values[upcard][value] else "Hit"
    return pd.DataFrame(soft_optimal_moves)